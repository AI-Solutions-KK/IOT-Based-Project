
# 🥭 Mango Disease Detection System

**AI-Powered Plant Disease Diagnosis with Edge Computing**

A production-ready IoT solution that combines deep learning, edge AI, and cloud deployment for real-time mango disease detection using Raspberry Pi and cloud infrastructure.

---

## 🎯 **Project Overview**

This system enables farmers and agricultural workers to diagnose mango plant diseases instantly using:
- **Raspberry Pi** with CSI/USB camera for field deployment
- **Cloud API** (HuggingFace) for scalable inference
- **Local fallback** when internet connectivity is limited
- **Voice feedback** for accessibility in low-literacy environments

The model identifies 7 common mango diseases with high accuracy and provides treatment recommendations in real-time.

---

## ✨ **Key Features**

### **AI/ML Capabilities**
- ✅ **Transfer Learning**: EfficientNetV2-B0 for feature extraction (512-dimensional embeddings)
- ✅ **Hybrid Architecture**: TensorFlow Lite + SVM classifier for edge deployment
- ✅ **Confidence Thresholding**: Rejects low-quality/non-leaf images (< 50% confidence)
- ✅ **8 Disease Classes**: Anthracnose, Bacterial Canker, Powdery Mildew, Die Back, Sooty Mould, Gall Midge, Cutting Weevil, Healthy

### **Edge Computing**
- ✅ **Raspberry Pi Optimized**: Runs on 32-bit ARM architecture
- ✅ **TFLite Inference**: ~300-500ms per image on CPU
- ✅ **Multi-Camera Support**: Auto-detects CSI, USB, or built-in webcam
- ✅ **Offline Capable**: Works without internet when using local backend

### **Cloud Deployment**
- ✅ **HuggingFace Spaces**: Dockerized FastAPI backend
- ✅ **Auto-Scaling**: Handles multiple concurrent requests
- ✅ **API Key Security**: Optional authentication for private deployments
- ✅ **CORS Enabled**: Cross-origin requests from any frontend

### **User Experience**
- ✅ **Live Camera Preview**: 10-second focus adjustment window
- ✅ **Voice Output**: Multi-device TTS (Bluetooth/wired/built-in speakers)
- ✅ **Smart Fallback**: Cloud → Local → Manual connection
- ✅ **Connection History**: Saves last 5 used local IPs
- ✅ **Mobile Responsive**: Works on phones, tablets, and desktops

---

## 🏗️ **System Architecture**

```
┌─────────────────────────────────────────────────────────┐
│                    RASPBERRY PI (Frontend)              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ CSI Camera   │→ │ Camera Server│→ │  Web UI      │ │
│  │ (Pi Cam v2)  │  │ (Flask 5001) │  │ (HTML/JS)    │ │
│  └──────────────┘  └──────────────┘  └──────┬───────┘ │
└──────────────────────────────────────────────┼─────────┘
                                               │
                                    ┌──────────▼──────────┐
                                    │  API Request        │
                                    │  (Base64 Image)     │
                                    └──────────┬──────────┘
                                               │
                        ┌──────────────────────┼──────────────────────┐
                        │                      │                      │
                ┌───────▼────────┐    ┌───────▼────────┐    ┌───────▼────────┐
                │ Cloud API      │    │ Local PC       │    │ Manual Entry   │
                │ (HuggingFace)  │    │ (FastAPI:8000) │    │ (Custom IP)    │
                └───────┬────────┘    └───────┬────────┘    └───────┬────────┘
                        │                     │                      │
                        └─────────────────────┼──────────────────────┘
                                              │
                                    ┌─────────▼─────────┐
                                    │  Inference Engine │
                                    │  • TFLite Model   │
                                    │  • SVM Classifier │
                                    │  • Rejection Logic│
                                    └─────────┬─────────┘
                                              │
                                    ┌─────────▼─────────┐
                                    │  Response         │
                                    │  • Disease Label  │
                                    │  • Confidence     │
                                    │  • Treatment      │
                                    │  • Voice Output   │
                                    └───────────────────┘
```

---

## 🧠 **Machine Learning Pipeline**

### **Training Phase** 
1. **Dataset**: Custom mango disease dataset (~2000 images)
2. **Preprocessing**: Image augmentation, resizing (224x224)
3. **Feature Extraction**: EfficientNetV2-B0 (frozen weights)
4. **Classifier**: SVM with RBF kernel
5. **Output**: TFLite model (16MB) + SVM pickle (~500KB)

### **Inference Phase** (This Repo)
```
Image → Preprocessing → TFLite (512-dim embedding) 
     → StandardScaler → SVM → Confidence Check → Result
```

**Rejection Criteria:**
- Overall confidence < 50% → "No Valid Leaf Detected"
- Healthy prediction with confidence < 60% → "Unclear Image"

---

## 🛠️ **Technology Stack**

### **Backend (API)**
| Component | Technology | Purpose |
|-----------|-----------|---------|
| Web Framework | FastAPI 0.109 | REST API with auto-docs |
| ML Inference | TensorFlow 2.13 + TFLite | Lightweight model serving |
| Classifier | Scikit-learn 1.3.2 | SVM with StandardScaler |
| Voice Output | pyttsx3 2.99 | Cross-platform TTS |
| Networking | Zeroconf, mDNS | Auto-discovery on LAN |
| Deployment | Docker, Uvicorn | Cloud + local hosting |

### **Frontend (Pi Client)**
| Component | Technology | Purpose |
|-----------|-----------|---------|
| UI | HTML5, CSS3, JavaScript | Responsive web interface |
| Camera | OpenCV 4.8.1, Flask | CSI/USB camera handling |
| Video Streaming | MJPEG over HTTP | Live camera preview |
| Storage | localStorage API | Save connection history |
| Communication | Fetch API | REST client with fallback |

### **Infrastructure**
- **Cloud**: HuggingFace Spaces (Docker SDK)
- **Edge**: Raspberry Pi 4 (2GB RAM minimum)
- **Network**: WiFi (2.4/5GHz), mDNS, HTTP/HTTPS

---

## 🚀 **Unique Features & Innovations**

### **1. Hybrid Cloud-Edge Architecture**
- **Seamless Fallback**: Automatically switches from cloud to local server
- **Zero Configuration**: Auto-discovers local backend via mDNS
- **Offline First**: Works without internet in remote farms

### **2. Multi-Camera Intelligence**
- **Auto-Detection**: CSI → USB → Built-in webcam priority
- **Live Preview**: 10-second adjustment window before capture
- **Cross-Platform**: Same code works on Pi, PC, and mobile

### **3. Confidence-Based Rejection**
- **Quality Gate**: Prevents false positives from blank/blurry images
- **User Feedback**: Clear error messages for retakes
- **Adaptive Thresholds**: Different thresholds for disease vs healthy

### **4. Voice Accessibility**
- **Multi-Device**: Auto-detects Bluetooth, wired, HDMI audio
- **Non-Blocking**: Runs in background thread
- **Silent Fallback**: Never crashes if audio unavailable

### **5. Developer Experience**
- **Swagger Docs**: Auto-generated API documentation
- **Connection History**: Saves last 5 IPs for quick reconnect
- **QR Code**: Terminal displays QR for mobile access
- **Hot-Reload**: Instant feedback during development

---

## 📊 **Performance Metrics**

| Metric | Value | Notes |
|--------|-------|-------|
| Inference Time | 300-500ms | CPU only (Pi 4) |
| Model Size | 16MB | TFLite quantized |
| Memory Usage | ~200MB | Inference engine |
| Accuracy | ~85-90% | On test dataset |
| API Latency | 1-2s | Cloud (network dependent) |
| Local Latency | <1s | Direct Pi connection |
| Camera Lag | 10s | User adjustment window |
| Startup Time | 3-5s | Backend initialization |

---

## 🎓 **Concepts & Techniques Covered**

### **Machine Learning**
- Transfer Learning (EfficientNetV2)
- Hybrid Deep Learning + Traditional ML (SVM)
- Model Quantization (TFLite)
- Confidence Calibration
- Rejection Mechanisms

### **Software Engineering**
- RESTful API Design
- Docker Containerization
- Microservices Architecture
- CORS & Security Headers
- API Key Authentication

### **IoT & Edge Computing**
- Raspberry Pi GPIO
- Camera Module Integration
- mDNS Service Discovery
- Resource-Constrained Deployment
- WiFi-Based Communication

### **Frontend Development**
- Responsive Web Design
- Fetch API with Timeouts
- WebRTC (Browser Webcam)
- MJPEG Streaming
- localStorage Persistence

### **DevOps**
- CI/CD with HuggingFace
- Environment Variables
- Multi-Platform Deployment
- Health Checks & Monitoring

---

## 📋 **Disease Database**

| Disease | Cause | Severity | Treatment |
|---------|-------|----------|-----------|
| **Anthracnose** | Fungal (Colletotrichum) | High | Carbendazim 0.1% |
| **Bacterial Canker** | Bacterial | Medium | Streptocycline 0.01% |
| **Powdery Mildew** | Fungal (Oidium) | Medium | Sulphur 0.2% |
| **Die Back** | Fungal (Lasiodiplodia) | High | Prune + Carbendazim |
| **Sooty Mould** | Fungal (secondary) | Low | Imidacloprid |
| **Gall Midge** | Insect pest | Medium | Thiamethoxam |
| **Cutting Weevil** | Insect pest | Low | Chlorpyrifos 0.05% |
| **Healthy** | None | N/A | Maintenance only |

---

## 🔒 **Security & Privacy**

- ✅ **No Data Storage**: Images processed in-memory only
- ✅ **HTTPS Support**: Encrypted transmission (cloud)
- ✅ **API Key Optional**: Private spaces need authentication
- ✅ **CORS Whitelisting**: Configurable allowed origins
- ✅ **Local Processing**: Sensitive farms can use offline mode

---

## 📦 **Project Structure**

```
mango-disease-detection/
├── backend/api/              # Cloud/Local API Server
│   ├── main.py              # FastAPI application
│   ├── inference.py         # ML inference engine
│   ├── voice.py             # TTS functionality
│   ├── models/              # TFLite model
│   └── embeddings_cache/    # SVM classifier
├── frontend/pi-client/      # Raspberry Pi Frontend
│   ├── web_ui.html          # Main UI
│   ├── camera_capture.py    # Camera server
│   └── open_ui.py           # Launcher script
└── docs/
    └── SETUP.md             # Installation guide
```

---

## 🌟 **Use Cases**

1. **Small-Scale Farmers**: Instant diagnosis in the field
2. **Agricultural Extension Workers**: Mobile consultation tool
3. **Research Institutions**: Data collection for disease tracking
4. **Agri-Tech Startups**: White-label disease detection API
5. **Educational Purposes**: Teaching ML deployment best practices

---

## 🔮 **Future Enhancements**

- [ ] Multi-language support (Hindi, Tamil, Telugu)
- [ ] GPS tagging for disease mapping
- [ ] Historical trend analysis dashboard
- [ ] SMS/WhatsApp alerts for treatment reminders
- [ ] Integration with weather APIs for preventive alerts
- [ ] Mobile app (React Native)
- [ ] Batch processing for multiple images
- [ ] Model versioning and A/B testing

---

## 📚 **References & Credits**

- **EfficientNetV2**: [Google Research Paper](https://arxiv.org/abs/2104.00298)
- **TensorFlow Lite**: [Official Documentation](https://www.tensorflow.org/lite)
- **FastAPI**: [FastAPI Framework](https://fastapi.tiangolo.com)
- **HuggingFace Spaces**: [Deployment Platform](https://huggingface.co/spaces)

---

## 📄 **License**

MIT License - See LICENSE file for details

---

## 🤝 **Contributing**

Contributions are welcome! Please refer to SETUP.md for development environment setup.

---

## 📞 **Support**

For setup instructions and troubleshooting, see **SETUP.md**

**Project Status**: ✅ Production Ready  
**Maintained**: Yes  
**Last Updated**: January 2026



**Built with ❤️ for the agricultural community**

~
---

# COMPLETE SETUP & TESTING GUIDE
# Portable System - Works on Any WiFi Network

## 📁 File Structure

```
YOUR_PROJECT/
│
├── api/                           (BACKEND - On PC)
│   ├── main.py                    ✅ Auto IP detection + mDNS
│   ├── start_server.py            ✅ Launcher with QR code
│   ├── inference.py               (No changes)
│   ├── voice.py                   (No changes)
│   ├── requirements.txt           ✅ Updated with networking
│   ├── models/
│   │   └── efficientnetv2_b0_embedding_512.tflite
│   └── embeddings_cache/
│       ├── svc_model.pkl
│       └── classes.npy
│
└── pi-client/                     (FRONTEND - On Pi/PC)
    ├── web_ui.html                ✅ Smart auto-discovery
    ├── open_ui.py                 ✅ Simple launcher
    ├── camera_capture.py          (Optional - not needed)
    ├── test_api.py                (Optional - for testing)
    └── requirements.txt           ✅ Minimal dependencies
```

---

## 🚀 PHASE 1: Test on PC (Both Backend + Frontend)

### Step 1: Setup Backend

```bash
cd api

# Install dependencies
pip install -r requirements.txt

# Start server with visual feedback
python start_server.py
```

**Expected Output:**
```
===========================================================
🥭 MANGO DISEASE DETECTION API
===========================================================

📡 Network Configuration:
   IP Address: 192.168.1.105
   Port: 8000

🌐 Access URLs:
   • Direct IP:  http://192.168.1.105:8000
   • mDNS Name:  http://mango-api.local:8000
   • Localhost:  http://localhost:8000

📖 API Documentation:
   http://192.168.1.105:8000/docs

📱 QR Code (Optional - Scan to get IP):
────────────────────────────────────────
███████████████████████████████
█  QR CODE HERE - SCAN ME      █
███████████████████████████████
────────────────────────────────────────

✅ Starting server...
💡 Tip: Frontend will auto-discover this API
🛑 Press CTRL+C to stop
===========================================================

INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 2: Setup Frontend (Same PC)

**Open new terminal:**

```bash
cd pi-client

# Install dependencies (minimal)
pip install -r requirements.txt

# Launch UI
python open_ui.py
```

**Expected Output:**
```
==================================================
🥭 MANGO DISEASE DETECTION - CLIENT
==================================================

🌐 Starting local server...
✅ Server running on port 5000

🔍 Auto-discovering API...
💡 UI will connect automatically

🌐 Opening browser: http://localhost:5000/web_ui.html

🛑 Press CTRL+C to stop
==================================================
```

**Browser will open automatically!**

### Step 3: Test All Features

1. **Auto-Discovery Test:**
   - UI should show: "✅ API Connected" with green indicator
   - Should display: "http://localhost:8000"

2. **Upload Image Test:**
   - Click "Upload Selected"
   - Choose a mango leaf image
   - Image preview should appear

3. **Webcam Capture Test:**
   - Click "📷 Capture Webcam"
   - Allow camera permission
   - Camera feed appears for 3 seconds
   - Auto-captures snapshot

4. **Diagnosis Test:**
   - Click "🔍 Diagnose"
   - Wait 2-3 seconds
   - Results appear with disease info

5. **Voice Output Test:**
   - Check "Enable Voice Output"
   - Click "🔍 Diagnose"
   - Should hear diagnosis from PC speakers

---

## 🌐 PHASE 2: Test with Raspberry Pi (Same WiFi)

### Prerequisites

- ✅ PC and Raspberry Pi on **same WiFi network**
- ✅ PC running backend (from Phase 1)
- ✅ Know your PC's IP (from start_server.py output)

### Step 1: Copy Frontend to Pi

**Option A - USB Drive:**
```bash
# On PC
cd pi-client
# Copy entire folder to USB

# On Pi
cp -r /media/usb/pi-client ~/Desktop/
```

**Option B - SSH/SCP:**
```bash
# From PC
scp -r pi-client/ pi@raspberrypi.local:~/Desktop/
```

**Option C - Git (if using):**
```bash
# On Pi
cd ~/Desktop
git clone <your-repo>
cd <repo>/pi-client
```

### Step 2: Run Frontend on Pi

```bash
cd ~/Desktop/pi-client

# Install dependencies
pip3 install -r requirements.txt

# Launch UI
python3 open_ui.py
```

**Browser opens on Pi → Auto-discovers PC's API!**

### Step 3: Verify Connection

**On Pi's browser, you should see:**
```
Status: ✅ API Connected
URL: http://192.168.1.105:8000
Log: ✅ Found at: http://192.168.1.105:8000
```

**If connection fails:**
```
Status: ❌ API Not Found
Log: Scanning local network...
```

**Manual Fix (if needed):**
- Open browser console (F12)
- Check backend IP from PC terminal
- Verify PC firewall allows port 8000

---

## 🏢 PHASE 3: Test at Different Location (Office)

### Same Steps, Different Network

1. **At Office:**
   - Connect PC to office WiFi
   - Connect Pi to **same** office WiFi

2. **Start Backend on PC:**
   ```bash
   cd api
   python start_server.py
   ```
   - Note the **new IP** (e.g., 10.0.0.50)

3. **Open Frontend on Pi:**
   ```bash
   cd pi-client
   python3 open_ui.py
   ```
   - Auto-discovers **new IP** automatically!

**No configuration changes needed! 🎉**

---

## ☁️ PHASE 4: Cloud Deployment (HuggingFace)

### Deploy Backend to Cloud

1. **Create HuggingFace Space:**
   - Go to: https://huggingface.co/spaces
   - Click "Create new Space"
   - Choose "Docker" SDK

2. **Upload Files:**
   ```
   api/
   ├── main.py
   ├── inference.py
   ├── voice.py
   ├── requirements.txt
   ├── Dockerfile          (create this)
   └── models/ + embeddings_cache/
   ```

3. **Create Dockerfile:**
   ```dockerfile
   FROM python:3.10-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   COPY . .
   EXPOSE 8000
   CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

4. **Get Cloud URL:**
   - Example: `https://your-username-mango-api.hf.space`

### Update Frontend for Cloud Fallback

**Modify web_ui.html (line 299):**
```javascript
const candidates = [
  'https://your-username-mango-api.hf.space',  // Cloud first
  'http://mango-api.local:8000',              // Local mDNS
  'http://localhost:8000'                      // Same machine
];
```

Now frontend tries:
1. ✅ Cloud API (if available)
2. ✅ Local PC (if on same network)
3. ✅ Localhost (if same machine)

---

## 🐛 Troubleshooting

### Backend Issues

**"ModuleNotFoundError: zeroconf"**
```bash
pip install zeroconf qrcode
```

**"Port 8000 already in use"**
```bash
# Find and kill process
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Pi:
lsof -ti:8000 | xargs kill -9
```

**"Model files not found"**
```bash
# Verify paths
ls api/models/
ls api/embeddings_cache/

# Should see:
# - efficientnetv2_b0_embedding_512.tflite
# - svc_model.pkl
# - classes.npy
```

### Frontend Issues

**"API Not Found" (Auto-discovery fails)**
```bash
# Manual test - from Pi's terminal
ping <PC_IP>              # Test connectivity
curl http://<PC_IP>:8000/health  # Test API

# Check PC firewall
# Windows: Allow port 8000 in Windows Defender
# Linux: sudo ufw allow 8000
```

**"Camera access denied"**
```bash
# Browser needs HTTPS for webcam (except localhost)
# Solution: Use file upload instead, or run on localhost
```

**"Voice not working"**
```bash
# Voice only works on backend PC, not in browser
# Enable in UI, but output comes from backend machine
```

### Network Issues

**Pi can't find PC**
```bash
# Verify same network
# On PC:
ipconfig    # Windows
ifconfig    # Linux

# On Pi:
ifconfig

# Both should be 192.168.x.x (same subnet)
```

**mDNS not working**
```bash
# Install avahi on Pi (should be default)
sudo apt-get install avahi-daemon

# Test mDNS
ping mango-api.local
```

---

## 📊 Performance Tips

### On Raspberry Pi

**For better performance:**
```bash
# Use lightweight browser
sudo apt-get install chromium-browser

# Increase swap (if Pi freezes)
sudo dphys-swapfile swapoff
sudo nano /etc/dphys-swapfile
# Set: CONF_SWAPSIZE=2048
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
```

### On PC Backend

**For faster inference:**
```bash
# Use GPU (if available)
pip install tensorflow-gpu==2.15.0

# Or use lighter model (trade accuracy for speed)
```

---

## ✅ Success Checklist

### Phase 1 (PC Testing):
- [ ] Backend starts without errors
- [ ] Frontend opens in browser
- [ ] Green "API Connected" indicator
- [ ] Can upload images
- [ ] Can capture from webcam
- [ ] Diagnosis returns results
- [ ] Voice output works (optional)

### Phase 2 (Pi + PC):
- [ ] PC and Pi on same WiFi
- [ ] Frontend auto-discovers PC
- [ ] Can diagnose from Pi
- [ ] Results display correctly

### Phase 3 (Different Location):
- [ ] Works at office/home without changes
- [ ] Auto-discovers new IP

### Phase 4 (Cloud):
- [ ] Backend deployed to HuggingFace
- [ ] Frontend tries cloud first
- [ ] Falls back to local if cloud fails

---

## 🎯 Quick Commands Reference

**Start Backend:**
```bash
cd api && python start_server.py
```

**Start Frontend:**
```bash
cd pi-client && python open_ui.py
```

**Test API Health:**
```bash
curl http://localhost:8000/health
```

**Get PC IP:**
```bash
# Windows
ipconfig | findstr IPv4

# Linux/Mac
ifconfig | grep "inet "
```

---

## 📞 Need Help?

**Common Questions:**

1. **Q: Do I need to configure IP addresses?**
   - A: No! Auto-discovery handles it.

2. **Q: Can I use this without internet?**
   - A: Yes! Works on local WiFi only.

3. **Q: Does Pi need camera module?**
   - A: No! UI uses browser webcam or file upload.

4. **Q: Can multiple Pis connect to one PC?**
   - A: Yes! Backend supports multiple clients.

5. **Q: What if I change WiFi networks?**
   - A: Just restart - auto-discovery finds new IP.

---

**🎉 You're all set! Test each phase and confirm it works before moving to the next.**