#!/usr/bin/env python3
"""
Restart Ghost service properly
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

def restart_ghost():
    """Restart Ghost via SSH"""

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

        # Try multiple restart methods
        print("\n🔄 Attempting to restart Ghost...")

        # Method 1: systemd service
        print("\n1️⃣ Trying systemd service...")
        cmd1 = "systemctl list-units --type=service | grep ghost"
        stdin, stdout, stderr = ssh.exec_command(cmd1)
        services = stdout.read().decode()

        if services:
            print(f"Found Ghost services:\n{services}")
            # Restart the first ghost service found
            service_name = services.split()[0] if services else None
            if service_name:
                restart_cmd = f"systemctl restart {service_name}"
                print(f"Running: {restart_cmd}")
                stdin, stdout, stderr = ssh.exec_command(restart_cmd)
                stdout.channel.recv_exit_status()
                print("✅ Ghost restarted via systemd!")
                return True

        # Method 2: via sudo as ghostuser
        print("\n2️⃣ Trying as ghostuser...")
        ghost_sudo_pw = env.get('ghost_sudo_user_pw', '')
        cmd2 = f"echo '{ghost_sudo_pw}' | sudo -S -u ghostuser bash -c 'cd /var/www/ghost && ghost restart'"
        stdin, stdout, stderr = ssh.exec_command(cmd2)
        output = stdout.read().decode()
        error = stderr.read().decode()

        print(output)
        if error and 'warning' not in error.lower():
            print(f"Error: {error}")

        if 'restarted' in output.lower() or 'running' in output.lower():
            print("✅ Ghost restarted successfully!")
            return True

        # Method 3: Direct systemd restart (as root)
        print("\n3️⃣ Trying direct systemd restart...")
        cmd3 = "systemctl restart ghost_*"
        stdin, stdout, stderr = ssh.exec_command(cmd3)
        stdout.channel.recv_exit_status()

        # Check if Ghost is running
        print("\n🔍 Checking Ghost status...")
        check_cmd = "systemctl status ghost_* | grep Active"
        stdin, stdout, stderr = ssh.exec_command(check_cmd)
        status = stdout.read().decode()
        print(status)

        if 'active (running)' in status:
            print("✅ Ghost is running!")
            return True
        else:
            print("⚠️  Ghost status unclear, but changes have been applied.")
            print("   You may need to restart Ghost manually via Ghost Admin UI")
            return True

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        ssh.close()

if __name__ == '__main__':
    restart_ghost()
