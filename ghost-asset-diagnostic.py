#!/usr/bin/env python3
"""
Ghost Asset Fix Script - Non-destructive version
Checks asset status and provides diagnostic information
"""
import os
import sys
import subprocess
import time

def check_ghost_status():
    """Check if Ghost is running"""
    print("👻 Checking Ghost status...")
    try:
        result = subprocess.run(
            ["curl", "-sI", "https://digitalalchemisten.de/"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0 and "HTTP/2 200" in result.stdout:
            print("✅ Ghost is running and responding")
            return True
        else:
            print("❌ Ghost is not responding correctly")
            return False
    except Exception as e:
        print(f"❌ Error checking Ghost status: {e}")
        return False

def check_css_status():
    """Check CSS file status"""
    print("\n🎨 Checking CSS file status...")
    
    # First, get the current CSS version from the main page
    try:
        result = subprocess.run(
            ["curl", "-s", "https://digitalalchemisten.de/"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            print("❌ Could not fetch main page")
            return None, None
        
        # Extract CSS version
        import re
        css_match = re.search(r'href="/assets/built/screen\.css\?v=([a-f0-9]+)"', result.stdout)
        if css_match:
            css_version = css_match.group(1)
            print(f"✅ Found CSS version: {css_version}")
            
            # Check if CSS file exists
            css_result = subprocess.run(
                ["curl", "-sI", f"https://digitalalchemisten.de/assets/built/screen.css?v={css_version}"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if "HTTP/2 200" in css_result.stdout:
                print(f"✅ CSS file is accessible")
                return css_version, True
            else:
                print(f"❌ CSS file is NOT accessible (404)")
                return css_version, False
        else:
            print("❌ Could not find CSS reference in HTML")
            return None, False
            
    except Exception as e:
        print(f"❌ Error checking CSS status: {e}")
        return None, False

def check_asset_paths():
    """Check what asset paths are being used"""
    print("\n🔍 Checking asset paths...")
    
    try:
        result = subprocess.run(
            ["curl", "-s", "https://digitalalchemisten.de/"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            # Find all asset references
            import re
            assets = re.findall(r'href="(/assets/[^"]+)"', result.stdout)
            css_assets = [a for a in assets if '.css' in a]
            
            print(f"✅ Found {len(css_assets)} CSS asset references:")
            for asset in css_assets[:5]:  # Show first 5
                print(f"   - {asset}")
                
            # Check each CSS asset
            print("\n📊 Checking CSS asset availability:")
            for asset in css_assets[:3]:  # Check first 3
                full_url = f"https://digitalalchemisten.de{asset}"
                asset_result = subprocess.run(
                    ["curl", "-sI", full_url],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                
                if "HTTP/2 200" in asset_result.stdout:
                    print(f"✅ {asset} - OK")
                else:
                    print(f"❌ {asset} - NOT FOUND")
                    
            return True
        else:
            print("❌ Could not fetch page to check assets")
            return False
            
    except Exception as e:
        print(f"❌ Error checking asset paths: {e}")
        return False

def provide_diagnostics():
    """Provide diagnostic information"""
    print("\n💡 DIAGNOSTIC INFORMATION:")
    print("="*60)
    
    ghost_ok = check_ghost_status()
    css_version, css_ok = check_css_status()
    assets_ok = check_asset_paths()
    
    print("\n" + "="*60)
    print("SUMMARY:")
    print("="*60)
    print(f"Ghost Status: {'✅ OK' if ghost_ok else '❌ FAILED'}")
    print(f"CSS Status: {'✅ OK' if css_ok else '❌ FAILED'} (Version: {css_version if css_version else 'N/A'})")
    print(f"Asset Check: {'✅ OK' if assets_ok else '❌ FAILED'}")
    
    if ghost_ok and not css_ok:
        print("\n🔧 RECOMMENDED ACTIONS:")
        print("1. Ghost Theme neu bauen (bereits versucht)")
        print("2. Ghost komplett neu starten (stop/start)")
        print("3. Nginx-Cache leeren")
        print("4. Dateiberechtigungen prüfen")
        print("5. Ghost-Logs prüfen")
    
    return ghost_ok and css_ok and assets_ok

if __name__ == "__main__":
    print("🚀 Ghost Asset Diagnostic Tool")
    print("="*60)
    
    success = provide_diagnostics()
    
    if success:
        print("\n🎉 All checks passed!")
        sys.exit(0)
    else:
        print("\n❌ Issues found - see recommendations above")
        sys.exit(1)