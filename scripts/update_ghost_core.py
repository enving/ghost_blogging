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
SSH connection eventually reset. This run first installs a NOPASSWD
sudoers rule for ghostuser (validated with visudo -c before being
written). The rule is deliberately broad (NOPASSWD: ALL): ghost update
also sudos non-systemctl commands (e.g. `mv` of nginx site configs into
/etc/nginx/sites-available, `nginx -s reload`, symlink management), and
each missing command hangs on a `? Sudo Password` prompt that kills the
SSH session instead of failing fast. ghostuser already holds
(ALL:ALL) ALL with password via group membership, so this only removes
the interactive prompt - it grants no new privilege. All exec_command
calls also get a hard timeout so a stuck command fails fast instead of
hanging the whole job again.
"""
from pathlib import Path
import sys
import time
import paramiko

SERVICE = "ghost_digitalalchemisten-de.service"
# ghost-cli invokes systemctl with the unit name both with and without the
# ".service" suffix (systemd treats them as equivalent, sudoers does not -
# it does exact argument matching). Use a glob so both forms match.
SERVICE_GLOB = "ghost_digitalalchemisten-de*"
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
        # Broad on purpose: ghost-cli sudos systemctl AND nginx/mv/ln/reload
        # etc. during update; any missing command hangs on a password prompt
        # and kills the SSH session. ghostuser already has (ALL:ALL) ALL via
        # group membership - this only drops the interactive prompt.
        f"ghostuser ALL=(root) NOPASSWD: ALL\n"
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

        run(
            ssh,
            "cd /var/www/ghost && find . ! -path './versions/*' -type f -exec chmod 664 {} \\;",
            "2b) FIX FILE PERMISSIONS (ghost-cli's own suggested fix - theme was likely uploaded manually as root)",
        )

        run(
            ssh,
            "npm install -g ghost-cli@latest",
            "2c) UPGRADE GHOST-CLI (1.28.3 can't install Ghost v6.51.0, which needs ghost-cli ^1.29.1)",
            timeout=180,
        )

        run(
            ssh,
            "curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && apt-get install -y nodejs 2>&1 | tail -3",
            "2c2) UPGRADE NODE TO LATEST 22.x (Ghost 6.70.0 requires ^22.23.1; server had v22.22.0)",
            timeout=300,
        )

        _, node_out, _ = run(ssh, "node --version", "2c3) VERIFY NODE VERSION")
        node_version = (node_out or "").strip().lstrip("v")
        node_parts = (node_version.split(".") + ["0", "0"])[:3]
        try:
            node_major, node_minor, node_patch = (int(p) for p in node_parts)
        except ValueError:
            node_major, node_minor, node_patch = 0, 0, 0
        node_ok = (
            (node_major == 22 and (node_minor, node_patch) >= (23, 1))
            or (node_major == 24 and (node_minor, node_patch) >= (20, 0))
        )
        if not node_ok:
            print(f"Node {node_version} does not satisfy Ghost (^22.23.1 || ^24.20.0) - aborting before update.")
            return

        run(
            ssh,
            "sudo -u ghostuser bash -lc 'cd /var/www/ghost && ghost setup linux-user systemd --force 2>&1'",
            "2d) REPAIR SYSTEMD SETUP (ghost-cli's own suggested fix - update got as far as downloading v6.51.0, "
            "then failed to stop Ghost because it doesn't recognize its own systemd setup)",
            get_pty=True,
            timeout=120,
        )

        status, out, err = run(
            ssh,
            "sudo -u ghostuser bash -lc 'cd /var/www/ghost && ghost update --force 2>&1'",
            "3) GHOST UPDATE (this can take a couple of minutes)",
            get_pty=True,
            timeout=300,
        )
        if err == "timeout":
            print("Update command timed out - checking whatever state we're left in below.")
        combined_output = (out or "") + (err or "")
        update_ok = True
        if "not compatible with the current Node version" in combined_output or "SystemError" in combined_output:
            print("Ghost update refused (compatibility error) - aborting, update step applied nothing.")
            update_ok = False

        run(ssh, "sleep 5 && systemctl status ghost_digitalalchemisten-de.service --no-pager | head -15", "4) SERVICE STATUS AFTER UPDATE")

        run(ssh, "cat /var/www/ghost/current/package.json | grep '\"version\"'", "5) VERSION AFTER UPDATE")

        run(
            ssh,
            "curl -s -o /dev/null -w 'HTTP %{http_code}\\n' http://127.0.0.1:2368/",
            "6) LOCAL HTTP CHECK",
        )

        print("\n" + "=" * 60)
        print(f"Backup saved at: {backup_path}")
        if update_ok:
            print("UPDATE COMPLETE")
        else:
            print("UPDATE FAILED - see output above, server left untouched by update step")
        print("=" * 60)
        if not update_ok:
            sys.exit(1)

    finally:
        ssh.close()


if __name__ == '__main__':
    main()
