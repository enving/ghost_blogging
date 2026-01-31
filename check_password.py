#!/usr/bin/env python3
"""
Check password hash for Sebastian
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

def check_password():
    """Check password hash"""

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

        # Check both users' password hashes
        check_sql = f"""
        USE {env['MySQL_database_name']};

        SELECT
            name,
            email,
            SUBSTRING(password, 1, 20) as password_start,
            LENGTH(password) as password_length,
            CASE WHEN password IS NULL OR password = '' THEN 'NO' ELSE 'YES' END as has_password
        FROM users
        WHERE email IN ('tristanwilms111@gmail.com', 'sebastian.schade@posteo.de');
        """

        cmd = f"mysql -u{env['MySQL_username']} -p'{env['MySQL_password']}' -e \"{check_sql}\" 2>&1 | grep -v Warning"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        output = stdout.read().decode()

        print("\n" + "="*60)
        print("PASSWORD COMPARISON")
        print("="*60)
        print(output)

        # Now let's reset Sebastian's password with a simpler one
        print("\n🔑 Resetting Sebastian's password to a simple one for testing...")

        # Use Ghost's bcrypt format - let's check what Tristan's looks like first
        get_tristan_pw = f"""
        USE {env['MySQL_database_name']};
        SELECT password FROM users WHERE email = 'tristanwilms111@gmail.com';
        """

        cmd = f"mysql -u{env['MySQL_username']} -p'{env['MySQL_password']}' -e \"{get_tristan_pw}\" 2>&1 | grep -v Warning"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        tristan_output = stdout.read().decode()

        print("\nTristan's password hash format:")
        print(tristan_output)

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        ssh.close()

if __name__ == '__main__':
    check_password()
