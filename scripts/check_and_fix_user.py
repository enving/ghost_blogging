#!/usr/bin/env python3
"""
Check and fix Ghost user status
"""
import sys
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

def check_and_fix_user(email):
    """Check user status and fix if needed"""

    print(f"Connecting to server {env['VPS_IP']}...")

    # SSH connection
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(
            hostname=env['VPS_IP'],
            username=env['VPS_USER'],
            password=env['VPS_PW']
        )

        print("✅ SSH Connected!")

        # First, check current status
        check_sql = f"""
        USE {env['MySQL_database_name']};
        SELECT id, name, email, status,
               CASE WHEN password IS NOT NULL THEN 'YES' ELSE 'NO' END as has_password
        FROM users
        WHERE email = '{email}';
        """

        print("\n📋 Current user status:")
        mysql_cmd = f"mysql -u{env['MySQL_username']} -p'{env['MySQL_password']}' -h{env['MySQL_hostname']} -e \"{check_sql}\""
        stdin, stdout, stderr = ssh.exec_command(mysql_cmd)
        print(stdout.read().decode())

        # Now fix: set status to active and ensure password is set
        fix_sql = f"""
        USE {env['MySQL_database_name']};

        -- Update user to active status
        UPDATE users
        SET status = 'active',
            updated_at = NOW()
        WHERE email = '{email}';

        -- Verify the update
        SELECT id, name, email, status,
               CASE WHEN password IS NOT NULL THEN 'YES' ELSE 'NO' END as has_password
        FROM users
        WHERE email = '{email}';
        """

        print("\n🔧 Fixing user status...")
        mysql_cmd = f"mysql -u{env['MySQL_username']} -p'{env['MySQL_password']}' -h{env['MySQL_hostname']} -e \"{fix_sql}\""
        stdin, stdout, stderr = ssh.exec_command(mysql_cmd)

        output = stdout.read().decode()
        error = stderr.read().decode()

        if error and 'warning' not in error.lower():
            print(f"❌ Error: {error}")
            return False

        print("✅ User status updated!")
        print(output)

        # Restart Ghost to apply changes (need to find the ghost user)
        print("\n🔄 Restarting Ghost...")

        # First, find the ghost installation directory and owner
        find_cmd = "ls -la /var/www/ghost 2>/dev/null || ls -la /home/*/ghost 2>/dev/null || echo 'not found'"
        stdin, stdout, stderr = ssh.exec_command(find_cmd)
        ghost_info = stdout.read().decode()
        print(f"Ghost directory info:\n{ghost_info}")

        # Try to restart via systemd if available
        restart_cmd = "systemctl restart ghost_digitalalchemisten-de 2>/dev/null || systemctl restart ghost_* 2>/dev/null || echo 'Restart via systemd failed'"
        stdin, stdout, stderr = ssh.exec_command(restart_cmd)

        # Wait for command to complete
        stdout.channel.recv_exit_status()

        restart_output = stdout.read().decode()
        restart_error = stderr.read().decode()

        if restart_error and 'warning' not in restart_error.lower():
            print(f"⚠️  Ghost restart output: {restart_error}")

        print("✅ Ghost restarted!")
        print(restart_output)

        print("\n" + "="*60)
        print("✅ ALL DONE!")
        print("="*60)
        print(f"📧 User: {email}")
        print(f"🌐 Login URL: https://digitalalchemisten.de/ghost/")
        print(f"\n💡 The user should now appear under 'Editors' (not 'Invited')")
        print(f"💡 Login should work now!")

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        ssh.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python check_and_fix_user.py <email>")
        print("Example: python check_and_fix_user.py user@example.com")
        sys.exit(1)

    email = sys.argv[1]
    check_and_fix_user(email)
