#!/usr/bin/env python3
"""
n8n auf dem VPS einrichten/aktualisieren: lädt infra/n8n/ hoch und führt setup.sh aus.
Läuft über .github/workflows/manage.yml (script=setup_n8n.py).
Achtung: Actions-Logs dieses Repos sind öffentlich – setup.sh gibt keine Secrets aus.
"""
from pathlib import Path
import sys
import paramiko

DOMAIN = "n8n.digitalalchemisten.de"
REMOTE_DIR = "/root/n8n-setup"
LOCAL_DIR = Path(__file__).parent.parent / "infra" / "n8n"
FILES = ["setup.sh", "docker-compose.yml", "nginx-n8n.conf"]

def load_env():
    env_vars = {}
    with open(Path(__file__).parent / '.env') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key] = value
    return env_vars

env = load_env()
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=env['VPS_IP'], username=env['VPS_USER'], password=env['VPS_PW'])
print("✅ SSH verbunden")

ssh.exec_command(f"mkdir -p {REMOTE_DIR}")[1].channel.recv_exit_status()
sftp = ssh.open_sftp()
for name in FILES:
    sftp.put(str(LOCAL_DIR / name), f"{REMOTE_DIR}/{name}")
sftp.close()
print(f"📦 {len(FILES)} Dateien hochgeladen")

_, stdout, _ = ssh.exec_command(f"bash {REMOTE_DIR}/setup.sh {DOMAIN} 2>&1", get_pty=False)
for line in iter(stdout.readline, ""):
    print(line, end="", flush=True)
code = stdout.channel.recv_exit_status()
ssh.close()
print(f"\nsetup.sh exit {code}")
sys.exit(code)
