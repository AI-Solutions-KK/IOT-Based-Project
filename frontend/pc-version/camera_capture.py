# pi-client/camera_capture.py
# Camera handling for Raspberry Pi
# Supports: CSI camera, USB camera, Laptop webcam

import cv2
import os
import time
import base64


def _is_valid_camera(index: int) -> bool:
    """Test if camera index is usable"""
    cap = cv2.VideoCapture(index, cv2.CAP_ANY)
    
    if not cap.isOpened():
        cap.release()
        return False
    
    time.sleep(0.2)  # Warm-up
    ret, frame = cap.read()
    cap.release()
    
    if not ret or frame is None:
        return False
    
    h, w = frame.shape[:2]
    return h > 100 and w > 100


def get_camera_index(max_scan: int = 6) -> int:
    """
    Auto-detect available camera
    
    Returns:
        int: Camera index (0, 1, 2, etc.)
    
    Raises:
        RuntimeError: If no camera found
    """
    # Check ENV override
    env_idx = os.environ.get("CAMERA_INDEX")
    if env_idx:
        try:
            idx = int(env_idx)
            if _is_valid_camera(idx):
                print(f"📷 Using camera from ENV: {idx}")
                return idx
        except ValueError:
            pass
    
    # Auto-scan
    for idx in range(max_scan):
        if _is_valid_camera(idx):
            print(f"📷 Auto-detected camera: {idx}")
            return idx
    
    raise RuntimeError(
        "❌ No camera detected\n"
        "• Check CSI ribbon or USB camera\n"
        "• Try: export CAMERA_INDEX=0"
    )


def capture_image(save_path: str = None) -> dict:
    """
    Capture image from camera
    
    Args:
        save_path: Optional path to save image
    
    Returns:
        dict with 'success', 'image_path', 'base64'
    """
    try:
        cam_index = get_camera_index()
        cap = cv2.VideoCapture(cam_index, cv2.CAP_ANY)
        
        if not cap.isOpened():
            return {"success": False, "error": "Camera not accessible"}
        
        ret, frame = cap.read()
        cap.release()
        
        if not ret or frame is None:
            return {"success": False, "error": "Failed to capture"}
        
        # Save to file
        if save_path:
            cv2.imwrite(save_path, frame)
        else:
            save_path = "temp_capture.jpg"
            cv2.imwrite(save_path, frame)
        
        # Convert to base64
        _, buffer = cv2.imencode('.jpg', frame)
        img_b64 = base64.b64encode(buffer).decode('utf-8')
        
        return {
            "success": True,
            "image_path": save_path,
            "base64": img_b64
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def image_to_base64(image_path: str) -> str:
    """Convert image file to base64"""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode('utf-8')


# Test function
if __name__ == "__main__":
    print("Testing camera...")
    result = capture_image("test_capture.jpg")
    
    if result["success"]:
        print(f"✅ Captured: {result['image_path']}")
        print(f"📦 Base64 length: {len(result['base64'])} chars")
    else:
        print(f"❌ Error: {result['error']}")