#!/usr/bin/env python3
"""
Diagnose theme rendering issue: unstyled page + "undefined" text in footer.
Read-only checks against the VPS and the live site.
"""
from pathlib import Path
import paramiko

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

def run(ssh, cmd, label):
    print("\n" + "=" * 60)
    print(label)
    print("=" * 60)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    out = stdout.read().decode()
    err = stderr.read().decode()
    print(out)
    if err.strip():
        print(f"[stderr] {err}")
    return out

def diagnose():
    print(f"Connecting to server {env['VPS_IP']}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(hostname=env['VPS_IP'], username=env['VPS_USER'], password=env['VPS_PW'])
        print("SSH Connected!")

        run(ssh, "ls -la /var/www/ghost/content/themes/", "1) INSTALLED THEMES")

        run(
            ssh,
            "mysql -u" + env['MySQL_username'] + " -p'" + env['MySQL_password'] + "' -e "
            "\"SELECT \\`key\\`, value FROM " + env['MySQL_database_name'] + ".settings WHERE \\`key\\` = 'active_theme';\" 2>&1 | grep -v Warning",
            "2) ACTIVE THEME (from DB)",
        )

        run(ssh, "curl -s -o /dev/null -w 'HTTP %{http_code}\\n' http://127.0.0.1:2368/", "3) LOCAL GHOST HTTP STATUS")

        html = run(ssh, "curl -s http://127.0.0.1:2368/", "4) HOMEPAGE HTML (local, first 4000 chars)")
        print("\n--- Stylesheet <link> tags found ---")
        for line in html.splitlines():
            if 'stylesheet' in line.lower() or '.css' in line.lower():
                print(line.strip())

        print("\n--- Lines containing 'undefined' ---")
        for line in html.splitlines():
            if 'undefined' in line.lower():
                print(line.strip())

        run(ssh, "systemctl status ghost_digitalalchemisten-de.service --no-pager | head -20", "5) GHOST SERVICE STATUS")

        run(ssh, "journalctl -u ghost_digitalalchemisten-de.service -n 30 --no-pager", "6) RECENT GHOST LOGS")

        print("\n" + "=" * 60)
        print("DIAGNOSIS COMPLETE")
        print("=" * 60)

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

    finally:
        ssh.close()

if __name__ == '__main__':
    diagnose()
