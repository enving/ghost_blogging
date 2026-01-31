#!/usr/bin/env python3
"""
Run MySQL commands directly and show ALL output including errors
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

def direct_mysql():
    """Execute MySQL directly and show output"""

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

        # Simple test - just try to create a user step by step
        print("\n🔨 Testing MySQL connection and database...")

        # Step 1: Check if database exists and we can connect
        cmd1 = f"mysql -u{env['MySQL_username']} -p'{env['MySQL_password']}' -e 'SHOW DATABASES;'"
        stdin, stdout, stderr = ssh.exec_command(cmd1)
        print("\n📋 Databases:")
        print(stdout.read().decode())
        errors = stderr.read().decode()
        if errors:
            print(f"Errors: {errors}")

        # Step 2: Check users table
        cmd2 = f"mysql -u{env['MySQL_username']} -p'{env['MySQL_password']}' {env['MySQL_database_name']} -e 'SELECT COUNT(*) as user_count FROM users;'"
        stdin, stdout, stderr = ssh.exec_command(cmd2)
        print("\n📋 User count:")
        print(stdout.read().decode())
        errors = stderr.read().decode()
        if errors:
            print(f"Errors: {errors}")

        # Step 3: Try a simple INSERT to test
        print("\n🧪 Testing simple INSERT...")
        test_sql = f"""INSERT INTO {env['MySQL_database_name']}.users (
            id, name, slug, email, status, created_at, updated_at
        ) VALUES (
            UUID(), 'Test User', 'test-user', 'test@example.com', 'active', NOW(), NOW()
        );"""

        cmd3 = f"mysql -u{env['MySQL_username']} -p'{env['MySQL_password']}' -e \"{test_sql}\""
        stdin, stdout, stderr = ssh.exec_command(cmd3)
        stdout.channel.recv_exit_status()

        output = stdout.read().decode()
        errors = stderr.read().decode()

        if output:
            print(f"Output: {output}")
        if errors:
            print(f"Errors/Warnings: {errors}")

        # Check if test user was created
        cmd4 = f"mysql -u{env['MySQL_username']} -p'{env['MySQL_password']}' {env['MySQL_database_name']} -e \"SELECT * FROM users WHERE email='test@example.com';\""
        stdin, stdout, stderr = ssh.exec_command(cmd4)
        print("\n📋 Test user:")
        print(stdout.read().decode())

        # Clean up test user
        cmd5 = f"mysql -u{env['MySQL_username']} -p'{env['MySQL_password']}' {env['MySQL_database_name']} -e \"DELETE FROM users WHERE email='test@example.com';\""
        ssh.exec_command(cmd5)
        print("✅ Test user cleaned up")

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        ssh.close()

if __name__ == '__main__':
    direct_mysql()
