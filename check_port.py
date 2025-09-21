#!/usr/bin/env python3
"""
Port checker utility for StonkBot007
"""

import socket
import subprocess
import sys

def find_available_port(start_port=5000, max_attempts=10):
    """Find an available port starting from start_port."""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue
    return None

def check_port_usage(port):
    """Check what's using a specific port."""
    try:
        result = subprocess.run(['lsof', '-ti', f':{port}'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            pids = result.stdout.strip().split('\n')
            return pids
        return []
    except:
        return []

def main():
    print("🔍 StonkBot007 Port Checker")
    print("=" * 30)
    
    # Check port 5000
    port_5000_usage = check_port_usage(5000)
    if port_5000_usage:
        print(f"❌ Port 5000 is in use by processes: {', '.join(port_5000_usage)}")
        print("💡 To free port 5000, run:")
        print("   lsof -ti:5000 | xargs kill -9")
        print("   # Or disable AirPlay Receiver in System Preferences")
    else:
        print("✅ Port 5000 is available")
    
    # Find available port
    available_port = find_available_port(5000)
    if available_port:
        print(f"✅ First available port: {available_port}")
        print(f"🌐 You can access the app at: http://localhost:{available_port}")
    else:
        print("❌ No available ports found in range 5000-5009")
        print("💡 Try freeing up some ports or restart your system")
    
    print("\n🚀 To start the server:")
    print("   python start_portfolio_scanner.py")

if __name__ == "__main__":
    main()
