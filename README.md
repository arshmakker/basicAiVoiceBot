# Voice Bot - Multilingual Voice Assistant

A complete Python voice bot implementation that supports real-time conversation in English and Hindi using open-source technologies.

## Features

- 🎤 **Speech Recognition**: Uses Vosk and Whisper for accurate speech-to-text conversion
- 🔊 **Text-to-Speech**: Powered by Coqui TTS for natural-sounding speech synthesis
- 🌐 **Language Detection**: Automatically detects and responds in English or Hindi
- 💬 **Dialog System**: Intelligent conversation handling with intent recognition
- 🎯 **Intent Recognition**: Supports greeting, FAQ, small talk, and fallback responses
- 📱 **Command Line Interface**: Easy-to-use CLI with interactive and voice modes
- 🔧 **Modular Design**: Extensible architecture for adding new features
- 🛡️ **Error Handling**: Robust error handling for ASR/TTS failures

## Supported Languages

- **English (en)**: Full support with high-quality models
- **Hindi (hi)**: Complete support with Devanagari script recognition

## Requirements

### System Requirements
- Python 3.8 or higher
- Microphone and speakers/headphones
- At least 4GB RAM (8GB recommended)
- Optional: GPU for faster processing

### Operating Systems
- ✅ Linux (Ubuntu 18.04+, CentOS 7+)
- ✅ Windows 10/11
- ✅ macOS 10.14+

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

```bash
# Download all models automatically
python download_models.py --all

# Or download specific models
python download_models.py --model vosk_en
python download_models.py --model vosk_hi
python download_models.py --model whisper
```

**Note**: Model download may take 10-30 minutes depending on your internet connection.

## Quick Start

### Basic Usage

```bash
# Run voice bot with default settings
python voice_bot_cli.py
```

### Interactive Mode

```bash
# Run in interactive mode for testing
python voice_bot_cli.py --mode interactive
```

### Advanced Usage

```bash
# Run with custom settings
python voice_bot_cli.py --models-dir ./models --use-gpu --verbose
```

## Usage Examples

### Voice Commands

**English:**
- "Hello" - Greet the bot
- "How are you?" - Small talk
- "What can you do?" - Get help
- "What is a voice bot?" - Learn about voice bots
- "Goodbye" - End conversation

**Hindi:**
- "नमस्ते" - Greet the bot
- "आप कैसे हैं?" - Small talk
- "आप क्या कर सकते हैं?" - Get help
- "वॉयस बॉट क्या है?" - Learn about voice bots
- "अलविदा" - End conversation

### Interactive Commands

When running in interactive mode, you can use these commands:

- `help` - Show help information
- `status` - Display bot status
- `history` - Show conversation history
- `clear` - Clear conversation history
- `speak <text>` - Make bot speak text
- `text <text>` - Process text and get response
- `quit` - Exit the program

## Configuration

### Command Line Options

```bash
python voice_bot_cli.py [OPTIONS]

Model Configuration:
  --models-dir DIR          Directory containing model files (default: models)
  --vosk-en-model PATH      Path to English Vosk model
  --vosk-hi-model PATH      Path to Hindi Vosk model
  --whisper-model SIZE      Whisper model size: tiny, base, small, medium, large (default: medium)

TTS Configuration:
  --tts-language LANG       Default TTS language: en, hi (default: en)
  --use-gpu                 Use GPU acceleration (if available)

Audio Configuration:
  --sample-rate RATE        Audio sample rate (default: 16000)
  --chunk-size SIZE         Audio chunk size (default: 1024)

Runtime Configuration:
  --mode MODE               Run mode: voice, interactive (default: voice)
  --verbose, -v             Enable verbose logging
```

### Environment Variables

You can also set these environment variables:

```bash
export VOICE_BOT_MODELS_DIR="/path/to/models"
export VOICE_BOT_USE_GPU="true"
export VOICE_BOT_TTS_LANGUAGE="hi"
```

## Project Structure

```
basicAiVoiceBot/
├── voice_bot/                 # Main package
│   ├── __init__.py           # Package initialization
│   ├── asr.py                # Speech recognition module
│   ├── tts.py                # Text-to-speech module
│   ├── language_detection.py # Language detection
│   ├── dialog_system.py      # Dialog management
│   ├── audio_utils.py        # Audio processing utilities
│   └── voice_bot.py          # Main voice bot class
├── models/                   # Model files directory
├── voice_bot_cli.py          # Command line interface
├── download_models.py        # Model downloader script
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## API Usage

### Basic API Example

```python
from voice_bot import VoiceBot

# Initialize voice bot
bot = VoiceBot(models_dir="models")

# Set up callbacks
def on_speech(text):
    print(f"Detected: {text}")

def on_response(response):
    print(f"Response: {response}")

bot.on_speech_detected = on_speech
bot.on_response_generated = on_response

# Start the bot
with bot:
    # Bot will run until interrupted
    input("Press Enter to stop...")
```

### Text Processing Example

```python
from voice_bot import VoiceBot

bot = VoiceBot()

# Process text input
response = bot.process_text("Hello, how are you?")
print(f"Bot response: {response}")

# Speak response
bot.speak(response)
```

### Custom Language Detection

```python
from voice_bot import LanguageDetector

detector = LanguageDetector()

# Detect language
language, confidence = detector.detect_language("नमस्ते, आप कैसे हैं?")
print(f"Language: {language}, Confidence: {confidence}")
```

## Troubleshooting

### Common Issues

#### 1. Audio Device Issues

**Problem**: "No audio device found" or "PyAudio error"

**Solutions**:
```bash
# On Ubuntu/Debian
sudo apt-get install portaudio19-dev python3-pyaudio

# On CentOS/RHEL
sudo yum install portaudio-devel python3-pyaudio

# On macOS
brew install portaudio

# On Windows
pip install pipwin
pipwin install pyaudio
```

#### 2. Model Download Issues

**Problem**: Models fail to download

**Solutions**:
```bash
# Check internet connection
ping google.com

# Try downloading individual models
python download_models.py --model vosk_en
python download_models.py --model whisper

# Check available disk space
df -h
```

#### 3. GPU Issues

**Problem**: GPU not being used despite `--use-gpu` flag

**Solutions**:
```bash
# Check GPU availability
nvidia-smi

# Install GPU-enabled PyTorch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Verify GPU support
python -c "import torch; print(torch.cuda.is_available())"
```

#### 4. Permission Issues

**Problem**: "Permission denied" errors

**Solutions**:
```bash
# Make scripts executable
chmod +x voice_bot_cli.py
chmod +x download_models.py

# Check microphone permissions (Linux)
sudo usermod -a -G audio $USER
```

### Performance Optimization

#### For Better Performance:

1. **Use GPU**: Enable GPU acceleration if available
2. **Model Size**: Use smaller models for faster processing:
   ```bash
   python voice_bot_cli.py --whisper-model tiny
   ```
3. **Audio Settings**: Adjust sample rate and chunk size:
   ```bash
   python voice_bot_cli.py --sample-rate 8000 --chunk-size 512
   ```

#### For Better Accuracy:

1. **Use Larger Models**: Use larger Whisper models for better accuracy
2. **Quiet Environment**: Use in a quiet environment for better recognition
3. **Clear Speech**: Speak clearly and at moderate pace

## Development

### Adding New Intents

To add new conversation intents, modify `voice_bot/dialog_system.py`:

```python
# Add new intent patterns
Intent.NEW_INTENT: [
    r'\b(pattern1|pattern2)\b',
    r'\b(हिंदी पैटर्न)\b'
]

# Add responses
"NEW_INTENT": {
    "en": ["English response 1", "English response 2"],
    "hi": ["हिंदी जवाब 1", "हिंदी जवाब 2"]
}
```

### Adding New Languages

To add support for new languages:

1. Add language patterns to `LanguageDetector`
2. Add TTS models for the language
3. Add ASR models for the language
4. Update dialog system with new language responses

### Testing

```bash
# Run tests (if available)
python -m pytest tests/

# Test individual components
python -c "from voice_bot import LanguageDetector; print('Language detection works')"
python -c "from voice_bot import VoiceBot; print('Voice bot imports successfully')"
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Vosk](https://alphacephei.com/vosk/) for speech recognition
- [Whisper](https://github.com/openai/whisper) for additional speech recognition
- [Coqui TTS](https://github.com/coqui-ai/TTS) for text-to-speech
- [PyAudio](https://pypi.org/project/PyAudio/) for audio processing

## Support

For issues and questions:

1. Check the troubleshooting section above
2. Search existing issues on GitHub
3. Create a new issue with detailed information
4. Include system information and error logs

## Changelog

### Version 1.0.0
- Initial release
- English and Hindi support
- Vosk and Whisper ASR integration
- Coqui TTS integration
- Command line interface
- Modular architecture
- Error handling and logging
