# ============================================
# BACKEND: api/main.py
# ============================================
# FastAPI Backend with Auto IP Detection + mDNS Broadcasting
# Works on any WiFi network automatically

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64
import io
from PIL import Image
import os
import tempfile
import socket
from zeroconf import ServiceInfo, Zeroconf

from inference import predict_image
from voice import speak


# ==================== AUTO IP DETECTION ====================
def get_local_ip():
    """Get PC's WiFi IP address automatically"""
    try:
        # Create dummy socket to find local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"


# ==================== APP SETUP ====================
app = FastAPI(
    title="Mango Disease Detection API",
    description="AI-powered mango plant disease diagnosis",
    version="2.0.0"
)

# CORS - Allow all origins for portability
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== MDNS BROADCASTING ====================
zeroconf = None
service_info = None


def start_mdns_broadcast(port=8000):
    """Broadcast API as 'mango-api.local' on network"""
    global zeroconf, service_info

    try:
        local_ip = get_local_ip()

        zeroconf = Zeroconf()
        service_info = ServiceInfo(
            "_http._tcp.local.",
            "Mango-API._http._tcp.local.",
            addresses=[socket.inet_aton(local_ip)],
            port=port,
            properties={
                'description': 'Mango Disease Detection API',
                'version': '2.0.0'
            },
            server="mango-api.local."
        )

        zeroconf.register_service(service_info)
        print(f"🔊 Broadcasting as: mango-api.local")

    except Exception as e:
        print(f"⚠️ mDNS broadcast failed (optional): {e}")


def stop_mdns_broadcast():
    """Stop mDNS broadcasting"""
    global zeroconf, service_info

    if zeroconf and service_info:
        try:
            zeroconf.unregister_service(service_info)
            zeroconf.close()
        except Exception:
            pass


# ==================== STARTUP/SHUTDOWN ====================
@app.on_event("startup")
async def startup_event():
    """Initialize mDNS on startup"""
    start_mdns_broadcast(8000)


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup mDNS on shutdown"""
    stop_mdns_broadcast()


# ==================== REQUEST MODEL ====================
class DiagnoseRequest(BaseModel):
    image: str  # Base64 encoded
    enable_voice: bool = False


# ==================== ENDPOINTS ====================
@app.get("/")
def root():
    """Root endpoint with network info"""
    local_ip = get_local_ip()
    return {
        "status": "healthy",
        "service": "Mango Disease Detection API",
        "version": "2.0.0",
        "network": {
            "ip": local_ip,
            "port": 8000,
            "mdns": "mango-api.local"
        },
        "docs": "/docs"
    }


@app.get("/health")
def health():
    """Health check endpoint"""
    models_exist = os.path.exists("models/efficientnetv2_b0_embedding_512.tflite")
    svm_exists = os.path.exists("embeddings_cache/svc_model.pkl")

    return {
        "status": "healthy" if (models_exist and svm_exists) else "unhealthy",
        "tflite_model": models_exist,
        "svm_model": svm_exists,
        "ip": get_local_ip()
    }


@app.get("/network-info")
def network_info():
    """Get current network configuration"""
    return {
        "ip": get_local_ip(),
        "port": 8000,
        "mdns": "mango-api.local",
        "accessible_urls": [
            f"http://{get_local_ip()}:8000",
            "http://mango-api.local:8000",
            "http://localhost:8000"
        ]
    }


@app.post("/diagnose")
def diagnose(request: DiagnoseRequest):
    """Main diagnosis endpoint"""
    try:
        # Decode base64 image
        image_data = base64.b64decode(request.image)
        image = Image.open(io.BytesIO(image_data))

        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            image.save(tmp.name, format="JPEG")
            tmp_path = tmp.name

        # Run inference
        result = predict_image(tmp_path)

        # Cleanup
        os.remove(tmp_path)

        # Voice output (if enabled)
        if request.enable_voice and result.get("status") == "success":
            label = result.get("predicted_label", "")
            confidence = result.get("confidence", 0)
            cause = result.get("cause", "")
            treatment = result.get("treatment", "")
            prevention = result.get("prevention", "")

            speech_text = (
                f"Disease detected: {label}. "
                f"Confidence {int(confidence * 100)} percent. "
                f"Cause: {cause}. "
                f"Treatment: {treatment}. "
                f"Prevention: {prevention}."
            )

            speak(speech_text)

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== RUN SERVER ====================
if __name__ == "__main__":
    import uvicorn

    local_ip = get_local_ip()

    print("\n" + "=" * 50)
    print("🥭 Mango Disease Detection API")
    print("=" * 50)
    print(f"📡 Local IP: {local_ip}")
    print(f"🌐 Access URLs:")
    print(f"   • http://{local_ip}:8000")
    print(f"   • http://mango-api.local:8000")
    print(f"   • http://localhost:8000")
    print(f"📖 Docs: http://{local_ip}:8000/docs")
    print("=" * 50 + "\n")

    uvicorn.run(app, host="0.0.0.0", port=8000)