# Voice Bot - Multilingual Voice Assistant

A complete Python voice bot implementation that supports real-time conversation in English and Hindi using open-source technologies. Features multiple operation modes including manual recording, automatic voice activity detection, and audio visualization.

## Features

- 🎤 **Speech Recognition**: Uses Vosk for accurate speech-to-text conversion (English & Hindi)
- 🔊 **Text-to-Speech**: Multiple TTS options including system TTS and Coqui TTS
- 🌐 **Language Detection**: Automatically detects and responds in English or Hindi
- 💬 **Dialog System**: Intelligent conversation handling with intent recognition
- 🎯 **Multiple Modes**: Simple, Smart (VAD), Manual, Full, and Test modes
- 📱 **Command Line Interface**: Easy-to-use CLI with interactive and voice modes
- 🎨 **Audio Visualization**: Real-time voice modulation display
- 🔧 **Modular Design**: Extensible architecture for adding new features
- 🛡️ **Error Handling**: Robust error handling and recovery mechanisms
- 🎮 **Manual Control**: Single-key commands for recording control

## Supported Languages

- **English (en)**: Full support with high-quality models
- **Hindi (hi)**: Complete support with Devanagari script recognition

## Requirements

### System Requirements
- Python 3.8 or higher (tested with Python 3.13)
- Microphone and speakers/headphones
- At least 4GB RAM (8GB recommended for full mode)
- macOS 10.14+ (primary development platform)

### Audio Requirements
- Working microphone (macOS may require permission grants)
- Audio output device (speakers/headphones)
- Stable audio environment for best recognition

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd basicAiVoiceBot
```

### 2. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Download Required Models

The project includes automatic model downloading. Models are stored in the `models/` directory:

- `vosk-model-en-us-0.22` - English speech recognition
- `vosk-model-hi-0.22` - Hindi speech recognition

## Quick Start

### Simple Usage

```bash
# Run with native audio access (recommended)
./run_native_audio.sh

# Or run directly
python voice_bot.py
```

### Available Modes

The voice bot supports multiple operation modes:

#### 1. **Manual Mode** (Recommended)
```bash
python voice_bot.py manual
```
- Single-key commands: `s` (start), `t` (stop), `q` (quit), `h` (help)
- Full audio transcription
- Voice feedback for recording status
- Non-blocking recording with threading

#### 2. **Smart Mode** (Auto VAD)
```bash
python voice_bot.py smart
```
- Automatic voice activity detection
- Auto start/stop recording based on speech
- 3-second silence timeout
- Real-time audio visualization

#### 3. **Simple Mode**
```bash
python voice_bot.py simple
```
- Basic startup announcement
- Minimal functionality
- Quick testing without heavy models

#### 4. **Full Mode**
```bash
python voice_bot.py full
```
- Complete voice bot with all features
- May take time to load (heavy models)
- Full dialog system

#### 5. **Test Mode**
```bash
python voice_bot.py test
```
- System diagnostics
- Audio device testing
- Component verification

## 📚 **Complete Usage Guide**

For detailed instructions on all modes and features, see the **[Complete Usage Guide](USAGE_GUIDE.md)**.

### Quick Examples

#### Manual Recording Example
```bash
python voice_bot.py manual
```

Output:
```
🎮 Starting Manual Voice Bot Mode
==================================
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

🔊 Speaking transcript...
✅ Transcription completed
```

#### Interactive Commands (Manual Mode)

When running in manual mode:

- **`s` + Enter** - Start recording
- **`t` + Enter** - Stop recording  
- **`q` + Enter** - Quit the bot
- **`h` + Enter** - Show help

## ⚙️ Configuration

### Command Line Options

```bash
python voice_bot.py [MODE] [OPTIONS]

Modes:
  manual    - Manual start/stop with single key commands
  smart     - Auto start/stop recording (recommended)
  simple    - Basic voice bot with startup announcement
  full      - Complete voice bot (may hang)
  test      - Run tests

Options:
  --help, -h     Show help message
```

### Environment Variables

```bash
export VOICE_BOT_MODELS_DIR="/path/to/models"
export VOICE_BOT_DEBUG="true"  # Enable debug logging
```

## 📁 Project Structure

```
basicAiVoiceBot/
├── voice_bot/                 # Main package
│   ├── __init__.py           # Package initialization
│   ├── asr.py                # Speech recognition module
│   ├── tts.py                # Text-to-speech module
│   ├── language_detection.py # Language detection
│   ├── dialog_system.py      # Dialog management
│   ├── audio_utils.py        # Audio processing utilities
│   ├── voice_bot.py          # Main voice bot class
│   └── logging_utils.py      # Logging configuration
├── models/                   # Vosk model files
│   ├── vosk-model-en-us-0.22/  # English model
│   └── vosk-model-hi-0.22/     # Hindi model
├── voice_bot.py              # Main entry point
├── voice_bot_cli.py          # Command line interface
├── run_native_audio.sh       # Native audio runner
├── requirements.txt          # Python dependencies
├── requirements_simple.txt   # Simplified dependencies
├── USAGE_GUIDE.md           # Complete usage guide
└── README.md                # This file
```

## 🔧 Troubleshooting

### Common Issues

#### 1. **Microphone Permission Issues (macOS)**
**Problem**: "No working microphone found" or audio not working

**Solution:**
1. Go to System Preferences → Security & Privacy → Privacy → Microphone
2. Add Terminal/iTerm/VSCode to allowed applications
3. Restart the application after granting permission

#### 2. **Bus Error / Segmentation Fault**
**Problem**: Bot crashes with "Bus error"

**Solution:**
- Use **Manual Mode** - has better error handling
- Use **Simple Mode** - avoids heavy models
- The bot continues even if transcription fails

#### 3. **High Memory Usage**
**Problem**: Python using 15GB+ memory

**Solution:**
- Use **Manual Mode** or **Simple Mode**
- Restart if memory usage becomes excessive
- The bot includes automatic memory cleanup

For more detailed troubleshooting, see the **[Complete Usage Guide](USAGE_GUIDE.md)**.

## 🧪 Testing

### Run System Tests

```bash
# Test all components
python voice_bot.py test

# Test specific functionality
python test_audio_devices.py
python test_voice_input_debug.py
```

### Manual Testing

```bash
# Test manual mode
python voice_bot.py manual

# Test smart mode
python voice_bot.py smart

# Test simple mode
python voice_bot.py simple
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly (especially on macOS)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📄 License

This project is licensed under the Private License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Vosk](https://alphacephei.com/vosk/) for speech recognition
- [Coqui TTS](https://github.com/coqui-ai/TTS) for text-to-speech
- [PyAudio](https://pypi.org/project/PyAudio/) for audio processing
- macOS system TTS for reliable voice output

## 📞 Support

For issues and questions:

1. Check the troubleshooting section above
2. Search existing issues on GitHub
3. Create a new issue with:
   - System information (macOS version, Python version)
   - Error logs from `voice_bot_debug.log`
   - Steps to reproduce the issue

## 📈 Changelog

### Version 2.0.0 (Current)
- ✅ Removed Docker support (macOS audio limitations)
- ✅ Added Manual Mode with single-key commands
- ✅ Added Smart Mode with Voice Activity Detection
- ✅ Added audio visualization and real-time feedback
- ✅ Improved error handling and memory management
- ✅ Added comprehensive testing and debugging tools
- ✅ Enhanced macOS compatibility and troubleshooting

### Version 1.0.0
- Initial release with basic voice bot functionality
- English and Hindi support with Vosk models
- Basic CLI interface and dialog system
