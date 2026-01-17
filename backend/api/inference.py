# ============================================
# BACKEND: api/inference.py
# ============================================
# ML Inference Engine - TFLite EfficientNetV2 + SVM
# Cloud-compatible (No camera dependencies)

import os
import pickle
import numpy as np
from PIL import Image
import tensorflow as tf

# ================= PATHS (Cloud-Safe) =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "models", "efficientnetv2_b0_embedding_512.tflite")
CACHE_DIR = os.path.join(BASE_DIR, "embeddings_cache")
SVC_FILE = os.path.join(CACHE_DIR, "svc_model.pkl")
CLASSES_FILE = os.path.join(CACHE_DIR, "classes.npy")

IMG_SIZE = 224
EMB_DIM = 512  # Must match training

# ================= LOAD TFLITE =================
interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# ================= LOAD CLASSIFIER =================
with open(SVC_FILE, "rb") as f:
    obj = pickle.load(f)

clf = obj["clf"]  # SVM
scaler = obj["scaler"]  # StandardScaler
le = obj["le"]  # LabelEncoder

classes = np.load(CLASSES_FILE, allow_pickle=True)

# ================= DISEASE METADATA =================
DISEASE_TREATMENT = {
    "Anthracnose": {
        "cause": "Fungal infection causing dark sunken lesions on leaves and fruits.",
        "treatment": "Spray Carbendazim 0.1% or Copper Oxychloride 0.3%",
        "prevention": "Avoid overhead irrigation and prune infected parts"
    },
    "Bacterial Canker": {
        "cause": "Bacterial disease causing cracking and oozing lesions.",
        "treatment": "Spray Streptocycline (0.01%) with Copper fungicide",
        "prevention": "Use disease-free planting material"
    },
    "Powdery Mildew": {
        "cause": "White powdery fungal growth on leaves and panicles.",
        "treatment": "Spray Sulphur 0.2% or Hexaconazole",
        "prevention": "Maintain proper air circulation"
    },
    "Die Back": {
        "cause": "Fungal disease causing drying of branches from tips.",
        "treatment": "Prune affected branches and spray Carbendazim",
        "prevention": "Apply Bordeaux paste on cut surfaces"
    },
    "Sooty Mould": {
        "cause": "Fungal growth on honeydew secreted by insects.",
        "treatment": "Control insects using Imidacloprid",
        "prevention": "Manage aphids and scale insects"
    },
    "Gall Midge": {
        "cause": "Insect pest damaging flowers and young shoots.",
        "treatment": "Spray Thiamethoxam or Lambda-cyhalothrin",
        "prevention": "Timely pest monitoring"
    },
    "Cutting Weevil": {
        "cause": "Beetle cutting tender shoots and buds.",
        "treatment": "Spray Chlorpyrifos 0.05%",
        "prevention": "Remove and destroy affected shoots"
    },
    "Healthy": {
        "cause": "No disease detected.",
        "treatment": "No treatment required",
        "prevention": "Maintain good orchard hygiene"
    }
}


# ================= PREPROCESSING =================
def preprocess_image(path):
    """Load and preprocess image for EfficientNetV2"""
    img = Image.open(path).convert("RGB").resize((IMG_SIZE, IMG_SIZE))
    img = np.array(img, dtype=np.float32)
    img = tf.keras.applications.efficientnet_v2.preprocess_input(img)
    return img[None, ...]


# ================= EMBEDDING EXTRACTION =================
def extract_embedding(image_path):
    """Extract 512-dim feature vector from image"""
    x = preprocess_image(image_path)

    interpreter.set_tensor(input_details[0]["index"], x)
    interpreter.invoke()

    emb = interpreter.get_tensor(output_details[0]["index"]).reshape(-1)

    if emb.shape[0] != EMB_DIM:
        raise ValueError(f"Embedding dim mismatch: {emb.shape[0]} != {EMB_DIM}")

    return emb


# ================= PREDICTION =================
def predict_image(image_path):
    """
    Main prediction function.

    Returns:
        dict with status, predicted_label, confidence, cause, treatment, prevention
    """
    try:
        # Extract features
        emb = extract_embedding(image_path).reshape(1, -1)

        # Scale features (same as training)
        emb_scaled = scaler.transform(emb)

        # Predict with SVM
        probs = clf.predict_proba(emb_scaled)[0]
        idx = int(np.argmax(probs))

        label = le.inverse_transform([idx])[0]
        confidence = float(probs[idx])

        # ================= REJECTION LOGIC =================
        # Reject if confidence too low (blank/non-leaf images)
        if confidence < 0.50:
            return {
                "status": "rejected",
                "predicted_label": "No Valid Leaf Detected",
                "confidence": round(confidence, 4),
                "cause": "Image does not appear to be a mango leaf or confidence too low.",
                "treatment": "Please capture a clear image of a mango leaf",
                "prevention": "Ensure proper lighting and leaf is clearly visible"
            }

        # Additional check: If "Healthy" with low confidence, likely not a leaf
        if label == "Healthy" and confidence < 0.6:
            return {
                "status": "rejected",
                "predicted_label": "Unclear Image",
                "confidence": round(confidence, 4),
                "cause": "Image quality insufficient for accurate diagnosis.",
                "treatment": "Recapture with better focus on the leaf",
                "prevention": "Hold camera steady and ensure good lighting"
            }

        # Get treatment info
        info = DISEASE_TREATMENT.get(label, DISEASE_TREATMENT["Healthy"])

        return {
            "status": "success",
            "predicted_label": label,
            "confidence": round(confidence, 4),
            "cause": info["cause"],
            "treatment": info["treatment"],
            "prevention": info["prevention"]
        }

    except Exception as e:
        return {
            "status": "error",
            "predicted_label": "Error",
            "confidence": 0.0,
            "cause": str(e),
            "treatment": "Check image format and model files",
            "prevention": "Ensure proper setup"
        }