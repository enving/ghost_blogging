#!/usr/bin/env python3
"""
Check Ghost ID format
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

def check_id_format():
    """Check what ID format Ghost uses"""

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

        # Check ID format and column definition
        check_sql = f"""
        USE {env['MySQL_database_name']};

        -- Show table structure
        DESCRIBE users;

        -- Show existing IDs
        SELECT id, LENGTH(id) as id_length, name, email FROM users;

        -- Show role IDs
        SELECT id, LENGTH(id) as id_length, name FROM roles LIMIT 5;
        """

        cmd = f"mysql -u{env['MySQL_username']} -p'{env['MySQL_password']}' -e \"{check_sql}\""
        stdin, stdout, stderr = ssh.exec_command(cmd)

        output = stdout.read().decode()
        print("\n" + "="*60)
        print(output)

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

    finally:
        ssh.close()

if __name__ == '__main__':
    check_id_format()
