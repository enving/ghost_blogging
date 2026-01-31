#!/usr/bin/env python3
"""
Verify user exists in database
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

def verify_user(email):
    """Check if user exists and show details"""

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

        check_sql = f"""
        USE {env['MySQL_database_name']};

        SELECT 'ALL USERS IN DATABASE:' as info;
        SELECT id, name, email, status,
               CASE WHEN password IS NOT NULL AND password != '' THEN 'YES' ELSE 'NO' END as has_password
        FROM users;

        SELECT 'ROLE ASSIGNMENTS:' as info;
        SELECT u.email, r.name as role
        FROM roles_users ru
        JOIN users u ON ru.user_id = u.id
        JOIN roles r ON ru.role_id = r.id;

        SELECT 'LOOKING FOR {email}:' as info;
        SELECT u.id, u.name, u.email, u.status,
               CASE WHEN u.password IS NOT NULL AND u.password != '' THEN 'YES' ELSE 'NO' END as has_password,
               r.name as role
        FROM users u
        LEFT JOIN roles_users ru ON u.id = ru.user_id
        LEFT JOIN roles r ON ru.role_id = r.id
        WHERE u.email = '{email}';
        """

        mysql_cmd = f"mysql -u{env['MySQL_username']} -p'{env['MySQL_password']}' -h{env['MySQL_hostname']} -e \"{check_sql}\""
        stdin, stdout, stderr = ssh.exec_command(mysql_cmd)

        output = stdout.read().decode()
        error = stderr.read().decode()

        print("\n" + "="*60)
        print(output)

        if error and 'warning' not in error.lower():
            print(f"\n⚠️  Errors: {error}")

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

    finally:
        ssh.close()

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        email = "sebastian.schade@posteo.de"
        print(f"Checking for: {email}")
    else:
        email = sys.argv[1]

    verify_user(email)
