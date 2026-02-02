#!/usr/bin/env python3
"""
Debug user status and create properly
"""
from pathlib import Path
import paramiko
import bcrypt
import uuid

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

def hash_password(password):
    """Hash password using bcrypt"""
    salt = bcrypt.gensalt(rounds=10)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def debug_and_create_user(email, name, password, role='Editor'):
    """Debug current state and create user properly"""

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

        # Step 1: Debug - check current state
        debug_sql = f"""
        USE {env['MySQL_database_name']};

        SELECT 'ALL USERS:' as info;
        SELECT id, name, email, status FROM users;

        SELECT 'ALL ROLES:' as info;
        SELECT id, name FROM roles;

        SELECT 'ROLES_USERS ASSIGNMENTS:' as info;
        SELECT ru.id, u.email, r.name as role
        FROM roles_users ru
        LEFT JOIN users u ON ru.user_id = u.id
        LEFT JOIN roles r ON ru.role_id = r.id;

        SELECT 'INVITES:' as info;
        SELECT email, status FROM invites;

        SELECT 'CHECKING FOR {email}:' as info;
        SELECT * FROM users WHERE email = '{email}';
        """

        print("\n📋 DEBUGGING CURRENT STATE...")
        print("="*60)
        mysql_cmd = f"mysql -u{env['MySQL_username']} -p'{env['MySQL_password']}' -h{env['MySQL_hostname']} -e \"{debug_sql}\""
        stdin, stdout, stderr = ssh.exec_command(mysql_cmd)
        debug_output = stdout.read().decode()
        print(debug_output)

        # Step 2: Clean up any existing data for this email
        cleanup_sql = f"""
        USE {env['MySQL_database_name']};

        -- Delete any invites
        DELETE FROM invites WHERE email = '{email}';

        -- Get user id if exists
        SET @user_id = (SELECT id FROM users WHERE email = '{email}' LIMIT 1);

        -- Delete role assignments
        DELETE FROM roles_users WHERE user_id = @user_id;

        -- Delete user
        DELETE FROM users WHERE email = '{email}';

        SELECT 'CLEANUP DONE' as status;
        """

        print("\n🧹 CLEANING UP OLD DATA...")
        mysql_cmd = f"mysql -u{env['MySQL_username']} -p'{env['MySQL_password']}' -h{env['MySQL_hostname']} -e \"{cleanup_sql}\""
        stdin, stdout, stderr = ssh.exec_command(mysql_cmd)
        cleanup_output = stdout.read().decode()
        print(cleanup_output)

        # Step 3: Create user from scratch
        user_id = str(uuid.uuid4())
        hashed_pw = hash_password(password)
        hashed_pw_escaped = hashed_pw.replace("'", "\\'").replace("$", "\\$")
        slug = name.lower().replace(' ', '-')

        create_sql = f"""
        USE {env['MySQL_database_name']};

        -- Get the role ID for {role}
        SET @role_id = (SELECT id FROM roles WHERE name = '{role}' LIMIT 1);

        -- Get the admin/owner user ID (for created_by)
        SET @admin_id = (SELECT id FROM users WHERE email = '{env['ADMIN_EMAIL']}' LIMIT 1);

        -- Create the user
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
            '{hashed_pw_escaped}',
            'active',
            NOW(),
            COALESCE(@admin_id, '1'),
            NOW(),
            COALESCE(@admin_id, '1')
        );

        -- Assign role
        INSERT INTO roles_users (id, role_id, user_id)
        VALUES (UUID(), @role_id, '{user_id}');

        -- Verify creation
        SELECT '✅ USER CREATED:' as status;
        SELECT u.id, u.name, u.email, u.status, r.name as role
        FROM users u
        LEFT JOIN roles_users ru ON u.id = ru.user_id
        LEFT JOIN roles r ON ru.role_id = r.id
        WHERE u.email = '{email}';
        """

        print("\n🔨 CREATING USER FROM SCRATCH...")
        print("="*60)
        mysql_cmd = f"mysql -u{env['MySQL_username']} -p'{env['MySQL_password']}' -h{env['MySQL_hostname']} -e \"{create_sql}\""
        stdin, stdout, stderr = ssh.exec_command(mysql_cmd)

        create_output = stdout.read().decode()
        create_error = stderr.read().decode()

        if create_error and 'warning' not in create_error.lower():
            print(f"⚠️  Errors/Warnings: {create_error}")

        print(create_output)

        # Step 4: Restart Ghost
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
        print(f"\n💡 Refresh the Staff page in Ghost Admin (hard refresh: Ctrl+Shift+R)")

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
        print("Usage: python debug_and_create_user.py <email> <name> <password> [role]")
        print("Example: python debug_and_create_user.py user@example.com 'John Doe' 'SecurePass123!' Editor")
        print("\nAvailable roles: Editor, Author, Contributor, Administrator")
        sys.exit(1)

    email = sys.argv[1]
    name = sys.argv[2]
    password = sys.argv[3]
    role = sys.argv[4] if len(sys.argv) > 4 else 'Editor'

    debug_and_create_user(email, name, password, role)
