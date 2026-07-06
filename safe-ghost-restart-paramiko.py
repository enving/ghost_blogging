#!/usr/bin/env python3
"""
Safe Ghost Restart Script using Paramiko
Performs a complete restart of Ghost service and clears Nginx cache
"""
import os
import sys
import paramiko
import time

def get_github_secret(secret_name):
    """Get secret from environment variable (set by GitHub Actions)"""
    return os.environ.get(secret_name)

def safe_ghost_restart():
    """Safely restart Ghost and clear Nginx cache"""
    
    # Get credentials from GitHub Secrets
    vps_ip = get_github_secret('VPS_IP')
    vps_user = get_github_secret('VPS_USER')
    vps_pw = get_github_secret('VPS_PW')
    
    print(f"Debug - VPS_IP: '{vps_ip}'")
    print(f"Debug - VPS_USER: '{vps_user}'")
    print(f"Debug - VPS_PW: '{'***' if vps_pw else 'None'}'")
    
    if not vps_ip or not vps_user or not vps_pw:
        print("❌ Missing VPS credentials from GitHub Secrets")
        return False
    
    print(f"🔌 Connecting to VPS {vps_ip}...")
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # Connect to VPS
        ssh.connect(
            hostname=vps_ip,
            username=vps_user,
            password=vps_pw
        )
        
        print("✅ SSH Connected!")
        
        # 1. Check current Ghost status
        print("\n1️⃣ Checking current Ghost status...")
        stdin, stdout, stderr = ssh.exec_command("systemctl status ghost_digitalalchemisten-de.service --no-pager")
        status_output = stdout.read().decode()
        print("Ghost Status:", status_output[:200] if status_output else "No output")
        
        # 2. Stop Ghost
        print("\n2️⃣ Stopping Ghost service...")
        stdin, stdout, stderr = ssh.exec_command("sudo systemctl stop ghost_digitalalchemisten-de.service")
        stop_output = stdout.read().decode()
        print("Stop Result:", stop_output if stop_output else "Success")
        
        # Wait a bit
        time.sleep(5)
        
        # 3. Clear Nginx cache
        print("\n3️⃣ Clearing Nginx cache...")
        stdin, stdout, stderr = ssh.exec_command("sudo nginx -t && sudo systemctl reload nginx")
        nginx_output = stdout.read().decode()
        print("Nginx Result:", nginx_output if nginx_output else "Success")
        
        # 4. Start Ghost
        print("\n4️⃣ Starting Ghost service...")
        stdin, stdout, stderr = ssh.exec_command("sudo systemctl start ghost_digitalalchemisten-de.service")
        start_output = stdout.read().decode()
        print("Start Result:", start_output if start_output else "Success")
        
        # Wait for Ghost to fully start
        time.sleep(10)
        
        # 5. Verify Ghost is running
        print("\n5️⃣ Verifying Ghost is running...")
        stdin, stdout, stderr = ssh.exec_command("systemctl is-active ghost_digitalalchemisten-de.service")
        verify_output = stdout.read().decode()
        
        if "active" in verify_output.lower():
            print("✅ Ghost is running!")
            
            # 6. Check CSS availability
            print("\n6️⃣ Checking CSS availability...")
            time.sleep(5)  # Wait for assets to regenerate
            
            # Get current CSS version
            import subprocess
            html_result = subprocess.run(
                ["curl", "-s", "https://digitalalchemisten.de/"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            import re
            css_match = re.search(r'href="/assets/built/screen\.css\?v=([a-f0-9]+)"', html_result.stdout)
            if css_match:
                css_version = css_match.group(1)
                print(f"Current CSS version: {css_version}")
                
                # Check CSS
                css_result = subprocess.run(
                    ["curl", "-sI", f"https://digitalalchemisten.de/assets/built/screen.css?v={css_version}"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if "HTTP/2 200" in css_result.stdout:
                    print("✅ CSS file is now accessible!")
                    return True
                else:
                    print("❌ CSS file still not accessible")
                    return False
            else:
                print("❌ Could not find CSS version")
                return False
        else:
            print("❌ Ghost failed to start")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        ssh.close()

if __name__ == "__main__":
    print("🚀 Safe Ghost Restart Script")
    print("="*60)
    print("This script will:")
    print("1. Stop Ghost service")
    print("2. Clear Nginx cache")
    print("3. Start Ghost service")
    print("4. Verify CSS availability")
    print("="*60)
    
    success = safe_ghost_restart()
    
    if success:
        print("\n🎉 Operation completed successfully!")
        print("Check https://digitalalchemisten.de to verify the fix.")
        sys.exit(0)
    else:
        print("\n❌ Operation completed with issues")
        print("Manual intervention may be required.")
        sys.exit(1)