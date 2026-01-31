#!/usr/bin/env python3
"""
Manually create user and show ALL MySQL output
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

def manual_create():
    """Create user and show all output"""

    email = "sebastian.schade@posteo.de"
    name = "Sebastian Schade"
    password = "GhostEditor2025!"
    role = "Editor"

    user_id = secrets.token_hex(12)
    slug = "sebastian-schade"

    # Hash password
    salt = bcrypt.gensalt(rounds=10)
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    print(f"User ID: {user_id}")
    print(f"Password hash: {hashed_pw[:50]}...")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(
            hostname=env['VPS_IP'],
            username=env['VPS_USER'],
            password=env['VPS_PW']
        )

        print("✅ SSH Connected!")

        # Step 1: Delete any existing user
        print("\n1️⃣ Cleaning up any existing data...")
        cleanup_sql = f"DELETE FROM {env['MySQL_database_name']}.users WHERE email = '{email}'; SELECT ROW_COUNT() as deleted_rows;"

        cmd = f"mysql -u{env['MySQL_username']} -p'{env['MySQL_password']}' -e \"{cleanup_sql}\" 2>&1"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        print(stdout.read().decode())

        # Step 2: Get role ID
        print("\n2️⃣ Getting Editor role ID...")
        role_sql = f"SELECT id, name FROM {env['MySQL_database_name']}.roles WHERE name = 'Editor';"

        cmd = f"mysql -u{env['MySQL_username']} -p'{env['MySQL_password']}' -e \"{role_sql}\" 2>&1"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        role_output = stdout.read().decode()
        print(role_output)

        # Extract role ID from output
        role_id = None
        for line in role_output.strip().split('\n')[1:]:  # Skip header
            if 'Editor' in line:
                role_id = line.split()[0]
                break

        if not role_id:
            print("❌ Could not find Editor role!")
            return False

        print(f"✅ Editor role ID: {role_id}")

        # Step 3: Create user
        print(f"\n3️⃣ Creating user...")
        insert_sql = f"""INSERT INTO {env['MySQL_database_name']}.users
        (id, name, slug, email, password, status, created_at, updated_at)
        VALUES
        ('{user_id}', '{name}', '{slug}', '{email}', '{hashed_pw}', 'active', NOW(), NOW());
        SELECT ROW_COUNT() as inserted_rows;"""

        cmd = f"mysql -u{env['MySQL_username']} -p'{env['MySQL_password']}' -e \"{insert_sql}\" 2>&1"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        insert_output = stdout.read().decode()
        print(insert_output)

        if 'ERROR' in insert_output:
            print("❌ Failed to create user!")
            return False

        # Step 4: Assign role
        print(f"\n4️⃣ Assigning role...")
        roles_users_id = secrets.token_hex(12)
        role_assign_sql = f"""INSERT INTO {env['MySQL_database_name']}.roles_users
        (id, role_id, user_id)
        VALUES
        ('{roles_users_id}', '{role_id}', '{user_id}');
        SELECT ROW_COUNT() as assigned_rows;"""

        cmd = f"mysql -u{env['MySQL_username']} -p'{env['MySQL_password']}' -e \"{role_assign_sql}\" 2>&1"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        assign_output = stdout.read().decode()
        print(assign_output)

        # Step 5: Verify
        print(f"\n5️⃣ Verifying...")
        verify_sql = f"""SELECT u.id, u.name, u.email, u.status, r.name as role
        FROM {env['MySQL_database_name']}.users u
        LEFT JOIN {env['MySQL_database_name']}.roles_users ru ON u.id = ru.user_id
        LEFT JOIN {env['MySQL_database_name']}.roles r ON ru.role_id = r.id
        WHERE u.email = '{email}';"""

        cmd = f"mysql -u{env['MySQL_username']} -p'{env['MySQL_password']}' -e \"{verify_sql}\" 2>&1"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        verify_output = stdout.read().decode()
        print(verify_output)

        #  Restart Ghost
        print(f"\n6️⃣ Restarting Ghost...")
        ssh.exec_command("systemctl restart ghost_digitalalchemisten-de.service")

        print("\n" + "="*60)
        print("✅ DONE!")
        print("="*60)
        print(f"📧 Email: {email}")
        print(f"🔑 Password: {password}")

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        ssh.close()

if __name__ == '__main__':
    manual_create()
