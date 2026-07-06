#!/usr/bin/env python3
"""
Verification script for the updated rebuild_theme.py
"""
import os
import sys
import subprocess

def verify_python_syntax():
    """Verify Python script has valid syntax"""
    print("🐍 Verifying Python script syntax...")
    
    result = subprocess.run(
        ["python3", "-m", "py_compile", "scripts/rebuild_theme.py"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✅ Python script syntax is valid")
        return True
    else:
        print("❌ Python script syntax error:")
        print(result.stderr)
        return False

def verify_script_changes():
    """Verify the script has the necessary changes"""
    print("\n🔧 Verifying script changes...")
    
    try:
        with open("scripts/rebuild_theme.py") as f:
            content = f.read()
        
        # Check for the .strip() calls that were added
        if "os.environ.get('VPS_IP', '').strip()" in content:
            print("✅ VPS_IP trimming added")
        else:
            print("❌ VPS_IP trimming missing")
            return False
            
        if "os.environ.get('VPS_USER', '').strip()" in content:
            print("✅ VPS_USER trimming added")
        else:
            print("❌ VPS_USER trimming missing")
            return False
            
        if "os.environ.get('VPS_PW', '').strip()" in content:
            print("✅ VPS_PW trimming added")
        else:
            print("❌ VPS_PW trimming missing")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error verifying script changes: {e}")
        return False

def verify_ghost_status():
    """Verify Ghost is running on the live site"""
    print("\n👻 Verifying Ghost status on live site...")
    
    result = subprocess.run(
        ["curl", "-sI", "https://digitalalchemisten.de/"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0 and "HTTP/2 200" in result.stdout:
        print("✅ Ghost is running and responding")
        return True
    else:
        print("❌ Ghost is not responding correctly")
        print(f"Exit code: {result.returncode}")
        print(f"Output: {result.stdout}")
        return False

def verify_css_status():
    """Verify CSS file status"""
    print("\n🎨 Verifying CSS file status...")
    
    # Check the main page to see what CSS version it's looking for
    result = subprocess.run(
        ["curl", "-s", "https://digitalalchemisten.de/"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        # Extract CSS version from HTML
        import re
        css_match = re.search(r'href="/assets/built/screen\.css\?v=([a-f0-9]+)"', result.stdout)
        if css_match:
            css_version = css_match.group(1)
            print(f"✅ Found CSS version in HTML: {css_version}")
            
            # Check if this CSS file exists
            css_result = subprocess.run(
                ["curl", "-sI", f"https://digitalalchemisten.de/assets/built/screen.css?v={css_version}"],
                capture_output=True,
                text=True
            )
            
            if "HTTP/2 200" in css_result.stdout:
                print(f"✅ CSS file with version {css_version} is accessible")
                return True
            else:
                print(f"❌ CSS file with version {css_version} is NOT accessible (404)")
                print(f"CSS check output: {css_result.stdout[:200]}")
                return False
        else:
            print("❌ Could not find CSS reference in HTML")
            return False
    else:
        print("❌ Could not fetch main page to check CSS version")
        return False

def main():
    """Run all verification checks"""
    print("🚀 Starting verification of updated rebuild_theme.py\n")
    
    results = []
    
    # Run all verification functions
    results.append(("Python syntax", verify_python_syntax()))
    results.append(("Script changes", verify_script_changes()))
    results.append(("Ghost status", verify_ghost_status()))
    results.append(("CSS status", verify_css_status()))
    
    # Summary
    print("\n" + "="*60)
    print("VERIFICATION SUMMARY")
    print("="*60)
    
    all_passed = True
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} {name}")
        if not passed:
            all_passed = False
    
    print("="*60)
    
    if all_passed:
        print("🎉 All verification checks passed!")
        return 0
    else:
        print("❌ Some verification checks failed.")
        print("\nThe CSS file is still not accessible, which means:")
        print("1. The theme rebuild worked (version changed)")
        print("2. But the file is not being served by Ghost/Nginx")
        print("3. This could be a routing, caching, or permissions issue")
        return 1

if __name__ == "__main__":
    sys.exit(main())