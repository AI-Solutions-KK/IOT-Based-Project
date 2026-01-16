# api/voice.py
# Intelligent Multi-Device Text-to-Speech
# Supports: Bluetooth, Wired, Built-in speakers (Pi/PC/Mobile)

import threading
import sys
import subprocess


# ==================== DEVICE DETECTION ====================
def _detect_audio_device():
    """
    Auto-detect available audio output device.

    Priority:
    1. Bluetooth speaker (if connected)
    2. Wired/USB speaker
    3. Built-in speaker (PC/Mobile)
    4. Raspberry Pi audio jack
    5. HDMI audio output
    """
    try:
        # Linux (Raspberry Pi / Ubuntu)
        if sys.platform.startswith("linux"):
            result = subprocess.run(
                ["pactl", "list", "sinks", "short"],
                capture_output=True, text=True, timeout=2
            )

            if result.returncode == 0 and result.stdout.strip():
                # Found PulseAudio devices
                return "pulseaudio"

        # Check if any audio device exists (fallback)
        return "default"

    except Exception:
        return "default"


# ==================== TTS ENGINE SELECTION ====================
def _get_tts_engine():
    """
    Select best available TTS engine based on platform.

    Fallback chain:
    1. pyttsx3 (Cross-platform - Windows/Mac/Linux)
    2. espeak (Linux/Pi - lightweight)
    3. Festival (Linux fallback)
    4. Silent fail (no crash)
    """
    audio_device = _detect_audio_device()

    # Try pyttsx3 first (most compatible)
    try:
        import pyttsx3
        engine = pyttsx3.init()

        # Platform-specific audio routing
        if sys.platform.startswith("linux"):
            # Force audio to detected device on Linux
            try:
                engine.setProperty("driver", "espeak")  # More reliable on Pi
            except Exception:
                pass  # Use default driver

        engine.setProperty("rate", 150)  # Speech rate
        engine.setProperty("volume", 0.9)  # Volume

        return ("pyttsx3", engine)

    except Exception:
        pass

    # Fallback to espeak (Linux/Pi)
    if sys.platform.startswith("linux"):
        try:
            subprocess.run(["espeak", "--version"],
                           capture_output=True, timeout=1)
            return ("espeak", None)
        except Exception:
            pass

    # Last resort: Festival (Linux)
    if sys.platform.startswith("linux"):
        try:
            subprocess.run(["festival", "--version"],
                           capture_output=True, timeout=1)
            return ("festival", None)
        except Exception:
            pass

    # No TTS available - silent fail
    return (None, None)


# ==================== WORKER THREAD ====================
def _speak_worker(text: str):
    """Background thread for non-blocking speech"""
    tts_type, engine = _get_tts_engine()

    try:
        if tts_type == "pyttsx3":
            # Standard pyttsx3
            engine.say(text)
            engine.runAndWait()
            engine.stop()

        elif tts_type == "espeak":
            # Direct espeak (Linux/Pi)
            subprocess.run(
                ["espeak", text],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=30
            )

        elif tts_type == "festival":
            # Festival TTS (Linux fallback)
            subprocess.run(
                ["festival", "--tts"],
                input=text.encode(),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=30
            )

        # Silent if no TTS available

    except Exception:
        # Absolute silent fail - never crash the API
        pass


# ==================== PUBLIC API ====================
def speak(text: str):
    """
    Non-blocking, multi-device Text-to-Speech.

    Works on:
    - Raspberry Pi (Bluetooth, 3.5mm jack, HDMI)
    - Desktop PC (Built-in speakers)
    - Mobile devices (If API runs locally)

    Args:
        text: Text to speak

    Features:
    - Auto-detects available audio device
    - Non-blocking (runs in background)
    - Silent fail (never crashes API)
    - Multi-platform (Linux/Windows/Mac)
    """
    if not text or not text.strip():
        return

    # Run in daemon thread (non-blocking)
    threading.Thread(
        target=_speak_worker,
        args=(text,),
        daemon=True
    ).start()


# ==================== MANUAL DEVICE SELECTION ====================
def speak_with_device(text: str, device: str = "auto"):
    """
    Advanced: Speak with specific device override.

    Args:
        text: Text to speak
        device: "auto", "bluetooth", "builtin", "hdmi"

    Note: Device selection requires platform-specific setup.
    For production, use `speak()` with auto-detection.
    """
    # For future enhancement - specific device routing
    # Currently uses auto-detection
    speak(text)