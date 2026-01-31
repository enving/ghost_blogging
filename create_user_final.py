#!/usr/bin/env python3
"""
Create Ghost user by uploading SQL file to server
"""
from pathlib import Path
import paramiko
import bcrypt
import secrets

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

def create_user_via_sql_file(email, name, password, role='Editor'):
    """Create user by uploading SQL file to server"""

    # Ghost uses 24-character hex IDs
    user_id = secrets.token_hex(12)
    slug = name.lower().replace(' ', '-')

    # Hash password
    salt = bcrypt.gensalt(rounds=10)
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    print(f"Creating user: {name} ({email})")
    print(f"User ID: {user_id}")
    print(f"Password hash generated")

    # Create SQL content
    sql_content = f"""USE {env['MySQL_database_name']};

-- Get role ID
SET @role_id = (SELECT id FROM roles WHERE name = '{role}' LIMIT 1);

-- Get admin ID for created_by field
SET @admin_id = (SELECT id FROM users WHERE email = '{env['ADMIN_EMAIL']}' LIMIT 1);
SET @admin_id = COALESCE(@admin_id, '1');

-- Delete any existing user with this email
DELETE FROM roles_users WHERE user_id = (SELECT id FROM users WHERE email = '{email}');
DELETE FROM users WHERE email = '{email}';

-- Create user
INSERT INTO users (
    id,
    name,
    slug,
    email,
    password,
    status,
    created_at,
    created_by,
    updated_at,
    updated_by
) VALUES (
    '{user_id}',
    '{name}',
    '{slug}',
    '{email}',
    '{hashed_pw}',
    'active',
    NOW(),
    @admin_id,
    NOW(),
    @admin_id
);

-- Assign role (using hex ID for roles_users too)
SET @roles_users_id = CONCAT(SUBSTRING(MD5(RAND()), 1, 24));
INSERT INTO roles_users (id, role_id, user_id)
VALUES (@roles_users_id, @role_id, '{user_id}');

-- Verify
SELECT 'USER CREATED:' as status;
SELECT u.id, u.name, u.email, u.status,
       CASE WHEN u.password IS NOT NULL THEN 'YES' ELSE 'NO' END as has_password,
       r.name as role
FROM users u
LEFT JOIN roles_users ru ON u.id = ru.user_id
LEFT JOIN roles r ON ru.role_id = r.id
WHERE u.email = '{email}';
"""

    # Connect via SSH
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

        # Write SQL to temp file on server
        temp_sql_file = f"/tmp/create_user_{secrets.token_hex(4)}.sql"

        print(f"\n📝 Writing SQL to {temp_sql_file}...")
        sftp = ssh.open_sftp()
        with sftp.file(temp_sql_file, 'w') as f:
            f.write(sql_content)
        sftp.close()

        print("✅ SQL file written")

        # Execute SQL file
        print("\n🔨 Executing SQL...")
        exec_cmd = f"mysql -u{env['MySQL_username']} -p'{env['MySQL_password']}' < {temp_sql_file}"
        stdin, stdout, stderr = ssh.exec_command(exec_cmd)

        output = stdout.read().decode()
        error = stderr.read().decode()

        if output:
            print("\n📋 Result:")
            print(output)

        if error and 'warning' not in error.lower():
            print(f"\n⚠️  MySQL output: {error}")

        # Clean up temp file
        ssh.exec_command(f"rm {temp_sql_file}")

        # Restart Ghost
        print("\n🔄 Restarting Ghost...")
        restart_cmd = "systemctl restart ghost_digitalalchemisten-de.service"
        stdin, stdout, stderr = ssh.exec_command(restart_cmd)
        stdout.channel.recv_exit_status()
        print("✅ Ghost restarted!")

        print("\n" + "="*60)
        print("✅ USER CREATED SUCCESSFULLY!")
        print("="*60)
        print(f"📧 Email: {email}")
        print(f"👤 Name: {name}")
        print(f"🔑 Password: {password}")
        print(f"👔 Role: {role}")
        print(f"🌐 Login: https://digitalalchemisten.de/ghost/")
        print(f"\n💡 Hard refresh the Staff page (Ctrl+Shift+R or Cmd+Shift+R)")
        print(f"💡 User should appear under '{role}s' section")

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

    if len(sys.argv) < 4:
        print("Usage: python create_user_final.py <email> <name> <password> [role]")
        print("Example: python create_user_final.py user@example.com 'John Doe' 'SecurePass123!' Editor")
        sys.exit(1)

    email = sys.argv[1]
    name = sys.argv[2]
    password = sys.argv[3]
    role = sys.argv[4] if len(sys.argv) > 4 else 'Editor'

    create_user_via_sql_file(email, name, password, role)
