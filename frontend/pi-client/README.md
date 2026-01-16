# pi-client/README.md
# Raspberry Pi Client - Frontend

## 📁 Files

```
pi-client/
├── camera_capture.py    # Camera handling
├── web_ui.html          # Web interface
├── test_api.py          # Quick test script
└── requirements.txt     # Dependencies
```

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd pi-client
pip install -r requirements.txt
```

### 2. Test Camera
```bash
python camera_capture.py
```

**Expected Output:**
```
📷 Auto-detected camera: 0
✅ Captured: test_capture.jpg
📦 Base64 length: 45892 chars
```

---

## 🌐 Use Web Interface

### Option A: Open HTML Directly
```bash
# Open in browser
firefox web_ui.html
# or
chromium-browser web_ui.html
```

### Option B: Run Local Server
```bash
python -m http.server 8080
```

Then open: **http://localhost:8080/web_ui.html**

---

## 🧪 Test API Integration

### Test with Camera
```bash
python test_api.py
```

### Test with Image File
```bash
python test_api.py path/to/mango_leaf.jpg
```

---

## ⚙️ Configuration

### Change API Endpoint

**In `web_ui.html`:**
```javascript
// Line 229
const endpoint = document.getElementById('apiEndpoint').value;
```

**In `test_api.py`:**
```python
# Line 7
API_ENDPOINT = "https://your-space.hf.space/diagnose"
```

---

## 📷 Camera Setup

### For CSI Camera (Raspberry Pi)
```bash
# Enable camera
sudo raspi-config
# → Interface Options → Camera → Enable

# Test
raspistill -o test.jpg
```

### For USB Camera
```bash
# Check device
ls /dev/video*

# Test
python camera_capture.py
```

### Camera Index Override
```bash
# Force specific camera
export CAMERA_INDEX=0
python test_api.py
```

---

## 🎯 Usage Flow

```
1. Open web_ui.html in browser
2. Set API endpoint (localhost or cloud)
3. Upload image OR capture from camera
4. Click "Diagnose"
5. View results + optional voice output
```

---

## 🐛 Troubleshooting

### Camera Not Detected?
```bash
# Check permissions
sudo usermod -a -G video $USER
logout  # and login again

# Check available cameras
v4l2-ctl --list-devices
```

### API Connection Failed?
```bash
# Test API health
curl http://localhost:8000/health

# Check if API is running
ps aux | grep "python main.py"
```

### Import Error opencv?
```bash
# On Raspberry Pi, use system package
sudo apt-get install python3-opencv

# Or reinstall
pip uninstall opencv-python
pip install opencv-python==4.8.1.78
```

---

## 🌍 Deploy on Local Network

### 1. Get Pi IP Address
```bash
hostname -I
# Example: 192.168.1.100
```

### 2. Run Local Server
```bash
python -m http.server 8080 --bind 0.0.0.0
```

### 3. Access from Other Devices
```
http://192.168.1.100:8080/web_ui.html
```

---

## 📊 Performance

- **Camera Capture:** ~0.5s
- **Image Upload:** ~0.3s
- **API Call:** ~1-2s (depending on network)
- **Total Time:** ~2-3s per diagnosis

---

## 🔐 Security Tips

- Use HTTPS for cloud API
- Don't expose Pi to public internet
- Add authentication if needed
- Rate limit API calls

---

## 📞 Next Steps

1. ✅ Test locally with `python test_api.py`
2. ✅ Open `web_ui.html` and test UI
3. ✅ Deploy backend to HuggingFace
4. ✅ Update API endpoint in frontend
5. ✅ Test end-to-end flow