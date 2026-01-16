# ============================================
# BACKEND: api/start_server.py
# ============================================
# Simple launcher with QR code and network info
# Use this instead of 'python main.py' for better UX

import socket
import qrcode
import sys
import os


def get_local_ip():
    """Get WiFi IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def generate_qr_code(url):
    """Generate QR code in terminal"""
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=1,
            border=1,
        )
        qr.add_data(url)
        qr.make(fit=True)
        qr.print_ascii(invert=True)
    except Exception:
        print("⚠️ QR code generation failed (optional feature)")


def main():
    """Start server with visual feedback"""
    local_ip = get_local_ip()
    port = 8000
    url = f"http://{local_ip}:{port}"

    # Display banner
    print("\n" + "=" * 60)
    print("🥭 MANGO DISEASE DETECTION API")
    print("=" * 60)
    print(f"\n📡 Network Configuration:")
    print(f"   IP Address: {local_ip}")
    print(f"   Port: {port}")
    print(f"\n🌐 Access URLs:")
    print(f"   • Direct IP:  {url}")
    print(f"   • mDNS Name:  http://mango-api.local:{port}")
    print(f"   • Localhost:  http://localhost:{port}")
    print(f"\n📖 API Documentation:")
    print(f"   {url}/docs")

    # QR Code (optional - for phone access)
    print(f"\n📱 QR Code (Optional - Scan to get IP):")
    print("─" * 40)
    generate_qr_code(url)
    print("─" * 40)

    print(f"\n✅ Starting server...")
    print(f"💡 Tip: Frontend will auto-discover this API")
    print(f"🛑 Press CTRL+C to stop")
    print("=" * 60 + "\n")

    # Start uvicorn
    try:
        import uvicorn
        from main import app

        uvicorn.run(app, host="0.0.0.0", port=port)

    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 Make sure all dependencies are installed:")
        print("   pip install -r requirements.txt")
        sys.exit(1)


if __name__ == "__main__":
    main()