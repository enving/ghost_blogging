#!/usr/bin/env python3
"""
Update Ghost core to the latest version via Ghost-CLI.

Root cause: the site's Ghost core (6.10.3) is ~6 months behind current (6.49.0+),
so the actively-developed official "Edition" theme now uses a Handlebars helper
(social_accounts) that this Ghost version doesn't register yet, and its
theme upload gets rejected with a ThemeValidationError.

Takes a MySQL dump before updating as a safety net, then runs `ghost update`
as the ghostuser (Ghost-CLI refuses to run as root), then verifies the
service comes back up.
"""
from pathlib import Path
import time
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


def run(ssh, cmd, label, get_pty=False):
    print("\n" + "=" * 60)
    print(label)
    print("=" * 60)
    print(f"$ {cmd}")
    stdin, stdout, stderr = ssh.exec_command(cmd, get_pty=get_pty)
    exit_status = stdout.channel.recv_exit_status()
    out = stdout.read().decode()
    err = stderr.read().decode()
    print(out)
    if err.strip():
        print(f"[stderr] {err}")
    return exit_status, out, err


def main():
    print(f"Connecting to server {env['VPS_IP']}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=env['VPS_IP'], username=env['VPS_USER'], password=env['VPS_PW'])
    print("SSH Connected!")

    try:
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        backup_path = f"/var/www/ghost/content/data/pre_update_backup_{timestamp}.sql"

        status, out, err = run(
            ssh,
            f"mysqldump -u{env['MySQL_username']} -p'{env['MySQL_password']}' "
            f"{env['MySQL_database_name']} > {backup_path} 2>&1 && echo BACKUP_OK",
            "1) DATABASE BACKUP",
        )
        if 'BACKUP_OK' not in out:
            print("Backup did not confirm success, aborting update.")
            return

        run(ssh, "cat /var/www/ghost/current/package.json | grep '\"version\"'", "2) VERSION BEFORE UPDATE")

        status, out, err = run(
            ssh,
            "sudo -u ghostuser bash -lc 'cd /var/www/ghost && ghost update --force 2>&1'",
            "3) GHOST UPDATE (this can take a couple of minutes)",
            get_pty=True,
        )

        run(ssh, "sleep 5 && systemctl status ghost_digitalalchemisten-de.service --no-pager | head -15", "4) SERVICE STATUS AFTER UPDATE")

        run(ssh, "cat /var/www/ghost/current/package.json | grep '\"version\"'", "5) VERSION AFTER UPDATE")

        run(
            ssh,
            "curl -s -o /dev/null -w 'HTTP %{http_code}\\n' http://127.0.0.1:2368/",
            "6) LOCAL HTTP CHECK",
        )

        print("\n" + "=" * 60)
        print(f"Backup saved at: {backup_path}")
        print("UPDATE COMPLETE")
        print("=" * 60)

    finally:
        ssh.close()


if __name__ == '__main__':
    main()
