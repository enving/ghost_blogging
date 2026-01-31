#!/usr/bin/env python3
"""
Fix invited status - delete invite entries and ensure user is active
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

def fix_invited_status(email):
    """Remove invite entries and set user to active"""

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

        # First, check all tables for this email
        check_sql = f"""
        USE {env['MySQL_database_name']};

        -- Check users table
        SELECT 'USERS TABLE:' as info;
        SELECT id, name, email, status,
               CASE WHEN password IS NOT NULL THEN 'YES' ELSE 'NO' END as has_password
        FROM users
        WHERE email = '{email}';

        -- Check invites table
        SELECT 'INVITES TABLE:' as info;
        SELECT * FROM invites WHERE email = '{email}';
        """

        print("\n📋 Checking current state...")
        mysql_cmd = f"mysql -u{env['MySQL_username']} -p'{env['MySQL_password']}' -h{env['MySQL_hostname']} -e \"{check_sql}\""
        stdin, stdout, stderr = ssh.exec_command(mysql_cmd)
        output = stdout.read().decode()
        print(output)

        # Now fix: delete invites and set user to active
        fix_sql = f"""
        USE {env['MySQL_database_name']};

        -- Delete any invite entries
        DELETE FROM invites WHERE email = '{email}';

        -- Update user to active status
        UPDATE users
        SET status = 'active',
            updated_at = NOW()
        WHERE email = '{email}';

        -- Verify changes
        SELECT 'AFTER FIX - USERS:' as info;
        SELECT id, name, email, status,
               CASE WHEN password IS NOT NULL THEN 'YES' ELSE 'NO' END as has_password
        FROM users
        WHERE email = '{email}';

        SELECT 'AFTER FIX - INVITES:' as info;
        SELECT COUNT(*) as invite_count FROM invites WHERE email = '{email}';
        """

        print("\n🔧 Fixing status...")
        mysql_cmd = f"mysql -u{env['MySQL_username']} -p'{env['MySQL_password']}' -h{env['MySQL_hostname']} -e \"{fix_sql}\""
        stdin, stdout, stderr = ssh.exec_command(mysql_cmd)

        output = stdout.read().decode()
        error = stderr.read().decode()

        if error and 'warning' not in error.lower():
            print(f"❌ Error: {error}")

        print("✅ Status fixed!")
        print(output)

        # Restart Ghost
        print("\n🔄 Restarting Ghost...")
        restart_cmd = "systemctl restart ghost_digitalalchemisten-de.service"
        stdin, stdout, stderr = ssh.exec_command(restart_cmd)
        stdout.channel.recv_exit_status()

        print("✅ Ghost restarted!")

        print("\n" + "="*60)
        print("✅ ALL DONE!")
        print("="*60)
        print(f"📧 User: {email}")
        print(f"🌐 Login URL: https://digitalalchemisten.de/ghost/")
        print(f"\n💡 Refresh the Staff page in Ghost Admin")
        print(f"💡 User should now appear under 'Editors' (not 'Invited')")
        print(f"💡 Login should work now!")

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

    if len(sys.argv) < 2:
        print("Usage: python fix_invited_status.py <email>")
        print("Example: python fix_invited_status.py user@example.com")
        sys.exit(1)

    email = sys.argv[1]
    fix_invited_status(email)
