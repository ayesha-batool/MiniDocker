"""Utility functions for Mini Docker - reduces code redundancy"""
import os
import platform
import subprocess

def windows_to_wsl_path(windows_path):
    """Convert Windows path to WSL path format"""
    windows_path = os.path.normpath(windows_path)
    if len(windows_path) >= 3 and windows_path[1:3] == ':\\':
        drive = windows_path[0].lower()
        path = windows_path[3:].replace('\\', '/')
        return f"/mnt/{drive}/{path}"
    return windows_path.replace('\\', '/')

def is_wsl_available():
    """Check if WSL is available and properly configured"""
    if platform.system() != "Windows":
        return False
    try:
        if subprocess.run(["wsl", "--list", "--quiet"], capture_output=True, timeout=5).returncode != 0:
            return False
        wsl_cmd = "wsl.exe" if os.path.exists("C:\\Windows\\System32\\wsl.exe") else "wsl"
        result = subprocess.run([wsl_cmd, "bash", "-c", "which unshare"],
                              capture_output=True, timeout=8,
                              creationflags=subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0)
        return result.returncode == 0
    except:
        return False

def test_wsl_connection():
    """Test WSL connection and return status"""
    if platform.system() != "Windows":
        return True, "Not on Windows"
    wsl_cmd = "wsl.exe" if os.path.exists("C:\\Windows\\System32\\wsl.exe") else "wsl"
    try:
        if subprocess.run([wsl_cmd, "--list", "--quiet"], capture_output=True, timeout=5).returncode != 0:
            return False, "WSL command failed"
        result = subprocess.run([wsl_cmd, "bash", "-c", "which unshare"],
                              capture_output=True, timeout=8, text=True,
                              creationflags=subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0)
        if result.returncode == 0 and result.stdout.strip():
            return True, "WSL is properly configured"
        return False, "unshare not found. Install util-linux: wsl sudo apt-get install util-linux"
    except subprocess.TimeoutExpired:
        return True, "WSL is available (slow response)"
    except FileNotFoundError:
        return False, "WSL is not installed. Install with: wsl --install"
    except Exception as e:
        return False, f"WSL test failed: {str(e)}"

def parse_volume(volume_str):
    """Parse volume string (host_path:container_path) into tuple"""
    if ":" in volume_str:
        return tuple(volume_str.split(":", 1))
    return (volume_str, volume_str)

def parse_env_var(env_str):
    """Parse environment variable string (KEY=VALUE) into tuple"""
    if "=" in env_str:
        key, value = env_str.split("=", 1)
        return (key.strip(), value.strip())
    return (env_str.strip(), "")

