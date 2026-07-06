#!/usr/bin/env python3
"""
Safe Ghost Restart Script
Performs a complete restart of Ghost service and clears Nginx cache
"""
import os
import sys
import subprocess
import time

def get_github_secret(secret_name):
    """Get GitHub secret using gh CLI"""
    try:
        result = subprocess.run(
            ["gh", "secret", "list"],
            capture_output=True,
            text=True
        )
        
        for line in result.stdout.split('\n'):
            if secret_name in line:
                # Extract the value (last part of the line)
                parts = line.split()
                if len(parts) >= 2:
                    return parts[-1].strip()
        return None
    except Exception as e:
        print(f"❌ Could not get GitHub secret {secret_name}: {e}")
        return None

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
    
    try:
        # Use SSH command instead of paramiko for simplicity
        # 1. Check current Ghost status
        print("\n1️⃣ Checking current Ghost status...")
        ssh_cmd = f"sshpass -p '{vps_pw}' ssh -o StrictHostKeyChecking=no {vps_user}@{vps_ip}"
        
        # Check Ghost status
        status_cmd = f"{ssh_cmd} 'systemctl status ghost_digitalalchemisten-de.service --no-pager'"
        result = subprocess.run(status_cmd, shell=True, capture_output=True, text=True, timeout=30)
        print("Ghost Status:", result.stdout[:200] if result.stdout else "No output")
        
        # 2. Stop Ghost
        print("\n2️⃣ Stopping Ghost service...")
        stop_cmd = f"{ssh_cmd} 'sudo systemctl stop ghost_digitalalchemisten-de.service'"
        result = subprocess.run(stop_cmd, shell=True, capture_output=True, text=True, timeout=30)
        print("Stop Result:", result.stdout if result.stdout else "Success")
        
        # Wait a bit
        time.sleep(5)
        
        # 3. Clear Nginx cache
        print("\n3️⃣ Clearing Nginx cache...")
        nginx_cmd = f"{ssh_cmd} 'sudo nginx -t && sudo systemctl reload nginx'"
        result = subprocess.run(nginx_cmd, shell=True, capture_output=True, text=True, timeout=30)
        print("Nginx Result:", result.stdout if result.stdout else "Success")
        
        # 4. Start Ghost
        print("\n4️⃣ Starting Ghost service...")
        start_cmd = f"{ssh_cmd} 'sudo systemctl start ghost_digitalalchemisten-de.service'"
        result = subprocess.run(start_cmd, shell=True, capture_output=True, text=True, timeout=30)
        print("Start Result:", result.stdout if result.stdout else "Success")
        
        # Wait for Ghost to fully start
        time.sleep(10)
        
        # 5. Verify Ghost is running
        print("\n5️⃣ Verifying Ghost is running...")
        verify_cmd = f"{ssh_cmd} 'systemctl is-active ghost_digitalalchemisten-de.service'"
        result = subprocess.run(verify_cmd, shell=True, capture_output=True, text=True, timeout=30)
        
        if "active" in result.stdout.lower():
            print("✅ Ghost is running!")
            
            # 6. Check CSS availability
            print("\n6️⃣ Checking CSS availability...")
            time.sleep(5)  # Wait for assets to regenerate
            
            # Get current CSS version
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