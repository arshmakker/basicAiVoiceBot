# macOS Installation Guide for Voice Bot

## 🍎 macOS-Specific Installation Steps

Since you're on macOS, here's a step-by-step guide to fix the installation issues:

### Step 1: Install Homebrew (if not already installed)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Step 2: Install PortAudio

```bash
brew install portaudio
```

### Step 3: Install Python Dependencies

**Option A: Use the macOS helper script**
```bash
python install_macos.py
```

**Option B: Manual installation**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install basic dependencies first
pip install numpy scipy requests tqdm colorama langdetect

# Install PyAudio (this is the tricky one)
pip install pyaudio

# If PyAudio fails, try:
pip install --global-option='build_ext' --global-option='-I/opt/homebrew/include' --global-option='-L/opt/homebrew/lib' pyaudio

# Install remaining dependencies
pip install vosk>=0.3.38
pip install openai-whisper>=20231117
pip install TTS>=0.20.6
pip install librosa>=0.9.0
pip install soundfile>=0.10.0
pip install pygame>=2.1.0
pip install webrtcvad>=2.0.10
pip install pydub>=0.25.1
```

### Step 4: Alternative PyAudio Installation

If PyAudio still fails, try these alternatives:

**Option 1: Use conda**
```bash
# Install conda first, then:
conda install pyaudio
```

**Option 2: Use system Python**
```bash
# Install with system Python (not in virtual environment)
python3 -m pip install pyaudio
```

**Option 3: Skip PyAudio for now**
```bash
# Continue without PyAudio - you can test other components
# PyAudio is only needed for microphone input
```

### Step 5: Download Models

```bash
# Activate virtual environment
source venv/bin/activate

# Download models
python download_models.py --all
```

### Step 6: Test Installation

```bash
# Run tests
python test_voice_bot.py
```

## 🔧 Troubleshooting

### PyAudio Installation Issues

**Error**: `fatal error: 'portaudio.h' file not found`

**Solution**:
```bash
# Make sure portaudio is installed
brew install portaudio

# Set environment variables
export LDFLAGS="-L/opt/homebrew/lib"
export CPPFLAGS="-I/opt/homebrew/include"

# Try installing again
pip install pyaudio
```

### Vosk Version Issues

**Error**: `Could not find a version that satisfies the requirement vosk>=0.3.45`

**Solution**: The requirements.txt has been updated to use `vosk>=0.3.38` which is available.

### Permission Issues

**Error**: Permission denied when installing packages

**Solution**:
```bash
# Use --user flag
pip install --user pyaudio

# Or fix permissions
sudo chown -R $(whoami) /usr/local/lib/python3.x/site-packages/
```

## 🚀 Quick Start After Installation

Once everything is installed:

```bash
# Activate virtual environment
source venv/bin/activate

# Test the installation
python test_voice_bot.py

# Run voice bot
python voice_bot_cli.py --mode interactive
```

## 📱 Testing Without Microphone

If PyAudio installation continues to fail, you can still test the bot in text mode:

```bash
python voice_bot_cli.py --mode interactive
```

Then use commands like:
- `text Hello, how are you?`
- `text नमस्ते, आप कैसे हैं?`
- `speak Hello world`

This will test the language detection, dialog system, and TTS without needing microphone input.

## 🆘 Still Having Issues?

If you're still having trouble:

1. **Try conda instead of pip**:
   ```bash
   conda create -n voicebot python=3.9
   conda activate voicebot
   conda install pyaudio
   pip install -r requirements_simple.txt
   ```

2. **Use Docker** (if available):
   ```bash
   # Create a Dockerfile with all dependencies
   # This avoids macOS-specific issues
   ```

3. **Skip audio input for now**:
   - Focus on testing the dialog system and TTS
   - Add microphone support later

Let me know which step you'd like to try first!
