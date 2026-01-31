#!/usr/bin/env python3
"""
Set password for Ghost user directly in database
"""
import sys
from pathlib import Path
import paramiko
import bcrypt
import secrets
import string

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

def generate_password(length=16):
    """Generate a random secure password"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return password

def hash_password(password):
    """Hash password using bcrypt (Ghost's method)"""
    # Ghost uses bcrypt with 10 rounds
    salt = bcrypt.gensalt(rounds=10)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def set_password_via_ssh(email, password=None):
    """Set password for Ghost user via SSH and database"""

    if not password:
        password = generate_password()
        print(f"🔑 Generated password: {password}")
    else:
        print(f"🔑 Using provided password")

    # Hash the password
    hashed_password = hash_password(password)
    print(f"✅ Password hashed successfully")

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

        # Escape single quotes in password for SQL
        hashed_password_escaped = hashed_password.replace("'", "\\'")

        # SQL commands to set password and activate user
        sql_commands = f"""
        USE {env['MySQL_database_name']};

        -- Update password and activate user
        UPDATE users
        SET password = '{hashed_password_escaped}',
            status = 'active',
            updated_at = NOW()
        WHERE email = '{email}';

        -- Verify update
        SELECT id, name, email, status,
               CASE WHEN password IS NOT NULL THEN 'SET' ELSE 'NOT SET' END as password_status
        FROM users
        WHERE email = '{email}';
        """

        # Execute MySQL command via SSH
        mysql_cmd = f"mysql -u{env['MySQL_username']} -p'{env['MySQL_password']}' -h{env['MySQL_hostname']} -e \"{sql_commands}\""

        stdin, stdout, stderr = ssh.exec_command(mysql_cmd)

        output = stdout.read().decode()
        error = stderr.read().decode()

        if error and 'warning' not in error.lower():
            print(f"❌ Error: {error}")
            return None

        print("✅ Password set successfully!")
        print(output)

        print(f"\n📧 User: {email}")
        print(f"🔑 Password: {password}")
        print(f"🌐 Login URL: https://digitalalchemisten.de/ghost/")
        print(f"\n⚠️  IMPORTANT: Save this password and send it to the user!")

        return password

    except Exception as e:
        print(f"❌ Error: {e}")
        return None

    finally:
        ssh.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python set_user_password.py <email> [password]")
        print("Example: python set_user_password.py user@example.com")
        print("         python set_user_password.py user@example.com MySecurePass123!")
        print("\nIf no password is provided, a random one will be generated.")
        sys.exit(1)

    email = sys.argv[1]
    password = sys.argv[2] if len(sys.argv) > 2 else None

    set_password_via_ssh(email, password)
