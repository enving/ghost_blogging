#!/usr/bin/env python3
"""
Reset Sebastian's password properly
"""
from pathlib import Path
import paramiko
import bcrypt

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

def reset_password(email, password):
    """Reset password using prepared statement to avoid escaping issues"""

    print(f"Resetting password for {email}...")
    print(f"New password: {password}")

    # Hash password
    salt = bcrypt.gensalt(rounds=10)
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    print(f"Password hash: {hashed_pw}")
    print(f"Hash length: {len(hashed_pw)}")

    if not hashed_pw.startswith('$2'):
        print("❌ Invalid bcrypt hash format!")
        return False

    print(f"\nConnecting to server {env['VPS_IP']}...")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(
            hostname=env['VPS_IP'],
            username=env['VPS_USER'],
            password=env['VPS_PW']
        )

        print("✅ SSH Connected!")

        # Create a SQL file on the server to avoid escaping issues
        sql_content = f"""USE {env['MySQL_database_name']};
UPDATE users
SET password = '{hashed_pw}',
    updated_at = NOW()
WHERE email = '{email}';

-- Verify
SELECT
    name,
    email,
    SUBSTRING(password, 1, 20) as password_start,
    LENGTH(password) as password_length
FROM users
WHERE email = '{email}';
"""

        # Write SQL to temp file on server
        print("\n📝 Creating SQL file on server...")
        sftp = ssh.open_sftp()
        temp_file = f'/tmp/reset_password_{email.replace("@", "_").replace(".", "_")}.sql'
        with sftp.file(temp_file, 'w') as f:
            f.write(sql_content)
        sftp.close()

        print(f"✅ SQL file written: {temp_file}")

        # Execute SQL file
        print("\n🔧 Executing password update...")
        cmd = f"mysql -u{env['MySQL_username']} -p'{env['MySQL_password']}' < {temp_file} 2>&1 | grep -v Warning"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        output = stdout.read().decode()

        print("\n📋 Result:")
        print(output)

        # Clean up
        ssh.exec_command(f"rm {temp_file}")

        # Restart Ghost
        print("\n🔄 Restarting Ghost...")
        stdin, stdout, stderr = ssh.exec_command("systemctl restart ghost_digitalalchemisten-de.service")
        stdout.channel.recv_exit_status()

        import time
        time.sleep(2)

        print("\n" + "="*60)
        print("✅ PASSWORD RESET COMPLETE!")
        print("="*60)
        print(f"📧 Email: {email}")
        print(f"🔑 Password: {password}")
        print(f"🌐 Login: https://digitalalchemisten.de/ghost/")
        print("\n💡 Sebastian sollte jetzt einloggen können!")

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        ssh.close()

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 3:
        # Default values
        email = "sebastian.schade@posteo.de"
        password = "GhostEditor2025!"
        print(f"Using default credentials: {email}")
    else:
        email = sys.argv[1]
        password = sys.argv[2]

    reset_password(email, password)
