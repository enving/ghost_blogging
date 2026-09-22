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
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAr5Pk9/Hpm5sex2+imGL1
gL7kjWx4FZ/SHNVtwTYtKTDFxallvXoN6l3ovG1CNB5/EhI/BbX21iCcETTom5uN
EGip84xXphB209ZnHwi2lzPZ+loLsvVSpBG/w6vIZ9gnr2DvpKs2cGG28PS2eILA
uyy6Qy/srmPdYu5EyJqwyYSIfqi6Waa2vbUnScZAXUe0ku2cleXMM7pa0owOaX/i
b3H0DrypPhLjV/j/aMAojZWRghesoX3BjEPoTHAOeWVb1Rrv9g2FmeZEQeOi/wE2
dj27DUvrdTijYc0ARqvn+PlbFLegNkYPnumg+3k4jw5dx/b+ajAkxA7w8ImWF7YZ
TLooma0gYQAJ+nqt91HdK5x9UZ4kwxmHUCxrGDDK6tnsMpC0ndIqTI29GE9Y62Zz
g3Jp0NAnLBTTr3gn8DfFCDgdoeHdlwRyy4NCazTsy294BenIGDjOSeSqV4OUJ1s6
eATpX7f/WRNFQqXkx2SiHNkGheaxBRCSGHRMe2SL3UPSYw/2t+bvQgDUVEgC0JOK
dsxAuu2qCyit1NxdrBhd4DPjF5Q+iqNDU/BNdIBzVCue1SgxJTgAfl8QBnozYsZQ
+33AtqMVqJKzirh9XJspOSSpJqfsfGfpCr526ZXg3pvyL2000+WRSOkcgiuZ6z+k
pHoUCUs419iD3KyABxSuMRMCAwEAAQ==
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
