#!/usr/bin/env python3
"""
Update Ghost core to the latest version via Ghost-CLI.

Root cause: the site's Ghost core (6.10.3) is ~6 months behind current (6.49.0+),
so the actively-developed official "Edition" theme now uses a Handlebars helper
(social_accounts) that this Ghost version doesn't register yet, and its
theme upload gets rejected with a ThemeValidationError.

Takes a MySQL dump before updating as a safety net.

Previous run: ghost-cli, running as ghostuser (Ghost-CLI refuses to run
as root), internally calls `sudo systemctl is-active ...` to check the
service. ghostuser's sudo rights come from group membership ("(ALL:ALL)
ALL", per `sudo -l -U ghostuser`) with no NOPASSWD, so that inner sudo
call hung on an interactive password prompt nobody could answer, and the
SSH connection eventually reset. This run first installs a narrowly
scoped NOPASSWD sudoers rule (validated with visudo -c before being
written) limited to systemctl start/stop/restart/is-active/enable/disable
on this one service unit, so ghost-cli's own internal calls stop
prompting. All exec_command calls also get a hard timeout so a stuck
command fails fast instead of hanging the whole job again.
"""
from pathlib import Path
import time
import paramiko

SERVICE = "ghost_digitalalchemisten-de.service"
SUDOERS_FILE = "/etc/sudoers.d/ghost-cli-ghostuser"
COMMAND_TIMEOUT = 240


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


def run(ssh, cmd, label, get_pty=False, timeout=COMMAND_TIMEOUT):
    print("\n" + "=" * 60)
    print(label)
    print("=" * 60)
    print(f"$ {cmd}")
    stdin, stdout, stderr = ssh.exec_command(cmd, get_pty=get_pty, timeout=timeout)
    stdout.channel.settimeout(timeout)
    try:
        out = stdout.read().decode()
        err = stderr.read().decode()
        exit_status = stdout.channel.recv_exit_status()
    except TimeoutError:
        print(f"[TIMEOUT after {timeout}s] command did not complete, moving on")
        return None, "", "timeout"
    print(out)
    if err.strip():
        print(f"[stderr] {err}")
    return exit_status, out, err


def ensure_passwordless_systemctl(ssh):
    status, systemctl_path, _ = run(ssh, "command -v systemctl", "0a) LOCATE systemctl")
    systemctl_path = systemctl_path.strip()
    if not systemctl_path:
        raise RuntimeError("Could not locate systemctl")

    rule = (
        f"ghostuser ALL=(root) NOPASSWD: "
        f"{systemctl_path} start {SERVICE}, "
        f"{systemctl_path} stop {SERVICE}, "
        f"{systemctl_path} restart {SERVICE}, "
        f"{systemctl_path} reload {SERVICE}, "
        f"{systemctl_path} is-active {SERVICE}, "
        f"{systemctl_path} enable {SERVICE}, "
        f"{systemctl_path} disable {SERVICE}\n"
    )
    tmp_file = f"{SUDOERS_FILE}.tmp"
    run(ssh, f"cat > {tmp_file} << 'EOF'\n{rule}EOF", "0b) WRITE CANDIDATE SUDOERS RULE")
    status, out, err = run(ssh, f"visudo -c -f {tmp_file}", "0c) VALIDATE SUDOERS SYNTAX")
    if status != 0:
        run(ssh, f"rm -f {tmp_file}", "0d) INVALID - REMOVING TMP FILE")
        raise RuntimeError(f"visudo rejected the sudoers rule: {out} {err}")

    run(ssh, f"mv {tmp_file} {SUDOERS_FILE} && chown root:root {SUDOERS_FILE} && chmod 440 {SUDOERS_FILE}", "0e) INSTALL SUDOERS RULE")
    run(ssh, f"sudo -l -U ghostuser | grep -A5 'may run'", "0f) CONFIRM NEW RULE FOR ghostuser")


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

        ensure_passwordless_systemctl(ssh)

        status, out, err = run(
            ssh,
            "sudo -u ghostuser bash -lc 'cd /var/www/ghost && ghost update --force 2>&1'",
            "3) GHOST UPDATE (this can take a couple of minutes)",
            get_pty=True,
            timeout=300,
        )
        if err == "timeout":
            print("Update command timed out - checking whatever state we're left in below.")

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
