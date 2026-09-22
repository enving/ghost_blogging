#!/usr/bin/env python3
"""
Einmalig: N8N_ENCRYPTION_KEY aus /opt/n8n/.env verschlüsselt ausgeben (RSA-OAEP-SHA256).
Im öffentlichen Log steht nur Chiffretext; entschlüsseln kann nur der Besitzer des privaten Schlüssels.
Nach Gebrauch aus dem Repo entfernen.
"""
from pathlib import Path
import paramiko

PUBKEY = """
-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEA7tb67M6Z6KDJHit2ibSD
zI262DF9F8JY9hM2k97n4bD+nS+RZ6KHh8lCwWVGbvAe80+gYIGnjK3xmoOqp1He
kMzgS8AZmp8HfJpNTr9IYK5TedHk/kJ/eN5xSztI2/nKVHKdYmnYuTPV6H0kdAA8
VR2sIUkXvi8hjj3/fRZ7te3l+HHJgJY9P4NhSCbJi9bCxLjl2VsjqFbpDLpNRlDg
v1A+F34yswgodOGWpwimG7DqqknliuVWmFf+4nEDnBS1D+xn0LY4ZQORGfb87Knx
9Kf/ksciSZ5Ns3BY9RrQmo7eHLJa36jLVVLZV1lgitcjrZz0jxIFacFJ+ITlyEgx
+bsLZEz+BOc/J8SubZ5E2KGMXniXFk3yLDpWwAh/bFrOFn3RrtxK49waC4Al6jKc
v9Gkiwzkyc/LLi+Rc9zNV/O12OlFKoxJcB9RypxMhoCB4f7Ukh0JJWN3a2aXZ5k2
1+U2wyrtdNVgsN5eSEsenTrwiXTX+jfBxnDa3ysi+Onj8RGUTWCRj7AfAoiem3/R
Srshx+OSiP0H7n3r3KByDDTOylu87/083oqj8ii7whBd2rvTZxE2Nep/KdFBfTyO
Ypq2Tx+/KLHc1p8RKQL337XrpdD0AbB88ELQj2458xy06EBXTl458yVeKbb0v7o+
siOksHuW3kg5JAG+uA2O42sCAwEAAQ==
-----END PUBLIC KEY-----
"""

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
cmd = (
    't=$(mktemp) && cat > "$t" && '
    'grep "^N8N_ENCRYPTION_KEY=" /opt/n8n/.env | cut -d= -f2- | tr -d "\\n" | '
    'openssl pkeyutl -encrypt -pubin -inkey "$t" '
    '-pkeyopt rsa_padding_mode:oaep -pkeyopt rsa_oaep_md:sha256 | base64 -w0; '
    'rc=$?; rm -f "$t"; exit $rc'
)
stdin, stdout, stderr = ssh.exec_command(cmd)
stdin.write(PUBKEY.strip() + '\n')
stdin.channel.shutdown_write()
out = stdout.read().decode().strip()
code = stdout.channel.recv_exit_status()
ssh.close()
print("CIPHERTEXT_BEGIN")
print(out)
print("CIPHERTEXT_END")
raise SystemExit(code)
