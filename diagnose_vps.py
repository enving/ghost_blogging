#!/usr/bin/env python3
"""
Diagnose VPS status for Ghost and Nginx
"""
from pathlib import Path
import paramiko
import sys

# Load credentials from .env
def load_env():
    env_vars = {}
    env_path = Path(__file__).parent / '.env'
    try:
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key] = value
    except FileNotFoundError:
        print("Error: .env file not found")
        sys.exit(1)
    return env_vars

env = load_env()

def run_command(ssh, cmd, description):
    print(f"\n--- {description} ---")
    print(f"Command: {cmd}")
    stdin, stdout, stderr = ssh.exec_command(cmd)
    out = stdout.read().decode().strip()
    err = stderr.read().decode().strip()
    if out:
        print(f"STDOUT:\n{out}")
    if err:
        print(f"STDERR:\n{err}")

def diagnose():
    print(f"Connecting to server {env.get('VPS_IP')}...")
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(
            hostname=env['VPS_IP'],
            username=env['VPS_USER'],
            password=env['VPS_PW']
        )
        print("✅ SSH Connected!")
        
        # 1. Check Nginx Config Syntax
        run_command(ssh, "sudo nginx -t", "Checking Nginx Configuration Syntax")

        # 2. List Nginx Sites
        run_command(ssh, "ls -l /etc/nginx/sites-enabled/", "Listing Enabled Nginx Sites")

        # 3. Check Ghost Services
        run_command(ssh, "systemctl list-units --type=service | grep ghost", "Checking Ghost Services Status")
        
        # 4. Check Port Usage (80/443/2368)
        # Using ss since netstat might not be installed
        run_command(ssh, "sudo ss -tulpn | grep -E ':(80|443|2368)'", "Checking Ports 80, 443, 2368")

        # 5. Check Content of Nginx Sites (to spot conflicts)
        run_command(ssh, "cat /etc/nginx/sites-enabled/* | grep server_name", "Checking server_name in active sites")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        ssh.close()

if __name__ == '__main__':
    diagnose()
