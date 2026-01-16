# ============================================
# FRONTEND: pi-client/open_ui.py
# ============================================
# Simple launcher - Opens web UI in browser
# Auto-discovers backend API

import webbrowser
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading

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

def main():
    """Launch UI"""
    print("\n" + "="*50)
    print("🥭 MANGO DISEASE DETECTION - CLIENT")
    print("="*50)
    
    # Check if HTML exists
    if not os.path.exists('web_ui.html'):
        print("❌ Error: web_ui.html not found")
        print("💡 Make sure you're in pi-client/ folder")
        sys.exit(1)
    
    # Start local server
    print("\n🌐 Starting local server...")
    port = 5000
    server = start_local_server(port)
    
    url = f"http://localhost:{port}/web_ui.html"
    
    print(f"✅ Server running on port {port}")
    print(f"\n🔍 Auto-discovering API...")
    print(f"💡 UI will connect automatically")
    print(f"\n🌐 Opening browser: {url}")
    print("\n🛑 Press CTRL+C to stop")
    print("="*50 + "\n")
    
    # Open browser
    webbrowser.open(url)
    
    try:
        # Keep running
        while True:
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Stopped by user")
        server.shutdown()
        sys.exit(0)

if __name__ == "__main__":
    main()