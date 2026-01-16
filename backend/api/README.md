# api/README.md
# Mango Disease Detection API - Backend

## 🚀 Quick Start (Local Testing)

### 1. Install Dependencies
```bash
cd api
pip install -r requirements.txt
```

### 2. Ensure Model Files Exist
```
api/
├── models/
│   └── efficientnetv2_b0_embedding_512.tflite  ✅
└── embeddings_cache/
    ├── svc_model.pkl  ✅
    └── classes.npy    ✅
```

### 3. Run Server
```bash
python main.py
```

Server starts at: **http://localhost:8000**

---

## 📖 Swagger UI Testing

### Open Swagger Docs
```
http://localhost:8000/docs
```

### Test Endpoints

#### 1. Health Check
```http
GET /health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "tflite_model": true,
  "svm_model": true
}
```

#### 2. Diagnose Image
```http
POST /diagnose
```

**Request Body:**
```json
{
  "image": "BASE64_ENCODED_IMAGE_HERE",
  "enable_voice": false
}
```

**Response:**
```json
{
  "status": "success",
  "predicted_label": "Anthracnose",
  "confidence": 0.9234,
  "cause": "Fungal infection causing dark sunken lesions...",
  "treatment": "Spray Carbendazim 0.1%...",
  "prevention": "Avoid overhead irrigation..."
}
```

---

## 🧪 Testing with Python

### Convert Image to Base64
```python
import base64
import requests

# Read image
with open("test_image.jpg", "rb") as f:
    img_b64 = base64.b64encode(f.read()).decode()

# Send request
response = requests.post(
    "http://localhost:8000/diagnose",
    json={
        "image": img_b64,
        "enable_voice": False  # Set True for voice output
    }
)

print(response.json())
```

---

## 🔊 Voice Output Testing

### Enable Voice (Local Only)
```python
response = requests.post(
    "http://localhost:8000/diagnose",
    json={
        "image": img_b64,
        "enable_voice": True  # 🔊 Voice enabled
    }
)
```

**Voice Device Priority:**
1. Bluetooth speaker (if connected)
2. Wired/USB speaker
3. Built-in speaker (PC/Laptop)
4. Raspberry Pi 3.5mm jack
5. HDMI audio

**On Raspberry Pi:**
```bash
# Install espeak for better voice quality
sudo apt-get install espeak pulseaudio

# Test audio
speaker-test -t wav -c 2
```

---

## ☁️ Deploy to HuggingFace Spaces

### 1. Create Space
- Go to: https://huggingface.co/spaces
- Create new Space (SDK: **Docker** or **Gradio**)

### 2. Upload Files
```
api/
├── main.py
├── inference.py
├── voice.py
├── requirements.txt
├── models/
└── embeddings_cache/
```

### 3. Create `Dockerfile` (for HF Spaces)
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 4. Update Raspberry Pi Client
Change API endpoint in your Pi client:
```python
API_URL = "https://your-space.hf.space/diagnose"
```

---

## 🐛 Troubleshooting

### Voice Not Working?
```bash
# Check audio devices (Linux)
pactl list sinks short

# Test pyttsx3
python -c "import pyttsx3; pyttsx3.speak('Test')"
```

### Model Not Loading?
- Check file paths in `inference.py`
- Ensure `.tflite` and `.pkl` files are not corrupted
- Verify permissions: `chmod +r models/* embeddings_cache/*`

### Swagger UI Not Loading?
- Clear browser cache
- Try: `http://localhost:8000/redoc` (alternative docs)

---

## 📊 API Performance

- **Inference Time:** ~300-500ms (CPU)
- **Model Size:** ~16MB (TFLite)
- **Memory Usage:** ~200MB RAM
- **Voice Latency:** Non-blocking (background thread)

---

## 🔒 Production Checklist

- [ ] Change CORS origins to specific IPs
- [ ] Add API key authentication
- [ ] Set up HTTPS (Let's Encrypt)
- [ ] Monitor with logging
- [ ] Rate limiting (10 req/min per IP)
- [ ] Disable voice on cloud (keep for Pi only)

---

## 📞 Support

**Issues?** Check:
1. Model files present
2. Dependencies installed
3. Port 8000 not blocked
4. Check logs: `uvicorn main:app --log-level debug`