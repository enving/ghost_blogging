#!/usr/bin/env python3
"""
Read-only pre-update diagnostic for the Ghost VPS.

Collects Ghost/CLI/Node versions, service status, disk/RAM, theme listing,
local HTTP status, recent error logs, and backup recency over SSH.
Strictly READ-ONLY: no writes, no restarts, no config dumps.

Runs via GitHub Actions (secrets come from scripts/.env written by manage.yml):
    gh workflow run manage.yml -f script=ghost_preupdate_check.py --repo enving/ghost_blogging
"""
from pathlib import Path
import paramiko

COMMAND_TIMEOUT = 60


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


def run(ssh, cmd, label, timeout=COMMAND_TIMEOUT):
    print("\n" + "=" * 60)
    print(label)
    print("=" * 60)
    try:
        _, stdout, stderr = ssh.exec_command(cmd, timeout=timeout)
        stdout.channel.settimeout(timeout)
        out = stdout.read().decode(errors="replace")
        err = stderr.read().decode(errors="replace")
    except Exception as e:
        print(f"[ERROR] {type(e).__name__}: {e}")
        return None
    print(out[:3000])
    if err.strip():
        print(f"[stderr] {err[:500]}")
    return out


def main():
    print("Connecting to VPS (host redacted, user={})...".format(env.get('VPS_USER', '?')))
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(
            hostname=env['VPS_IP'],
            username=env['VPS_USER'],
            password=env['VPS_PW'],
            timeout=15, banner_timeout=15, auth_timeout=15,
        )
        print("SSH_CONNECTED")

        run(ssh, "cat /var/www/ghost/current/package.json 2>&1 | grep '\"version\"'",
            "1) GHOST CORE VERSION")
        run(ssh, "ghost --version 2>&1 | head -5; npm list -g ghost-cli 2>&1 | head -5",
            "2) GHOST-CLI VERSION")
        run(ssh, "node --version 2>&1; npm --version 2>&1",
            "3) NODE / NPM VERSION")
        run(ssh, "systemctl is-active ghost_digitalalchemisten-de.service 2>&1",
            "4) SERVICE ACTIVE STATE")
        run(ssh, "systemctl status ghost_digitalalchemisten-de.service --no-pager 2>&1 | head -15",
            "5) SERVICE STATUS")
        run(ssh, "df -h / /var/www/ghost 2>&1",
            "6) DISK SPACE")
        run(ssh, "free -h 2>&1; uptime 2>&1",
            "7) RAM / UPTIME")
        run(ssh, "ls -la /var/www/ghost/content/themes/ 2>&1 | head -20",
            "8) INSTALLED THEMES")
        run(ssh, "curl -s -o /dev/null -w 'HTTP %{http_code}\\n' http://127.0.0.1:2368/ 2>&1",
            "9) LOCAL HTTP CHECK")
        run(ssh, "journalctl -u ghost_digitalalchemisten-de.service -n 20 --no-pager -p err 2>&1 | head -25",
            "10) RECENT ERROR LOGS")
        run(ssh, "ls -lh /home/ghostuser/backups 2>&1 | head -10; "
                 "ls -lh /var/www/ghost/content/data/pre_update_backup* 2>&1 | head -10",
            "11) BACKUP RECENCY")
        run(ssh, "docker ps --format '{{.Names}} {{.Status}}' 2>&1 | head -10; "
                 "swapon --show 2>&1 | head -5",
            "12) N8N COEXISTENCE / SWAP")
        run(ssh, "ps aux 2>&1 | grep -iE 'ghost (update|install|setup)|ghost-cli' | grep -v grep | head -10; "
                 "ls /var/www/ghost/versions/ 2>&1 | head -10",
            "13) STRAY UPDATE PROCESSES / INSTALLED VERSIONS")
        run(ssh, "cat /var/www/ghost/.ghost-cli 2>&1 | head -30; echo '---GLOBAL CONFIG---'; "
                 "cat /home/ghostuser/.ghost/config 2>&1 | head -30",
            "14) GHOST-CLI INSTANCE STATE (.ghost-cli + global config)")
        run(ssh, "id ghost 2>&1; id ghostuser 2>&1; stat -c 'content owner: %U(%u)' /var/www/ghost/content 2>&1; "
                 "grep -E '^(User|Group)=|WorkingDirectory=' /lib/systemd/system/ghost_digitalalchemisten-de.service 2>&1",
            "14b) SYSTEMD PRECHECK INPUTS (ghost user vs content owner vs unit User)")
        run(ssh, "sudo -u ghostuser bash -lc 'cd /var/www/ghost && ghost doctor 2>&1' | head -40",
            "15) GHOST DOCTOR")
        run(ssh, "sudo -u ghostuser bash -lc 'cd /var/www/ghost && ghost ls 2>&1' | head -15",
            "16) GHOST LS")

        print("\n" + "=" * 60)
        print("CHECK DONE (READ-ONLY, no changes made)")
        print("=" * 60)
    finally:
        ssh.close()


if __name__ == '__main__':
    main()
