import os
import subprocess
import sys

def check_dependencies():
    required = ['gst-launch-1.0', 'ffmpeg', 'python3']
    for cmd in required:
        if not subprocess.run(['which', cmd], capture_output=True).returncode == 0:
            print(f"❌ Missing dependency: {cmd}")
            return False
    return True

def check_services():
    services = ['rtsp-server', 'recording-server', 'dashboard']
    for service in services:
        status = subprocess.run(['systemctl', 'is-active', service],
                              capture_output=True).stdout.decode().strip()
        print(f"Service {service}: {status}")

def main():
    if not check_dependencies():
        sys.exit(1)
    check_services()

if __name__ == "__main__":
    main()