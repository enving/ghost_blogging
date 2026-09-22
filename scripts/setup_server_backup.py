#!/usr/bin/env python3
"""
Verschlüsseltes Server-Backup nach Google Drive einrichten (rclone) – über manage.yml.
  script=setup_server_backup.py         einrichten, n8n-Stände hochladen, Status zeigen
  SERVER_BACKUP_ACTION=system           zusätzlich ersten Voll-Backup-Lauf im Hintergrund starten
  SERVER_BACKUP_ACTION=status           nur Status/Log anzeigen
Secrets (GitHub): RCLONE_DRIVE_TOKEN (JSON), RCLONE_CRYPT_PASS (rclone-obscured).
Achtung: Actions-Logs sind öffentlich – rclone.conf wird per SFTP geschrieben, nie ausgegeben.
"""
from pathlib import Path
import io
import os
import sys
import paramiko

LOCAL = Path(__file__).parent.parent / "infra" / "server"
REMOTE = "/opt/server-backup"
CRON = (
    "0 4 * * * root /opt/server-backup/gdrive-backup.sh n8n >> /var/log/server-backup.log 2>&1\n"
    "30 4 * * 0 root /opt/server-backup/gdrive-backup.sh system >> /var/log/server-backup.log 2>&1\n"
)

def load_env():
    env_vars = {}
    with open(Path(__file__).parent / '.env') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key] = value
    return env_vars

def run(ssh, cmd):
    _, stdout, _ = ssh.exec_command(cmd + " 2>&1")
    for line in iter(stdout.readline, ""):
        print(line, end="", flush=True)
    return stdout.channel.recv_exit_status()

env = load_env()
action = os.environ.get("SERVER_BACKUP_ACTION") or "setup"
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=env['VPS_IP'], username=env['VPS_USER'], password=env['VPS_PW'])
print("✅ SSH verbunden")

if action == "status":
    code = run(ssh, "echo '== System'; . /etc/os-release; echo \"$PRETTY_NAME, Kernel $(uname -r)\"; "
                    "free -h | sed -n 1,3p; df -h / | tail -1; "
                    "systemctl is-active nginx mysql docker 'ghost_*' 2>/dev/null | paste -sd' ' -; "
                    f"echo '== Drive'; {REMOTE}/gdrive-backup.sh status; "
                    "echo '== Log'; tail -n 20 /var/log/server-backup.log")
    ssh.close(); sys.exit(code)

token = os.environ.get("RCLONE_DRIVE_TOKEN", "").strip()
crypt = os.environ.get("RCLONE_CRYPT_PASS", "").strip()
if not token or not crypt:
    print("!! Secrets RCLONE_DRIVE_TOKEN / RCLONE_CRYPT_PASS fehlen"); sys.exit(1)

print("== rclone")
if run(ssh, "command -v rclone >/dev/null || (apt-get update -qq && apt-get install -y -qq rclone >/dev/null); rclone version | head -1") != 0:
    sys.exit(1)

conf = (
    "[gdrive]\ntype = drive\nscope = drive.file\n"
    f"token = {token}\n\n"
    "[gcrypt]\ntype = crypt\nremote = gdrive:vps-backup\n"
    "filename_encryption = standard\ndirectory_name_encryption = true\n"
    f"password = {crypt}\n"
)
run(ssh, f"mkdir -p /root/.config/rclone {REMOTE} && chmod 700 /root/.config/rclone {REMOTE}")
sftp = ssh.open_sftp()
# Bestehende Konfig nicht überschreiben: rclone erneuert das Token selbst und schreibt es zurück.
try:
    sftp.stat("/root/.config/rclone/rclone.conf")
    print("   rclone.conf vorhanden – bleibt (Token wird von rclone gepflegt)")
except IOError:
    with sftp.open("/root/.config/rclone/rclone.conf", "w") as f:
        f.write(conf)
    sftp.chmod("/root/.config/rclone/rclone.conf", 0o600)
    print("   rclone.conf geschrieben (600)")
sftp.put(str(LOCAL / "gdrive-backup.sh"), f"{REMOTE}/gdrive-backup.sh")
sftp.chmod(f"{REMOTE}/gdrive-backup.sh", 0o700)
with sftp.open("/etc/cron.d/server-backup", "w") as f:
    f.write(CRON)
sftp.chmod("/etc/cron.d/server-backup", 0o644)
sftp.close()
print("   Cron: täglich 04:00 n8n, sonntags 04:30 Voll-Backup")

print("== Verbindung zu Google Drive")
code = run(ssh, "RCLONE_CONFIG=/root/.config/rclone/rclone.conf rclone mkdir gcrypt:system && "
                f"{REMOTE}/gdrive-backup.sh n8n && {REMOTE}/gdrive-backup.sh status")

if code == 0 and action == "system":
    print("== Erster Voll-Backup-Lauf im Hintergrund gestartet (Log: /var/log/server-backup.log)")
    run(ssh, f"setsid nohup {REMOTE}/gdrive-backup.sh system >> /var/log/server-backup.log 2>&1 < /dev/null &")

ssh.close()
print(f"\nexit {code}")
sys.exit(code)
