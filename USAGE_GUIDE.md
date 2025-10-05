# 🤖 Voice Bot - Complete Usage Guide

## 🎯 **Overview**

The Voice Bot is a multilingual voice assistant with multiple operation modes. All modes are accessed through the main `voice_bot.py` entry point.

## 🚀 **Quick Start**

```bash
# Activate virtual environment
source venv/bin/activate

# Run with native audio access (recommended)
./run_native_audio.sh

# Or run directly
python voice_bot.py
```

## 📋 **Available Modes**

| Mode | Command | Description | Best For |
|------|---------|-------------|----------|
| **Manual** | `python voice_bot.py manual` | Single-key commands for recording control | **Most users** |
| **Smart** | `python voice_bot.py smart` | Auto start/stop with voice detection | Hands-free use |
| **Simple** | `python voice_bot.py simple` | Basic startup announcement | Quick testing |
| **Full** | `python voice_bot.py full` | Complete voice bot with AI | Advanced users |
| **Test** | `python voice_bot.py test` | System diagnostics | Troubleshooting |

---

## 🎮 **Manual Mode** (Recommended)

### **What is Manual Mode?**
Manual mode gives you complete control over recording with simple text commands and **intelligent dialog responses**.

### **How to Use:**
```bash
python voice_bot.py manual
```

### **Commands:**
| Command | Action | Description |
|---------|--------|-------------|
| `s` + Enter | Start recording | Begin recording your voice |
| `t` + Enter | Stop recording | Stop recording and get intelligent response |
| `c` + Enter | Show context | Display conversation history |
| `clear` + Enter | Clear context | Clear conversation history |
| `q` + Enter | Quit | Exit the bot |
| `h` + Enter | Help | Show command help |

### **Example Session:**
```
🎮 Starting Manual Voice Bot Mode with Dialog Integration
========================================================
✅ Audio transcriber ready
🔊 Startup: Hey, We ready to rumble! Manual recording activated.

Voice Bot> s
🔴 RECORDING STARTED
💡 Type 't' + Enter to stop recording

Voice Bot> t
⏹️  RECORDING STOPPED
📊 Recording stats:
  • Duration: 5.2 seconds
  • Audio chunks: 42
  • Total size: 170496 bytes

📝 Transcript: 'Hello, how are you today?'
🌐 Language detected: en (confidence: 0.95)
🤖 Processing through dialog system...
💬 Response: Hello! I'm doing well, thank you for asking. How can I help you today?
🔊 Speaking response...
✅ Dialog processing completed

Voice Bot> c
📚 Conversation Context:
  1. Input: "Hello, how are you today?" | Language: en | Response: "Hello! I'm doing well..."
  2. Input: "What's the weather like?" | Language: en | Response: "I don't have access to current weather data..."

Voice Bot> clear
🧹 Conversation context cleared
✅ Context cleared successfully
```

### **Features:**
- ✅ **Single-key commands** - Easy to remember
- ✅ **Real-time transcription** - See what you said
- ✅ **Intelligent responses** - Bot processes through dialog system
- ✅ **Language detection** - Automatic English/Hindi detection
- ✅ **Conversation context** - Maintains conversation history
- ✅ **Recording statistics** - Duration and file size
- ✅ **Multi-language support** - English and Hindi
- ✅ **Non-blocking recording** - Can type commands while recording
- ✅ **Context management** - View and clear conversation history
- ✅ **Fallback responses** - Graceful error handling

---

## 🎯 **Dialog System Integration**

### **What is Dialog System Integration?**
The Voice Bot now includes intelligent dialog processing that understands your input and generates contextual responses instead of just echoing back what you said.

### **How Dialog Integration Works:**

#### **1. Speech Processing Flow:**
```
🎤 Record Speech → 📝 Transcribe → 🌐 Detect Language → 🤖 Process Dialog → 💬 Generate Response → 🔊 Speak Response
```

#### **2. Language Detection:**
- **Automatic Detection**: Detects English (`en`) or Hindi (`hi`)
- **Confidence Scoring**: Shows confidence level (0.0-1.0)
- **Fallback Handling**: Defaults to English if detection fails
- **Mixed Language**: Handles mixed English-Hindi input

#### **3. Dialog Processing:**
- **Intent Recognition**: Understands what you're asking for
- **Context Awareness**: Remembers previous conversation turns
- **Response Generation**: Creates intelligent, contextual responses
- **Error Handling**: Graceful fallback when dialog fails

#### **4. Conversation Context:**
- **History Tracking**: Stores input, response, language, and timestamp
- **Context Commands**: Use `c` to view history, `clear` to reset
- **Multi-turn Conversations**: Bot remembers previous exchanges
- **Context Export**: Can export conversation history

### **Dialog Integration Commands:**

| Command | Purpose | Example |
|---------|---------|---------|
| `s` | Start recording | Begin voice input |
| `t` | Stop & process | Stop recording and get intelligent response |
| `c` | Show context | Display conversation history |
| `clear` | Clear context | Reset conversation history |
| `h` | Help | Show all available commands |

### **Example Dialog Interactions:**

#### **Greeting & Introduction:**
```
Input: "Hello, how are you?"
Language: en (confidence: 0.95)
Response: "Hello! I'm doing well, thank you for asking. How can I help you today?"
```

#### **Question & Answer:**
```
Input: "What's the weather like today?"
Language: en (confidence: 0.92)
Response: "I don't have access to current weather data, but I'd be happy to help you with other questions!"
```

#### **Multilingual Support:**
```
Input: "नमस्ते, आप कैसे हैं?"
Language: hi (confidence: 0.88)
Response: "नमस्ते! मैं ठीक हूं, धन्यवाद। आप कैसे हैं?"
```

#### **Context-Aware Conversation:**
```
Turn 1:
Input: "My name is John"
Response: "Nice to meet you, John! How can I help you today?"

Turn 2:
Input: "What's my name?"
Response: "Your name is John, as you mentioned earlier."
```

### **Dialog System Features:**

#### **✅ Intelligent Responses**
- Contextual understanding of your input
- Appropriate responses based on intent
- Natural conversation flow

#### **✅ Language Support**
- English and Hindi detection
- Mixed language handling
- Automatic language switching

#### **✅ Context Management**
- Conversation history tracking
- Multi-turn conversation support
- Context-aware responses

#### **✅ Error Handling**
- Graceful fallback when dialog fails
- Fallback responses for common errors
- System continues working even if dialog fails

#### **✅ Performance Optimization**
- Fast response generation
- Efficient memory usage
- Non-blocking processing

### **Troubleshooting Dialog Integration:**

#### **Dialog System Not Responding:**
- Check if models are loaded properly
- Verify language detection is working
- Try fallback responses

#### **Language Detection Issues:**
- Speak clearly in one language
- Avoid mixed languages if possible
- Check confidence scores

#### **Context Not Working:**
- Use `c` command to check context
- Clear context with `clear` if needed
- Restart bot if context becomes corrupted

---

## 🧠 **Smart Mode** (Auto VAD)

### **What is Smart Mode?**
Smart mode automatically starts and stops recording based on your voice activity.

### **How to Use:**
```bash
python voice_bot.py smart
```

### **How It Works:**
1. **Waits for speech** - Monitors for voice activity
2. **Auto-starts recording** - When you begin speaking
3. **Auto-stops recording** - After 3 seconds of silence
4. **Provides feedback** - Shows recording status and transcript

### **Example Session:**
```
🎯 Starting Smart Voice Bot Mode
================================
🎤 Smart audio monitoring started
💤 Waiting for speech... ░░░░░░░░░░

🎤 Speech detected! Starting recording...
🔴 RECORDING ████████░░

⏸️  Silence: 1.2s (stop in 1.8s)
⏸️  Silence: 2.1s (stop in 0.9s)
⏸️  Silence: 3.0s (stop in 0.0s)
⏹️  3.0s of silence detected. Stopping recording...

📝 Transcript: 'Hello, this is a test message'
```

### **Features:**
- ✅ **Voice Activity Detection** - Automatically detects speech
- ✅ **3-second silence timeout** - Stops recording after silence
- ✅ **Real-time visualizer** - Shows current state
- ✅ **Hands-free operation** - No manual commands needed
- ✅ **Smart timing** - Perfect for voice notes and memos

---

## 🎤 **Simple Mode** (Basic)

### **What is Simple Mode?**
Simple mode provides basic functionality without heavy AI models.

### **How to Use:**
```bash
python voice_bot.py simple
```

### **Features:**
- ✅ **Startup announcement** - "Hey, We ready to rumble! Let us go"
- ✅ **Audio recording** - Records your voice
- ✅ **Low memory usage** - ~240MB vs 15GB+ for full mode
- ✅ **Fast startup** - Starts in seconds
- ✅ **Clean shutdown** - Ctrl+C works properly

### **Use Cases:**
- Quick testing of audio functionality
- Demo purposes
- Development and debugging
- When you don't need speech recognition

---

## 🤖 **Full Mode** (Complete AI)

### **What is Full Mode?**
Full mode provides complete voice bot functionality with AI models.

### **How to Use:**
```bash
python voice_bot.py full
```

### **Features:**
- ✅ **Complete dialog system** - Intelligent conversation
- ✅ **Intent recognition** - Understands what you want
- ✅ **Multi-language responses** - English and Hindi
- ✅ **Advanced AI processing** - Full voice assistant capabilities

### **⚠️ Warnings:**
- **May hang during startup** - Heavy model loading
- **High memory usage** - 15GB+ RAM required
- **Long startup time** - 30-60 seconds to load
- **May crash** - Bus errors on some systems

### **Use Cases:**
- Production voice assistant
- Advanced conversation features
- When you need full AI capabilities

---

## 🧪 **Test Mode** (Diagnostics)

### **What is Test Mode?**
Test mode runs system diagnostics to check if everything is working.

### **How to Use:**
```bash
python voice_bot.py test
```

### **What It Tests:**
- ✅ **System TTS** - macOS `say` command
- ✅ **Audio devices** - Microphone detection
- ✅ **Voice Activity Detection** - VAD functionality
- ✅ **Core components** - All major systems

### **Example Output:**
```
🧪 Running Voice Bot Tests
==========================
🔊 Testing System TTS...
✅ System TTS works

🎤 Testing Audio Detection...
✅ Found 4 input devices
  • MacBook Air Microphone
  • External Microphone

🎯 Testing Voice Activity Detection...
  Silence test: is_speaking=False ✅
  Speech test: is_speaking=True ✅

🎉 Core tests completed!
```

---

## 🔧 **Troubleshooting**

### **Common Issues:**

#### 1. **Microphone Permission Issues (macOS)**
**Problem:** "No working microphone found"

**Solution:**
1. Go to System Preferences → Security & Privacy → Privacy → Microphone
2. Add Terminal/iTerm/VSCode to allowed applications
3. Restart the application

#### 2. **Bus Error / Segmentation Fault**
**Problem:** Bot crashes with "Bus error"

**Solution:**
- Use **Manual Mode** - has better error handling
- Use **Simple Mode** - avoids heavy models
- The bot continues even if transcription fails

#### 3. **High Memory Usage**
**Problem:** Python using 15GB+ memory

**Solution:**
- Use **Manual Mode** or **Simple Mode**
- Restart if memory usage becomes excessive
- The bot includes automatic memory cleanup

#### 4. **TTS Not Working**
**Problem:** No voice output

**Solution:**
- Check if `say` command works: `say "test"`
- Manual mode uses system TTS (most reliable)
- Bot falls back gracefully if TTS fails

#### 5. **Bot Hangs on Startup**
**Problem:** Bot appears frozen

**Solution:**
- Use **Manual Mode** - most stable
- Use **Simple Mode** - lightweight alternative
- Check system resources and restart

### **Performance Tips:**

#### For Better Performance:
1. **Use Manual Mode** - Most stable and responsive
2. **Quiet Environment** - Better speech recognition
3. **Clear Speech** - Speak clearly and at moderate pace
4. **Close Other Apps** - Reduce system load

#### For Better Accuracy:
1. **Use Smart Mode** - Automatic VAD provides better timing
2. **Speak Naturally** - Don't over-enunciate
3. **Wait for Processing** - Let the bot finish before speaking again

---

## 📊 **Mode Comparison**

| Feature | Manual | Smart | Simple | Full | Test |
|---------|--------|-------|--------|------|------|
| **Startup Time** | 5-10s | 3-5s | 2-3s | 30-60s | 1-2s |
| **Memory Usage** | 500MB | 240MB | 240MB | 15GB+ | 100MB |
| **Speech Recognition** | ✅ | ✅ | ❌ | ✅ | ❌ |
| **Voice Control** | ✅ Manual | ✅ Auto | ❌ | ✅ | ❌ |
| **Transcription** | ✅ | ✅ | ❌ | ✅ | ❌ |
| **Dialog System** | ✅ | ❌ | ❌ | ✅ | ❌ |
| **Language Detection** | ✅ | ❌ | ❌ | ✅ | ❌ |
| **Context Management** | ✅ | ❌ | ❌ | ✅ | ❌ |
| **Intelligent Responses** | ✅ | ❌ | ❌ | ✅ | ❌ |
| **Reliability** | ✅ High | ✅ High | ✅ High | ⚠️ Medium | ✅ High |
| **Best For** | Most users | Hands-free | Testing | Advanced | Debug |

---

## 🎯 **Recommendations**

### **For New Users:**
Start with **Manual Mode** - it's the most stable, gives you full control, and includes intelligent dialog responses.

### **For Hands-Free Use:**
Use **Smart Mode** - automatic voice detection is perfect for voice notes (note: no dialog integration).

### **For Quick Testing:**
Use **Simple Mode** - fast startup and basic functionality.

### **For Production with Dialog:**
Use **Manual Mode** - complete dialog integration with intelligent responses and context management.

### **For Advanced AI Features:**
Use **Full Mode** - complete AI capabilities (if your system can handle it).

### **For Troubleshooting:**
Use **Test Mode** - diagnose any issues with your setup.

---

## 🚀 **Getting Started**

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Test your setup:**
   ```bash
   python voice_bot.py test
   ```

3. **Start with Manual Mode:**
   ```bash
   python voice_bot.py manual
   ```

4. **Try the commands:**
   - Type `s` + Enter to start recording
   - Speak your message
   - Type `t` + Enter to stop and get intelligent response
   - Type `c` + Enter to view conversation context
   - Type `clear` + Enter to clear conversation history
   - Type `q` + Enter to quit

**You're ready to use the Voice Bot with intelligent dialog integration!** 🎉
