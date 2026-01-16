# ============================================
# COMPLETE SETUP & TESTING GUIDE
# ============================================
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