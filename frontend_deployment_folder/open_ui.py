# ============================================
# FRONTEND: pi-client/open_ui.py
# ============================================
# Launcher - Auto-starts camera server + web UI
# Single command to run everything

import webbrowser
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import time

def start_local_server(port=5000):
    """Start simple HTTP server for HTML file"""
    class CORSRequestHandler(SimpleHTTPRequestHandler):
        def end_headers(self):
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', '*')
            SimpleHTTPRequestHandler.end_headers(self)
        
        def log_message(self, format, *args):
            pass  # Suppress logs
    
    server = HTTPServer(('0.0.0.0', port), CORSRequestHandler)
    
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    
    return server

def start_camera_server():
    """Start camera capture server in background"""
    try:
        from camera_capture import start_camera_server
        
        thread = threading.Thread(
            target=start_camera_server,
            args=(5001, True),  # port=5001, silent=True
            daemon=True
        )
        thread.start()
        
        # Wait for server to start
        time.sleep(1)
        return True
        
    except Exception as e:
        print(f"⚠️  Camera server not started: {e}")
        print("   Upload feature will still work")
        return False

def main():
    """Launch complete UI system"""
    print("\n" + "="*50)
    print("🥭 MANGO DISEASE DETECTION - CLIENT")
    print("="*50)
    
    # Check if HTML exists
    if not os.path.exists('web_ui.html'):
        print("❌ Error: web_ui.html not found")
        print("💡 Make sure you're in pi-client/ folder")
        sys.exit(1)
    
    # Start camera server (background)
    print("\n📷 Starting camera server...")
    camera_started = start_camera_server()
    
    if camera_started:
        print("✅ Camera server ready")
    
    # Start web server
    print("\n🌐 Starting web server...")
    port = 5000
    server = start_local_server(port)
    
    url = f"http://localhost:{port}/web_ui.html"
    
    print(f"✅ Web server running on port {port}")
    print(f"\n🔍 UI will auto-discover backend API")
    print(f"📷 Camera capture: {'Enabled' if camera_started else 'Disabled (upload only)'}")
    print(f"\n🌐 Opening browser: {url}")
    print("\n🛑 Press CTRL+C to stop")
    print("="*50 + "\n")
    
    # Open browser
    webbrowser.open(url)
    
    try:
        # Keep running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Stopped by user")
        server.shutdown()
        sys.exit(0)

if __name__ == "__main__":
    main()
