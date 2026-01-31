#!/usr/bin/env python3
"""
Add Ghost user directly to MySQL database via SSH
"""
import sys
from pathlib import Path

# Try to import paramiko
try:
    import paramiko
except ImportError:
    print("Installing paramiko...")
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--user', 'paramiko'])
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

def add_user_via_ssh(email, name, slug=None, role='Editor'):
    """Add user directly to Ghost MySQL database via SSH"""

    if not slug:
        slug = name.lower().replace(' ', '-')

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

        # SQL commands to create user
        sql_commands = f"""
        USE {env['MySQL_database_name']};

        -- Get Editor role ID
        SET @role_id = (SELECT id FROM roles WHERE name = '{role}' LIMIT 1);

        -- Check if user already exists
        SET @existing_user = (SELECT id FROM users WHERE email = '{email}' LIMIT 1);

        -- Only insert if user doesn't exist
        INSERT INTO users (id, name, slug, email, status, created_at, created_by, updated_at, updated_by)
        SELECT UUID(), '{name}', '{slug}', '{email}', 'active', NOW(), '1', NOW(), '1'
        WHERE @existing_user IS NULL;

        -- Get the user ID (new or existing)
        SET @user_id = (SELECT id FROM users WHERE email = '{email}' LIMIT 1);

        -- Check if role assignment exists
        SET @existing_role = (SELECT id FROM roles_users WHERE user_id = @user_id LIMIT 1);

        -- Assign role if not already assigned
        INSERT INTO roles_users (id, role_id, user_id)
        SELECT UUID(), @role_id, @user_id
        WHERE @existing_role IS NULL;

        -- Show result
        SELECT u.id, u.name, u.email, u.status, r.name as role
        FROM users u
        LEFT JOIN roles_users ru ON u.id = ru.user_id
        LEFT JOIN roles r ON ru.role_id = r.id
        WHERE u.email = '{email}';
        """

        # Execute MySQL command via SSH
        mysql_cmd = f"mysql -u{env['MySQL_username']} -p'{env['MySQL_password']}' -h{env['MySQL_hostname']} -e \"{sql_commands}\""

        stdin, stdout, stderr = ssh.exec_command(mysql_cmd)

        output = stdout.read().decode()
        error = stderr.read().decode()

        if error and 'warning' not in error.lower():
            print(f"❌ Error: {error}")
            return False

        print("✅ User created/updated successfully!")
        print(output)

        print(f"\n📧 User '{name}' ({email}) has been added with role '{role}'")
        print(f"\n⚠️  IMPORTANT: The user needs a password!")
        print(f"Options:")
        print(f"1. Send password reset link via Ghost Admin UI")
        print(f"2. Set password directly via Ghost Admin > Staff")
        print(f"3. User can use 'Forgot Password' at https://digitalalchemisten.de/ghost/")

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

    finally:
        ssh.close()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python add_user_db.py <email> <name> [role]")
        print("Example: python add_user_db.py user@example.com 'John Doe' Editor")
        print("\nAvailable roles: Editor, Author, Contributor, Administrator, Owner")
        sys.exit(1)

    email = sys.argv[1]
    name = sys.argv[2]
    role = sys.argv[3] if len(sys.argv) > 3 else 'Editor'

    add_user_via_ssh(email, name, role=role)
