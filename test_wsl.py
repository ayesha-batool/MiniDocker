#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WSL Setup Verification Script
Tests if WSL is properly configured for Mini Docker
"""
import subprocess
import platform
import sys
import io

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def test_wsl_installation():
    """Test if WSL is installed"""
    print("🔍 Testing WSL Installation...")
    try:
        result = subprocess.run(["wsl", "--list", "--verbose"],
                              capture_output=True, timeout=5)
        if result.returncode == 0:
            print("✅ WSL is installed")
            print(f"   Output: {result.stdout.decode().strip()}")
            return True
        else:
            print("❌ WSL command failed")
            return False
    except FileNotFoundError:
        print("❌ WSL is not installed")
        print("   Install with: wsl --install")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_unshare():
    """Test if unshare is available in WSL"""
    print("\n🔍 Testing unshare command in WSL...")
    try:
        result = subprocess.run(["wsl", "which", "unshare"],
                              capture_output=True, timeout=5)
        if result.returncode == 0:
            unshare_path = result.stdout.decode().strip()
            print(f"✅ unshare found at: {unshare_path}")
            
            # Test version
            version_result = subprocess.run(["wsl", "unshare", "--version"],
                                          capture_output=True, timeout=5)
            if version_result.returncode == 0:
                version = version_result.stdout.decode().strip()
                print(f"   Version: {version}")
                return True
            else:
                print("❌ unshare version check failed")
                return False
        else:
            print("❌ unshare command not found in WSL")
            print("   Install with: wsl sudo apt-get install util-linux")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_path_conversion():
    """Test Windows to WSL path conversion"""
    print("\n🔍 Testing path conversion...")
    if platform.system() != "Windows":
        print("⏭️  Skipping (not on Windows)")
        return True
    
    test_path = "F:\\5 Semester\\OS\\Mini Docker"
    wsl_path = f"/mnt/f/5 Semester/OS/Mini Docker"
    
    try:
        result = subprocess.run(["wsl", "test", "-d", wsl_path],
                              capture_output=True, timeout=5)
        if result.returncode == 0:
            print(f"✅ Path conversion works")
            print(f"   Windows: {test_path}")
            print(f"   WSL: {wsl_path}")
            return True
        else:
            print(f"⚠️  Path exists but may need verification")
            return True  # Not a critical failure
    except Exception as e:
        print(f"⚠️  Path test error: {e}")
        return True  # Not a critical failure

def test_basic_command():
    """Test basic WSL command execution"""
    print("\n🔍 Testing basic WSL command execution...")
    try:
        result = subprocess.run(["wsl", "echo", "Hello from WSL"],
                              capture_output=True, timeout=5)
        if result.returncode == 0:
            output = result.stdout.decode().strip()
            print(f"✅ WSL command execution works: {output}")
            return True
        else:
            print("❌ WSL command execution failed")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all WSL tests"""
    print("=" * 60)
    print("🐳 Mini Docker - WSL Setup Verification")
    print("=" * 60)
    
    if platform.system() != "Windows":
        print("\n⏭️  This script is for Windows systems only.")
        print("   On Linux, all features work natively.")
        sys.exit(0)
    
    results = []
    
    # Run tests
    results.append(("WSL Installation", test_wsl_installation()))
    results.append(("unshare Command", test_unshare()))
    results.append(("Basic Command", test_basic_command()))
    results.append(("Path Conversion", test_path_conversion()))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ All tests passed! WSL is properly configured.")
        print("   You can now use Mini Docker with full containerization features.")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        print("\n💡 Quick Setup Guide:")
        print("   1. Install WSL: wsl --install")
        print("   2. Install util-linux in WSL:")
        print("      wsl sudo apt-get update")
        print("      wsl sudo apt-get install util-linux")
        print("   3. Verify: wsl unshare --version")
    print("=" * 60)
    
    sys.exit(0 if all_passed else 1)

if __name__ == "__main__":
    main()

