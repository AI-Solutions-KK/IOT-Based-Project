# ============================================
# FRONTEND: pi-client/camera_capture.py
# ============================================
# Smart Multi-Camera Support with Auto-Detection + Live Streaming
# Priority: CSI → USB → Built-in Webcam
# Auto-starts with open_ui.py

from flask import Flask, jsonify, Response
from flask_cors import CORS
import cv2
import base64
import os
import time

app = Flask(__name__)
CORS(app)

# Global camera configuration
CAMERA_INDEX = None
CAMERA_TYPE = None

def detect_camera():
    """
    Auto-detect available camera with priority:
    1. CSI camera (/dev/video0 on Pi)
    2. USB webcam (any /dev/video*)
    3. Built-in webcam (laptop/PC)
    
    Returns:
        tuple: (camera_index, camera_type)
    """
    global CAMERA_INDEX, CAMERA_TYPE
    
    # Check if running on Raspberry Pi
    is_pi = os.path.exists('/dev/video0') and os.path.exists('/boot/config.txt')
    
    # Try CSI camera first (Pi only)
    if is_pi:
        for idx in [0, 1, 2]:
            cap = cv2.VideoCapture(idx, cv2.CAP_V4L2)
            if cap.isOpened():
                # Warm-up test
                for _ in range(3):
                    ret, _ = cap.read()
                ret, frame = cap.read()
                cap.release()
                
                if ret and frame is not None:
                    CAMERA_INDEX = idx
                    CAMERA_TYPE = "CSI Camera"
                    print(f"✅ Detected: {CAMERA_TYPE} at /dev/video{idx}")
                    return (idx, CAMERA_TYPE)
    
    # Try USB/Built-in webcam (any platform)
    for idx in range(6):
        cap = cv2.VideoCapture(idx)
        if cap.isOpened():
            ret, frame = cap.read()
            cap.release()
            
            if ret and frame is not None:
                CAMERA_INDEX = idx
                CAMERA_TYPE = "USB Webcam" if is_pi else "Built-in Webcam"
                print(f"✅ Detected: {CAMERA_TYPE} at index {idx}")
                return (idx, CAMERA_TYPE)
    
    # No camera found
    CAMERA_INDEX = None
    CAMERA_TYPE = None
    print("⚠️ No camera detected")
    return (None, None)

@app.route('/camera-info', methods=['GET'])
def camera_info():
    """Get current camera configuration"""
    return jsonify({
        "available": CAMERA_INDEX is not None,
        "index": CAMERA_INDEX,
        "type": CAMERA_TYPE,
        "device": f"/dev/video{CAMERA_INDEX}" if CAMERA_INDEX is not None else None
    })

@app.route('/capture', methods=['POST', 'GET'])
def capture():
    """Capture image from detected camera"""
    if CAMERA_INDEX is None:
        return jsonify({
            "success": False,
            "error": "No camera detected. Please check camera connection."
        }), 404
    
    try:
        # Open camera with appropriate backend
        is_pi = CAMERA_TYPE == "CSI Camera"
        cap = cv2.VideoCapture(CAMERA_INDEX, cv2.CAP_V4L2 if is_pi else cv2.CAP_ANY)
        
        if not cap.isOpened():
            return jsonify({
                "success": False,
                "error": f"{CAMERA_TYPE} not accessible"
            }), 500
        
        # Warm-up frames (important for CSI)
        warmup_frames = 5 if is_pi else 2
        for _ in range(warmup_frames):
            cap.read()
        
        time.sleep(0.1)
        
        # Capture frame
        ret, frame = cap.read()
        cap.release()
        
        if not ret or frame is None:
            return jsonify({
                "success": False,
                "error": "Failed to capture frame"
            }), 500
        
        # Encode to JPEG
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        _, buffer = cv2.imencode('.jpg', frame, encode_param)
        img_b64 = base64.b64encode(buffer).decode('utf-8')
        
        return jsonify({
            "success": True,
            "base64": img_b64,
            "camera_type": CAMERA_TYPE,
            "camera_index": CAMERA_INDEX
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/video_feed')
def video_feed():
    """Live video stream from camera for preview"""
    def generate():
        if CAMERA_INDEX is None:
            return
        
        is_pi = CAMERA_TYPE == "CSI Camera"
        cap = cv2.VideoCapture(CAMERA_INDEX, cv2.CAP_V4L2 if is_pi else cv2.CAP_ANY)
        
        if not cap.isOpened():
            return
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Encode frame to JPEG
                encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 80]
                _, buffer = cv2.imencode('.jpg', frame, encode_param)
                
                # Yield frame in multipart format
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        
        finally:
            cap.release()
    
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "online",
        "camera_available": CAMERA_INDEX is not None
    })

def start_camera_server(port=5001, silent=False):
    """
    Start camera server (called from open_ui.py)
    
    Args:
        port: Server port
        silent: Suppress output
    """
    # Detect camera on startup
    detect_camera()
    
    if not silent:
        print("📷 Camera Capture Server")
        print("="*50)
        if CAMERA_INDEX is not None:
            print(f"✅ Camera: {CAMERA_TYPE}")
            print(f"📍 Index: {CAMERA_INDEX}")
        else:
            print("⚠️  No camera detected")
            print("   Upload feature will still work")
        print(f"🌐 Running on: http://localhost:{port}")
        print("="*50)
    
    # Run server without verbose logs
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    
    app.run(
        host='127.0.0.1',
        port=port,
        debug=False,
        use_reloader=False
    )

if __name__ == "__main__":
    start_camera_server()