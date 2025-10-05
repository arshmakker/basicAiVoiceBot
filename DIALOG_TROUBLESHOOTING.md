# Dialog Integration Troubleshooting Guide

## Overview

This guide helps you troubleshoot issues with the keyboard-controlled dialog integration in the Voice Bot. It covers common problems, solutions, and diagnostic steps.

## 🔍 Quick Diagnostic Checklist

Before diving into specific issues, run through this checklist:

- [ ] Are you using Manual Mode? (`python voice_bot.py manual`)
- [ ] Is the microphone working? (Test with `s` + Enter)
- [ ] Are you pressing Enter after each command?
- [ ] Is the dialog system showing "Processing through dialog system..."?
- [ ] Are there any error messages in the terminal?

## 🚨 Common Issues and Solutions

### Issue 1: Bot Transcribes But Doesn't Give Intelligent Responses

**Symptoms:**
- Bot transcribes speech correctly
- Response is just an echo: "I heard you say: [transcript]"
- No intelligent dialog processing

**Root Cause:** Dialog system integration not working

**Solutions:**

1. **Verify Manual Mode:**
   ```bash
   python voice_bot.py manual
   ```
   Ensure you see: "Manual recording activated"

2. **Check Dialog Processing:**
   Look for this message after pressing `t`:
   ```
   🤖 Processing through dialog system...
   ```
   If missing, dialog integration is not working.

3. **Test Dialog System:**
   ```bash
   # Test dialog system directly
   python -c "from voice_bot.dialog_system import DialogManager; dm = DialogManager(); print(dm.generate_response('Hello'))"
   ```

4. **Check Model Loading:**
   Ensure dialog system models are loaded:
   ```
   ✅ Dialog system ready
   ```

### Issue 2: Keyboard Commands Not Responding

**Symptoms:**
- Pressing `s` or `t` does nothing
- No recording starts/stops
- Commands appear to be ignored

**Root Cause:** Keyboard input not being processed

**Solutions:**

1. **Verify Interactive Mode:**
   Ensure you see the prompt:
   ```
   Voice Bot> 
   ```

2. **Press Enter After Commands:**
   ```
   Voice Bot> s
   [Press Enter]
   Voice Bot> t
   [Press Enter]
   ```

3. **Check Help Command:**
   ```
   Voice Bot> h
   [Press Enter]
   ```
   Should show available commands.

4. **Restart Application:**
   ```bash
   # Kill any running processes
   pkill -f voice_bot
   
   # Restart
   python voice_bot.py manual
   ```

### Issue 3: Recording Starts But Stops Immediately

**Symptoms:**
- Recording starts with `s`
- Stops immediately without user input
- No audio captured

**Root Cause:** Audio recording issues

**Solutions:**

1. **Check Microphone Permissions (macOS):**
   ```
   System Preferences → Security & Privacy → Privacy → Microphone
   ```
   Add Terminal/iTerm/VSCode to allowed applications.

2. **Test Microphone:**
   ```bash
   # Test microphone directly
   python -c "import pyaudio; p = pyaudio.PyAudio(); print('Microphone available:', p.get_device_count())"
   ```

3. **Check Audio Device:**
   ```bash
   # List available audio devices
   python -c "import pyaudio; p = pyaudio.PyAudio(); [print(f'{i}: {p.get_device_info_by_index(i)['name']}') for i in range(p.get_device_count())]"
   ```

4. **Use Specific Audio Device:**
   ```bash
   python voice_bot.py manual --audio-device "MacBook Air Microphone"
   ```

### Issue 4: Transcription Fails or Is Inaccurate

**Symptoms:**
- No transcript generated
- Incorrect transcript
- "No speech detected" message

**Root Cause:** Speech recognition issues

**Solutions:**

1. **Check Audio Quality:**
   - Speak closer to microphone (6-12 inches)
   - Reduce background noise
   - Speak clearly and at normal volume

2. **Verify Models:**
   ```bash
   ls -la models/
   ```
   Should show:
   ```
   vosk-model-en-us-0.22/
   vosk-model-hi-0.22/
   ```

3. **Test Speech Recognition:**
   ```bash
   # Test with simple phrase
   python -c "from voice_bot.asr import SpeechRecognizer; sr = SpeechRecognizer(); print(sr.recognize_speech(b'dummy_audio'))"
   ```

4. **Check Language Detection:**
   Ensure language detection is working:
   ```
   🌐 Language detected: English (confidence: 0.95)
   ```

### Issue 5: Dialog System Errors

**Symptoms:**
- "Dialog system error" message
- Fallback responses instead of intelligent ones
- System crashes during processing

**Root Cause:** Dialog system failure

**Solutions:**

1. **Check Dialog System Status:**
   Look for initialization messages:
   ```
   ✅ Dialog system ready
   ```

2. **Test Dialog System:**
   ```bash
   python -c "from voice_bot.dialog_system import DialogManager; dm = DialogManager(); print(dm.generate_response('Hello'))"
   ```

3. **Check Dependencies:**
   ```bash
   pip list | grep -E "(transformers|torch|numpy)"
   ```

4. **Restart with Debug:**
   ```bash
   python voice_bot.py manual --debug
   ```

### Issue 6: Memory Issues

**Symptoms:**
- High memory usage (8GB+)
- System slowdown
- Application crashes

**Root Cause:** Memory leaks or excessive resource usage

**Solutions:**

1. **Monitor Memory:**
   ```bash
   # Check memory usage
   ps aux | grep voice_bot
   ```

2. **Use Lightweight Mode:**
   ```bash
   python voice_bot.py simple
   ```

3. **Restart Application:**
   ```bash
   # Kill and restart
   pkill -f voice_bot
   python voice_bot.py manual
   ```

4. **Check System Resources:**
   ```bash
   # Check available memory
   vm_stat
   ```

## 🔧 Advanced Troubleshooting

### Debug Mode

Enable debug logging for detailed information:

```bash
python voice_bot.py manual --debug
```

**Debug Output Example:**
```
DEBUG: Audio recording started
DEBUG: Audio chunk received: 1024 bytes
DEBUG: Speech detected in audio
DEBUG: Transcribing audio...
DEBUG: Transcript: 'Hello'
DEBUG: Processing through dialog system...
DEBUG: Dialog response generated: 'Hello! How can I help you?'
```

### System Diagnostics

Run comprehensive system tests:

```bash
# Test all components
python voice_bot.py test

# Test specific functionality
python test_audio_devices.py
python test_voice_input_debug.py
```

### Log Analysis

Check log files for errors:

```bash
# Check debug log
tail -f voice_bot_debug.log

# Check for specific errors
grep -i "error\|exception\|failed" voice_bot_debug.log
```

## 🎯 Performance Optimization

### System Requirements

**Minimum:**
- Python 3.8+
- 4GB RAM
- Working microphone
- macOS 10.14+

**Recommended:**
- Python 3.13
- 8GB RAM
- High-quality microphone
- macOS 12+

### Optimization Tips

1. **Close Unnecessary Applications:**
   - Free up memory and CPU
   - Reduce background noise

2. **Use High-Quality Audio:**
   - External microphone
   - Quiet environment
   - Stable audio setup

3. **Optimize Recording:**
   - Keep messages concise (1-10 seconds)
   - Speak clearly and at normal volume
   - Wait for recording to stabilize

4. **Monitor Resources:**
   - Check memory usage regularly
   - Restart if usage exceeds 8GB
   - Monitor CPU usage

## 🆘 Emergency Recovery

### Complete Reset

If all else fails:

```bash
# 1. Kill all processes
pkill -f voice_bot

# 2. Clear temporary files
rm -rf /tmp/voice_bot_*

# 3. Restart with simple mode
python voice_bot.py simple

# 4. Test basic functionality
# Press 's', speak, press 't'

# 5. If working, try manual mode
python voice_bot.py manual
```

### Fallback Mode

Use simple mode as fallback:

```bash
python voice_bot.py simple
```

This mode:
- Avoids heavy models
- Uses basic functionality
- Provides reliable operation
- Good for testing

## 📞 Getting Help

### Before Asking for Help

1. **Run Diagnostics:**
   ```bash
   python voice_bot.py test
   ```

2. **Check Logs:**
   ```bash
   tail -20 voice_bot_debug.log
   ```

3. **Try Simple Mode:**
   ```bash
   python voice_bot.py simple
   ```

4. **Document the Issue:**
   - Error messages
   - Steps to reproduce
   - System information

### Information to Provide

When reporting issues:

1. **System Information:**
   - macOS version
   - Python version
   - Available memory

2. **Error Details:**
   - Complete error messages
   - Steps to reproduce
   - Expected vs actual behavior

3. **Log Files:**
   - `voice_bot_debug.log`
   - Terminal output
   - System logs

4. **Test Results:**
   - Output of `python voice_bot.py test`
   - Audio device information
   - Model status

## 🔄 Updates and Maintenance

### Regular Maintenance

1. **Update Dependencies:**
   ```bash
   pip install -r requirements.txt --upgrade
   ```

2. **Check Model Updates:**
   ```bash
   # Check for model updates
   ls -la models/
   ```

3. **Clear Logs:**
   ```bash
   # Clear old log files
   rm -f voice_bot_debug.log.*
   ```

4. **Test Functionality:**
   ```bash
   python voice_bot.py test
   ```

### Version Updates

Check for updates:
```bash
git pull origin main
pip install -r requirements.txt
```

---

**Last Updated**: Version 2.1.0  
**Compatibility**: macOS 10.14+, Python 3.8+
