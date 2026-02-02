#!/usr/bin/env python3
"""
Setup Nginx configuration for foerderwissensgraph.digitalalchemisten.de
"""
from pathlib import Path
import paramiko

# Load credentials from .env
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

NGINX_CONFIG = '''# Nginx configuration for foerderwissensgraph.digitalalchemisten.de
# Created automatically

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
    
    # SSL settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts for long LLM responses
        proxy_read_timeout 300;
        proxy_connect_timeout 300;
        proxy_send_timeout 300;
    }
}
'''

def run_cmd(ssh, cmd, description=""):
    """Run command and return output"""
    if description:
        print(f"\n🔄 {description}...")
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

def setup_nginx():
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
        
        # Step 1: Check existing nginx sites
        run_cmd(ssh, "ls -la /etc/nginx/sites-enabled/", "Checking existing Nginx sites")
        
        # Step 2: Check if SSL certs exist
        out, err, status = run_cmd(ssh, "ls -la /etc/letsencrypt/live/ 2>/dev/null || echo 'No letsencrypt certs'", "Checking SSL certificates")
        
        # Step 3: Check what ports the containers are using
        run_cmd(ssh, "docker ps --format '{{.Names}}: {{.Ports}}' 2>/dev/null || echo 'Docker not running or no containers'", "Checking Docker containers")
        
        # Step 4: Check if port 8080 is listening
        run_cmd(ssh, "ss -tlpn | grep -E ':(8080|8443)'", "Checking if ports 8080/8443 are listening")
        
        # Step 5: Write the nginx config
        print("\n📝 Writing Nginx configuration...")
        # Escape single quotes in config
        escaped_config = NGINX_CONFIG.replace("'", "'\"'\"'")
        cmd = f"echo '{escaped_config}' > /etc/nginx/sites-available/foerderwissensgraph.conf"
        run_cmd(ssh, cmd, "Creating nginx config file")
        
        # Step 6: Create symlink
        run_cmd(ssh, "ln -sf /etc/nginx/sites-available/foerderwissensgraph.conf /etc/nginx/sites-enabled/foerderwissensgraph.conf", "Creating symlink")
        
        # Step 7: Test nginx config
        out, err, status = run_cmd(ssh, "nginx -t 2>&1", "Testing Nginx configuration")
        
        if status != 0:
            print("\n❌ Nginx config test failed! Checking for certificate issues...")
            # Try alternative cert paths
            run_cmd(ssh, "find /etc/letsencrypt -name '*.pem' 2>/dev/null | head -10", "Looking for SSL certificates")
            run_cmd(ssh, "find /etc/nginx -name '*.crt' -o -name '*.pem' 2>/dev/null | head -10", "Looking in nginx dir")
            print("\n⚠️  You may need to adjust the SSL certificate paths manually.")
            return False
        
        # Step 8: Reload nginx
        run_cmd(ssh, "systemctl reload nginx", "Reloading Nginx")
        
        # Step 9: Verify
        run_cmd(ssh, "cat /etc/nginx/sites-enabled/* | grep server_name", "Verifying all server_names")
        
        print("\n✅ Nginx configuration complete!")
        print("🌐 foerderwissensgraph.digitalalchemisten.de should now work!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        ssh.close()

if __name__ == '__main__':
    setup_nginx()
