#!/usr/bin/env python3
"""
Startup script for StonkBot007 Portfolio Scanner
Launches the API server and opens the frontend
"""

import subprocess
import webbrowser
import time
import sys
import os
from threading import Timer

def open_browser(port=5000):
    """Open the browser after a short delay."""
    time.sleep(2)
    webbrowser.open(f'http://localhost:{port}')

def main():
    """Main startup function."""
    print("🤖 StonkBot007 - Portfolio Scanner")
    print("=" * 50)
    print("🚀 Starting API server...")
    print("🌐 Frontend will open automatically")
    print("📊 Portfolio Scanner API will find an available port")
    print("\n" + "=" * 50)
    print("💡 Features:")
    print("   • Secure user login with demo accounts")
    print("   • Portfolio scanning and analysis")
    print("   • Real-time news sentiment analysis")
    print("   • Actionable investment insights")
    print("   • Risk assessment and recommendations")
    print("\n" + "=" * 50)
    print("🔑 Demo Login Credentials:")
    print("   Username: priya, rohan, ananya")
    print("   Password: password123")
    print("\n" + "=" * 50)
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Start the Flask API server
        subprocess.run([sys.executable, 'api_server.py'], check=True)
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        print("👋 Thank you for using StonkBot007!")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error starting server: {e}")
        print("💡 Make sure you have installed the requirements:")
        print("   pip install -r requirements.txt")
        print("💡 If port 5000 is in use, try:")
        print("   - Disable AirPlay Receiver in System Preferences")
        print("   - Or the server will automatically find another port")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
