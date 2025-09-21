#!/usr/bin/env python3
"""
Simple test server to verify localhost connection works
"""

from flask import Flask, jsonify
import socket

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <html>
    <head><title>StonkBot007 Test Server</title></head>
    <body>
        <h1>🤖 StonkBot007 Test Server</h1>
        <p>✅ Server is running successfully!</p>
        <p>If you can see this page, localhost connection is working.</p>
        <p><a href="/api/health">Test API Health</a></p>
    </body>
    </html>
    '''

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'healthy',
        'message': 'Test server is working!',
        'port': '5000'
    })

def find_available_port(start_port=5000):
    """Find an available port."""
    for port in range(start_port, start_port + 10):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue
    return None

if __name__ == '__main__':
    port = find_available_port(5000)
    if port is None:
        print("❌ No available ports found")
        exit(1)
    
    print(f"🚀 Starting test server on port {port}")
    print(f"🌐 Open http://localhost:{port} in your browser")
    print("🛑 Press Ctrl+C to stop")
    
    app.run(host='127.0.0.1', port=port, debug=False)
