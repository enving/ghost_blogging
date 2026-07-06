#!/usr/bin/env python3
"""
Verification script for Ghost theme rebuild functionality
"""
import os
import sys
import subprocess
import tempfile

def verify_files_exist():
    """Verify that the created files exist and have correct content"""
    print("🔍 Verifying created files...")
    
    files_to_check = [
        "scripts/rebuild_theme.py",
        ".github/workflows/rebuild-theme.yml"
    ]
    
    all_exist = True
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"✅ {file_path} exists")
            
            # Check file size
            size = os.path.getsize(file_path)
            if size > 100:  # Reasonable minimum size
                print(f"   Size: {size} bytes ✅")
            else:
                print(f"   Size: {size} bytes ❌ (too small)")
                all_exist = False
        else:
            print(f"❌ {file_path} does not exist")
            all_exist = False
    
    return all_exist

def verify_python_script_syntax():
    """Verify Python script has valid syntax"""
    print("\n🐍 Verifying Python script syntax...")
    
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

def verify_workflow_syntax():
    """Verify GitHub Actions workflow syntax"""
    print("\n🤖 Verifying GitHub Actions workflow syntax...")
    
    # Basic YAML syntax check
    try:
        import yaml
        with open(".github/workflows/rebuild-theme.yml") as f:
            yaml.safe_load(f)
        print("✅ Workflow YAML syntax is valid")
        return True
    except Exception as e:
        print(f"❌ Workflow YAML syntax error: {e}")
        return False

def verify_workflow_structure():
    """Verify workflow has required components"""
    print("\n📋 Verifying workflow structure...")
    
    try:
        import yaml
        with open(".github/workflows/rebuild-theme.yml") as f:
            workflow = yaml.safe_load(f)
        
        # Check required fields
        checks = [
            ("name", "Workflow name"),
            ("on", "Trigger events"),
            ("jobs", "Jobs definition"),
        ]
        
        all_good = True
        for field, description in checks:
            if field in workflow and workflow[field]:  # Check that field exists and is not empty
                print(f"✅ {description} present")
            else:
                print(f"❌ {description} missing or empty")
                all_good = False
        
        # Check if rebuild-theme job exists
        if "rebuild-theme" in workflow.get("jobs", {}):
            print("✅ rebuild-theme job present")
            job = workflow["jobs"]["rebuild-theme"]
            
            # Check job steps
            if "steps" in job:
                print(f"✅ Job has {len(job['steps'])} steps")
                
                # Check for key steps
                step_names = [step.get("name", "") for step in job["steps"]]
                required_steps = [
                    "Checkout repository",
                    "Set up Python",
                    "Install dependencies",
                    "Rebuild Ghost Theme"
                ]
                
                for required in required_steps:
                    if any(required in name for name in step_names):
                        print(f"✅ Step '{required}' found")
                    else:
                        print(f"❌ Step '{required}' missing")
                        all_good = False
            else:
                print("❌ Job steps missing")
                all_good = False
        else:
            print("❌ rebuild-theme job missing")
            all_good = False
        
        return all_good
        
    except Exception as e:
        print(f"❌ Error verifying workflow structure: {e}")
        return False

def verify_script_functionality():
    """Verify the script has required functionality"""
    print("\n🔧 Verifying script functionality...")
    
    try:
        with open("scripts/rebuild_theme.py") as f:
            content = f.read()
        
        required_elements = [
            ("paramiko", "SSH library import"),
            ("rebuild_theme()", "Main function"),
            ("ssh.connect", "SSH connection"),
            ("ghost theme rebuild", "Ghost rebuild command"),
            ("systemctl restart", "Service restart"),
            ("VPS_IP", "VPS IP environment variable"),
            ("VPS_USER", "VPS user environment variable"),
            ("VPS_PW", "VPS password environment variable")
        ]
        
        all_good = True
        for element, description in required_elements:
            if element in content:
                print(f"✅ {description} found")
            else:
                print(f"❌ {description} missing")
                all_good = False
        
        return all_good
        
    except Exception as e:
        print(f"❌ Error verifying script functionality: {e}")
        return False

def main():
    """Run all verification checks"""
    print("🚀 Starting verification of Ghost theme rebuild functionality\n")
    
    results = []
    
    # Run all verification functions
    results.append(("Files exist", verify_files_exist()))
    results.append(("Python syntax", verify_python_script_syntax()))
    results.append(("Workflow YAML syntax", verify_workflow_syntax()))
    results.append(("Workflow structure", verify_workflow_structure()))
    results.append(("Script functionality", verify_script_functionality()))
    
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
        print("\nThe Ghost theme rebuild functionality is ready to use.")
        print("You can trigger it by:")
        print("1. Pushing changes to main branch")
        print("2. Manually running the workflow in GitHub Actions")
        return 0
    else:
        print("❌ Some verification checks failed.")
        print("\nPlease review the issues above and fix them.")
        return 1

if __name__ == "__main__":
    sys.exit(main())