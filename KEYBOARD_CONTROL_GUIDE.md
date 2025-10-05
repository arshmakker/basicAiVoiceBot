# Keyboard Control Reference Guide

## Overview

The Voice Bot's Manual Mode provides precise keyboard control for speech recording and dialog processing. This guide covers all keyboard commands, usage patterns, and best practices.

## 🎮 Basic Commands

### Primary Commands

| Command | Action | Description |
|---------|--------|-------------|
| `s` + Enter | Start Recording | Begin audio recording from microphone |
| `t` + Enter | Stop Recording | Stop recording and process through dialog system |
| `q` + Enter | Quit | Exit the voice bot application |
| `h` + Enter | Help | Display available commands and help |

### Command Usage Pattern

```
Voice Bot> s
🔴 RECORDING STARTED
💡 Type 't' + Enter to stop recording

Voice Bot> t
⏹️  RECORDING STOPPED
📝 Transcript: 'Your speech here'
🤖 Processing through dialog system...
🔊 Response: 'Intelligent response from dialog system'
```

## 🔄 Complete Workflow

### 1. Starting the Bot

```bash
python voice_bot.py manual
```

**Expected Output:**
```
🎮 Starting Manual Voice Bot Mode
==================================
✅ Audio transcriber ready
🔊 Startup: Hey, We ready to rumble! Manual recording activated.

Voice Bot> 
```

### 2. Recording Speech

**Step 1: Start Recording**
```
Voice Bot> s
🔴 RECORDING STARTED
💡 Type 't' + Enter to stop recording
```

**Step 2: Speak Your Message**
- Speak clearly into the microphone
- Keep your message concise (1-10 seconds recommended)
- Wait for the recording to stabilize

**Step 3: Stop Recording**
```
Voice Bot> t
⏹️  RECORDING STOPPED
📊 Recording stats:
  • Duration: 3.2 seconds
  • Audio chunks: 25
  • Total size: 102400 bytes
```

### 3. Dialog Processing

**Automatic Processing:**
```
📝 Transcript: 'Hello, how are you?'
🤖 Processing through dialog system...
🔊 Response: 'Hello! I'm doing well, thank you for asking. How can I help you today?'
✅ Transcription completed
```

## 🎯 Advanced Usage Patterns

### Multi-Turn Conversations

**Example Conversation Flow:**

```
Voice Bot> s
🔴 RECORDING STARTED
Voice Bot> t
⏹️  RECORDING STOPPED
📝 Transcript: 'Hello'
🤖 Processing through dialog system...
🔊 Response: 'Hello! Nice to meet you. How can I assist you today?'

Voice Bot> s
🔴 RECORDING STARTED
Voice Bot> t
⏹️  RECORDING STOPPED
📝 Transcript: 'What's the weather like?'
🤖 Processing through dialog system...
🔊 Response: 'I'd be happy to help with weather information. Could you tell me your location?'

Voice Bot> s
🔴 RECORDING STARTED
Voice Bot> t
⏹️  RECORDING STOPPED
📝 Transcript: 'I'm in New York'
🤖 Processing through dialog system...
🔊 Response: 'Let me check the weather in New York for you...'
```

### Language Detection

**English Input:**
```
Voice Bot> s
Voice Bot> t
📝 Transcript: 'Hello, how are you?'
🌐 Language detected: English (confidence: 0.95)
🔊 Response: 'Hello! I'm doing well, thank you for asking.'
```

**Hindi Input:**
```
Voice Bot> s
Voice Bot> t
📝 Transcript: 'नमस्ते, आप कैसे हैं?'
🌐 Language detected: Hindi (confidence: 0.92)
🔊 Response: 'नमस्ते! मैं ठीक हूँ, धन्यवाद। आप कैसे हैं?'
```

**Mixed Language Input:**
```
Voice Bot> s
Voice Bot> t
📝 Transcript: 'Hello नमस्ते'
🌐 Language detected: Mixed (confidence: 0.78)
🔊 Response: 'Hello! I can understand both English and Hindi. How can I help you?'
```

## ⚠️ Error Handling

### Common Error Scenarios

#### 1. No Speech Detected
```
Voice Bot> s
🔴 RECORDING STARTED
Voice Bot> t
⏹️  RECORDING STOPPED
⚠️  No speech detected in recording
💡 Try speaking louder or closer to the microphone
```

#### 2. Transcription Failure
```
Voice Bot> s
🔴 RECORDING STARTED
Voice Bot> t
⏹️  RECORDING STOPPED
❌ Transcription failed
🔄 Fallback: "I'm sorry, I couldn't understand that. Could you please try again?"
```

#### 3. Dialog System Failure
```
Voice Bot> s
🔴 RECORDING STARTED
Voice Bot> t
⏹️  RECORDING STOPPED
📝 Transcript: 'Hello'
❌ Dialog system error
🔄 Fallback: "I'm sorry, I'm having trouble processing your request right now. Please try again."
```

### Recovery Actions

| Error Type | Recovery Action | User Action |
|------------|------------------|-------------|
| No Speech | Speak louder/closer | Try recording again |
| Transcription Failed | Check audio quality | Rephrase your message |
| Dialog System Error | Wait and retry | Try a simpler question |
| Audio Device Error | Check microphone | Restart the application |

## 🎛️ Configuration Options

### Environment Variables

```bash
# Enable debug logging
export VOICE_BOT_DEBUG="true"

# Set models directory
export VOICE_BOT_MODELS_DIR="/path/to/models"

# Set audio device
export VOICE_BOT_AUDIO_DEVICE="MacBook Air Microphone"
```

### Command Line Options

```bash
# Run with debug logging
python voice_bot.py manual --debug

# Run with specific audio device
python voice_bot.py manual --audio-device "MacBook Air Microphone"

# Run with custom models directory
python voice_bot.py manual --models-dir "/path/to/models"
```

## 📊 Performance Tips

### Recording Best Practices

1. **Optimal Distance**: 6-12 inches from microphone
2. **Clear Speech**: Speak clearly and at normal volume
3. **Quiet Environment**: Minimize background noise
4. **Stable Recording**: Wait for recording to stabilize before speaking
5. **Concise Messages**: Keep messages under 10 seconds for best results

### System Performance

1. **Memory Management**: Restart if memory usage exceeds 8GB
2. **CPU Usage**: Close other applications during heavy usage
3. **Audio Quality**: Use high-quality microphone for better transcription
4. **Network**: Ensure stable internet for dialog system processing

## 🔧 Troubleshooting

### Command Not Responding

**Problem**: Commands don't execute when pressed

**Solutions:**
- Ensure you're in Manual Mode (`python voice_bot.py manual`)
- Press Enter after each command
- Check that the bot is in interactive mode
- Use `h` + Enter to see available commands

### Recording Issues

**Problem**: Recording doesn't start or stops immediately

**Solutions:**
- Check microphone permissions (macOS: System Preferences → Security & Privacy → Privacy → Microphone)
- Verify audio device is working
- Try a different microphone
- Restart the application

### Dialog System Not Responding

**Problem**: Bot transcribes but doesn't give intelligent responses

**Solutions:**
- Ensure dialog system models are loaded
- Check for error messages in the output
- Verify the bot shows "Processing through dialog system..." message
- Try a simpler question first

### Audio Quality Issues

**Problem**: Poor transcription accuracy

**Solutions:**
- Speak closer to the microphone
- Reduce background noise
- Use a higher-quality microphone
- Check audio device settings
- Ensure stable audio environment

## 📚 Examples and Use Cases

### Basic Greeting
```
Voice Bot> s
Voice Bot> t
📝 Transcript: 'Hello'
🔊 Response: 'Hello! Nice to meet you. How can I help you today?'
```

### Question and Answer
```
Voice Bot> s
Voice Bot> t
📝 Transcript: 'What time is it?'
🔊 Response: 'I don't have access to real-time information, but I can help you with other questions!'
```

### Task Request
```
Voice Bot> s
Voice Bot> t
📝 Transcript: 'Can you help me find a restaurant?'
🔊 Response: 'I'd be happy to help you find a restaurant! What type of cuisine are you interested in?'
```

### Language Switching
```
Voice Bot> s
Voice Bot> t
📝 Transcript: 'Hello, how are you?'
🔊 Response: 'Hello! I'm doing well, thank you for asking.'

Voice Bot> s
Voice Bot> t
📝 Transcript: 'नमस्ते, आप कैसे हैं?'
🔊 Response: 'नमस्ते! मैं ठीक हूँ, धन्यवाद। आप कैसे हैं?'
```

## 🎯 Best Practices

### Do's ✅

- **Use Manual Mode** for reliable control
- **Press Enter** after each command
- **Speak clearly** and at normal volume
- **Wait for recording** to stabilize before speaking
- **Use concise messages** (1-10 seconds)
- **Check microphone permissions** before starting
- **Restart if memory usage** becomes excessive

### Don'ts ❌

- **Don't speak too fast** or too slow
- **Don't speak too far** from the microphone
- **Don't interrupt** the recording process
- **Don't use background noise** during recording
- **Don't expect perfect accuracy** in noisy environments
- **Don't ignore error messages** - they provide important feedback

## 📞 Support

If you encounter issues not covered in this guide:

1. **Check the main README** for general troubleshooting
2. **Review error messages** in the terminal output
3. **Try the help command** (`h` + Enter) for available options
4. **Restart the application** if problems persist
5. **Check system requirements** and dependencies

## 🔄 Updates

This guide is updated regularly. Check the main README for the latest version information and new features.

---

**Last Updated**: Version 2.1.0  
**Compatibility**: macOS 10.14+, Python 3.8+
