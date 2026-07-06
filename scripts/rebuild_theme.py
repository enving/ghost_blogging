#!/usr/bin/env python3
"""
Rebuild Ghost Theme via SSH
Connects to VPS and rebuilds the Ghost theme to fix missing CSS assets
"""
from pathlib import Path
import paramiko
import sys
import os

def rebuild_theme():
    """Rebuild Ghost theme on VPS"""
    
    # Get credentials from environment variables (set by GitHub Actions)
    vps_ip = os.environ.get('VPS_IP', '').strip()
    vps_user = os.environ.get('VPS_USER', '').strip()
    vps_pw = os.environ.get('VPS_PW', '').strip()
    
    print(f"Debug - VPS_IP: '{vps_ip}'")
    print(f"Debug - VPS_USER: '{vps_user}'")
    print(f"Debug - VPS_PW: '{'***' if vps_pw else 'None'}'")
    
    if not vps_ip or not vps_user or not vps_pw:
        print("❌ Missing VPS credentials from environment variables")
        print("Required: VPS_IP, VPS_USER, VPS_PW")
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
        
        # 1. Check Ghost status
        print("\n" + "="*60)
        print("1️⃣ Checking Ghost Status")
        print("="*60)
        stdin, stdout, stderr = ssh.exec_command("systemctl status ghost_digitalalchemisten-de.service")
        status_output = stdout.read().decode()
        print(status_output)
        
        # 2. Navigate to Ghost directory
        print("\n" + "="*60)
        print("2️⃣ Navigating to Ghost Directory")
        print("="*60)
        
        # 3. Rebuild theme
        print("\n" + "="*60)
        print("3️⃣ Rebuilding Ghost Theme")
        print("="*60)
        
        # Ghost CLI command to rebuild theme
        stdin, stdout, stderr = ssh.exec_command("cd /var/www/ghost && ghost theme rebuild")
        rebuild_output = stdout.read().decode()
        error_output = stderr.read().decode()
        
        print("Rebuild Output:")
        print(rebuild_output)
        
        if error_output:
            print("Errors:")
            print(error_output)
        
        # 4. Restart Ghost
        print("\n" + "="*60)
        print("4️⃣ Restarting Ghost Service")
        print("="*60)
        
        stdin, stdout, stderr = ssh.exec_command("systemctl restart ghost_digitalalchemisten-de.service")
        restart_output = stdout.read().decode()
        
        print("Restart Output:")
        print(restart_output)
        
        # 5. Check if theme rebuild was successful
        print("\n" + "="*60)
        print("5️⃣ Verifying Theme Rebuild")
        print("="*60)
        
        # Check if CSS file exists
        stdin, stdout, stderr = ssh.exec_command("ls -la /var/www/ghost/content/themes/casper/assets/built/screen.css")
        css_check = stdout.read().decode()
        
        if "screen.css" in css_check:
            print("✅ Theme CSS file found!")
        else:
            print("❌ Theme CSS file not found")
            print("Trying alternative path...")
            stdin, stdout, stderr = ssh.exec_command("find /var/www/ghost -name 'screen.css' 2>/dev/null")
            find_output = stdout.read().decode()
            print("Search results:")
            print(find_output)
        
        # 6. Check Ghost logs
        print("\n" + "="*60)
        print("6️⃣ Ghost Service Logs")
        print("="*60)
        
        stdin, stdout, stderr = ssh.exec_command("journalctl -u ghost_digitalalchemisten-de.service -n 20 --no-pager")
        logs = stdout.read().decode()
        print(logs)
        
        print("\n" + "="*60)
        print("✅ Theme Rebuild Complete!")
        print("="*60)
        print("\n📝 Summary:")
        print("- Ghost theme rebuilt")
        print("- Ghost service restarted")
        print("- Check https://digitalalchemisten.de for CSS changes")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        ssh.close()

if __name__ == '__main__':
    success = rebuild_theme()
    sys.exit(0 if success else 1)