#!/usr/bin/env python3
"""
Fix Nginx configuration for foerderwissensgraph.digitalalchemisten.de
Uses port 8443 instead of 8080 to avoid redirect loop
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

# Fixed config - use 8443 with proper SSL passthrough
NGINX_CONFIG = '''# Nginx configuration for foerderwissensgraph.digitalalchemisten.de
# Fixed: Use port 8443 to avoid redirect loop

server {
    listen 80;
    server_name foerderwissensgraph.digitalalchemisten.de;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name foerderwissensgraph.digitalalchemisten.de;

    # Use existing Let's Encrypt certificates from Ghost
    ssl_certificate /etc/letsencrypt/live/digitalalchemisten.de/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/digitalalchemisten.de/privkey.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;

    location / {
        # Connect to container's HTTPS port to avoid redirect loop
        proxy_pass https://127.0.0.1:8443;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Don't verify container's self-signed cert
        proxy_ssl_verify off;
        
        # Timeouts for long LLM responses
        proxy_read_timeout 300;
        proxy_connect_timeout 300;
        proxy_send_timeout 300;
    }
}
'''

def run_cmd(ssh, cmd, description=""):
    if description:
        print(f"\\n🔄 {description}...")
    print(f"   $ {cmd}")
    stdin, stdout, stderr = ssh.exec_command(cmd)
    exit_status = stdout.channel.recv_exit_status()
    out = stdout.read().decode().strip()
    err = stderr.read().decode().strip()
    if out:
        print(f"   {out}")
    if err and exit_status != 0:
        print(f"   ⚠️  {err}")
    return out, err, exit_status

def fix_nginx():
    print(f"🔌 Connecting to VPS {env['VPS_IP']}...")
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(
            hostname=env['VPS_IP'],
            username=env['VPS_USER'],
            password=env['VPS_PW']
        )
        print("✅ SSH Connected!")
        
        # Check what ports are actually listening
        run_cmd(ssh, "ss -tlpn | grep -E ':(8080|8443)'", "Checking container ports")
        
        # Check if 8443 responds
        run_cmd(ssh, "curl -k -s -o /dev/null -w '%{http_code}' https://127.0.0.1:8443/ 2>/dev/null || echo 'Port 8443 not responding'", "Testing port 8443")
        
        # Update the config
        print("\\n📝 Updating Nginx configuration to use port 8443...")
        
        # Write config via cat heredoc
        cmd = f'''cat > /etc/nginx/sites-available/foerderwissensgraph.conf << 'ENDCONF'
{NGINX_CONFIG}
ENDCONF'''
        run_cmd(ssh, cmd, "Writing new config")
        
        # Test nginx
        out, err, status = run_cmd(ssh, "nginx -t 2>&1", "Testing Nginx configuration")
        
        if status != 0:
            print("\\n❌ Nginx config test failed!")
            return False
        
        # Reload nginx
        run_cmd(ssh, "systemctl reload nginx", "Reloading Nginx")
        
        # Test the result
        run_cmd(ssh, "curl -k -s -o /dev/null -w '%{http_code}' https://foerderwissensgraph.digitalalchemisten.de/ 2>/dev/null || echo 'Still having issues'", "Testing the site")
        
        print("\\n✅ Configuration updated!")
        print("🌐 Try https://foerderwissensgraph.digitalalchemisten.de now")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        ssh.close()

if __name__ == '__main__':
    fix_nginx()
