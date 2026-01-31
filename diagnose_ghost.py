#!/usr/bin/env python3
"""
Diagnose Ghost server issues
"""
from pathlib import Path
import paramiko

# Load credentials from .env
def load_env():
    env_vars = {}
    env_path = Path(__file__).parent / '.env'
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key] = value
    return env_vars

env = load_env()

def diagnose():
    """Diagnose Ghost server"""

    print(f"Connecting to server {env['VPS_IP']}...")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(
            hostname=env['VPS_IP'],
            username=env['VPS_USER'],
            password=env['VPS_PW']
        )

        print("✅ SSH Connected!")

        # 1. Check Ghost service status
        print("\n" + "="*60)
        print("1️⃣ GHOST SERVICE STATUS")
        print("="*60)
        stdin, stdout, stderr = ssh.exec_command("systemctl status ghost_digitalalchemisten-de.service")
        print(stdout.read().decode())

        # 2. Check if Ghost is listening on ports
        print("\n" + "="*60)
        print("2️⃣ GHOST LISTENING PORTS")
        print("="*60)
        stdin, stdout, stderr = ssh.exec_command("netstat -tlnp | grep node || ss -tlnp | grep node")
        print(stdout.read().decode())

        # 3. Check Ghost logs (last 50 lines)
        print("\n" + "="*60)
        print("3️⃣ GHOST LOGS (Last 50 lines)")
        print("="*60)
        stdin, stdout, stderr = ssh.exec_command("journalctl -u ghost_digitalalchemisten-de.service -n 50 --no-pager")
        print(stdout.read().decode())

        # 4. Check Ghost config file
        print("\n" + "="*60)
        print("4️⃣ GHOST CONFIG")
        print("="*60)
        stdin, stdout, stderr = ssh.exec_command("cat /var/www/ghost/config.production.json")
        print(stdout.read().decode())

        # 5. Check MySQL connection
        print("\n" + "="*60)
        print("5️⃣ MYSQL CONNECTION TEST")
        print("="*60)
        stdin, stdout, stderr = ssh.exec_command(f"mysql -u{env['MySQL_username']} -p'{env['MySQL_password']}' -e 'SELECT 1;' 2>&1")
        mysql_output = stdout.read().decode()
        if "ERROR" in mysql_output:
            print(f"❌ MySQL Error: {mysql_output}")
        else:
            print("✅ MySQL connection OK")

        # 6. Check disk space
        print("\n" + "="*60)
        print("6️⃣ DISK SPACE")
        print("="*60)
        stdin, stdout, stderr = ssh.exec_command("df -h /var/www/ghost")
        print(stdout.read().decode())

        # 7. Check Sebastian's user
        print("\n" + "="*60)
        print("7️⃣ SEBASTIAN'S USER IN DATABASE")
        print("="*60)
        check_user_sql = f"SELECT id, name, email, status FROM {env['MySQL_database_name']}.users WHERE email = 'sebastian.schade@posteo.de';"
        stdin, stdout, stderr = ssh.exec_command(f"mysql -u{env['MySQL_username']} -p'{env['MySQL_password']}' -e \"{check_user_sql}\" 2>&1 | grep -v Warning")
        print(stdout.read().decode())

        print("\n" + "="*60)
        print("DIAGNOSIS COMPLETE")
        print("="*60)

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

    finally:
        ssh.close()

if __name__ == '__main__':
    diagnose()
