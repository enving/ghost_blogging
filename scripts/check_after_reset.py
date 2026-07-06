#!/usr/bin/env python3
"""
Read-only sanity check after the update_ghost_core.py run got its SSH
connection reset while ghost-cli was waiting on a sudo password prompt
(for its internal `sudo systemctl is-active ...` pre-check). Confirms
Ghost is still serving at the old version and inspects why that sudo
call needed a password, so we don't blindly retry into the same hang.
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
    print(f"$ {cmd}")
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=20)
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
    ssh.connect(hostname=env['VPS_IP'], username=env['VPS_USER'], password=env['VPS_PW'], timeout=20)
    print("SSH Connected!")

    try:
        run(ssh, "systemctl status ghost_digitalalchemisten-de.service --no-pager | head -10", "1) GHOST SERVICE STATUS")
        run(ssh, "cat /var/www/ghost/current/package.json | grep '\"version\"'", "2) CURRENT GHOST VERSION")
        run(ssh, "curl -s -o /dev/null -w 'HTTP %{http_code}\\n' http://127.0.0.1:2368/", "3) LOCAL HTTP CHECK")
        run(ssh, "ls -la /etc/sudoers.d/", "4) SUDOERS.D FILES")
        run(ssh, "grep -r ghostuser /etc/sudoers.d/ /etc/sudoers 2>/dev/null", "5) ghostuser SUDO RULES")
        run(ssh, "sudo -l -U ghostuser 2>&1", "6) SUDO -l -U ghostuser (privileges list)")
        run(ssh, "ls -la /var/www/ghost/content/data/pre_update_backup_*.sql", "7) BACKUP FILE FROM PREVIOUS RUN")
    finally:
        ssh.close()


if __name__ == '__main__':
    main()
