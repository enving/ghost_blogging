#!/usr/bin/env python3
"""
Fix Ghost device verification issue
"""
from pathlib import Path
import paramiko
import json

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

def fix_device_verification():
    """Disable staff device verification"""

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

        # Read current config
        print("\n📖 Reading current Ghost config...")
        stdin, stdout, stderr = ssh.exec_command("cat /var/www/ghost/config.production.json")
        config_str = stdout.read().decode()
        config = json.loads(config_str)

        print("Current config:")
        print(json.dumps(config, indent=2))

        # Update config - disable device verification
        if 'security' not in config:
            config['security'] = {}

        config['security']['staffDeviceVerification'] = False

        print("\n✏️  Updated config (staffDeviceVerification: false):")
        print(json.dumps(config, indent=2))

        # Write updated config back
        print("\n💾 Writing updated config to server...")
        updated_config = json.dumps(config, indent=2)

        # Use SFTP to write the file
        sftp = ssh.open_sftp()
        with sftp.file('/tmp/config.production.json', 'w') as f:
            f.write(updated_config)
        sftp.close()

        # Move temp file to actual location (need sudo)
        print("📝 Replacing config file...")
        stdin, stdout, stderr = ssh.exec_command(
            "mv /tmp/config.production.json /var/www/ghost/config.production.json && "
            "chown ghostuser:ghostuser /var/www/ghost/config.production.json"
        )
        stdout.channel.recv_exit_status()

        # Restart Ghost
        print("\n🔄 Restarting Ghost...")
        stdin, stdout, stderr = ssh.exec_command("systemctl restart ghost_digitalalchemisten-de.service")
        stdout.channel.recv_exit_status()

        # Wait a moment for Ghost to start
        import time
        time.sleep(3)

        # Check status
        print("\n✅ Checking Ghost status...")
        stdin, stdout, stderr = ssh.exec_command("systemctl is-active ghost_digitalalchemisten-de.service")
        status = stdout.read().decode().strip()

        if status == "active":
            print("✅ Ghost is running!")
        else:
            print(f"⚠️  Ghost status: {status}")

        print("\n" + "="*60)
        print("✅ DEVICE VERIFICATION DISABLED!")
        print("="*60)
        print("Sebastian kann sich jetzt anmelden:")
        print(f"🌐 https://digitalalchemisten.de/ghost/")
        print(f"📧 sebastian.schade@posteo.de")
        print(f"🔑 GhostEditor2025!")
        print("\n💡 Bitte Sebastian bitten, die Seite neu zu laden (Ctrl+Shift+R)")

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        ssh.close()

if __name__ == '__main__':
    fix_device_verification()
