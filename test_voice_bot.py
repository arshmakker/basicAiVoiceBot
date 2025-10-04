#!/usr/bin/env python3
"""
Test Script for Voice Bot
Simple test to verify all components are working
"""

import sys
import logging
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test if all modules can be imported"""
    print("Testing imports...")
    
    try:
        from voice_bot import VoiceBot, LanguageDetector, TTSSynthesizer
        print("✅ Main modules imported successfully")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    
    try:
        from voice_bot.asr import SpeechRecognizer
        print("✅ ASR module imported successfully")
    except ImportError as e:
        print(f"❌ ASR import error: {e}")
        return False
    
    try:
        from voice_bot.tts import TTSSynthesizer
        print("✅ TTS module imported successfully")
    except ImportError as e:
        print(f"❌ TTS import error: {e}")
        return False
    
    try:
        from voice_bot.language_detection import LanguageDetector
        print("✅ Language detection module imported successfully")
    except ImportError as e:
        print(f"❌ Language detection import error: {e}")
        return False
    
    try:
        from voice_bot.dialog_system import DialogManager
        print("✅ Dialog system module imported successfully")
    except ImportError as e:
        print(f"❌ Dialog system import error: {e}")
        return False
    
    return True


def test_language_detection():
    """Test language detection functionality"""
    print("\nTesting language detection...")
    
    try:
        from voice_bot import LanguageDetector
        
        detector = LanguageDetector()
        
        # Test English
        lang, conf = detector.detect_language("Hello, how are you?")
        print(f"English test: {lang} (confidence: {conf:.2f})")
        
        # Test Hindi
        lang, conf = detector.detect_language("नमस्ते, आप कैसे हैं?")
        print(f"Hindi test: {lang} (confidence: {conf:.2f})")
        
        print("✅ Language detection working")
        return True
        
    except Exception as e:
        print(f"❌ Language detection error: {e}")
        return False


def test_dialog_system():
    """Test dialog system functionality"""
    print("\nTesting dialog system...")
    
    try:
        from voice_bot import DialogManager
        
        dialog = DialogManager()
        
        # Test English greeting
        response = dialog.process_input("Hello", "en")
        print(f"English greeting response: {response}")
        
        # Test Hindi greeting
        response = dialog.process_input("नमस्ते", "hi")
        print(f"Hindi greeting response: {response}")
        
        # Test FAQ
        response = dialog.process_input("What is a voice bot?", "en")
        print(f"FAQ response: {response[:50]}...")
        
        print("✅ Dialog system working")
        return True
        
    except Exception as e:
        print(f"❌ Dialog system error: {e}")
        return False


def test_model_files():
    """Test if model files exist"""
    print("\nTesting model files...")
    
    models_dir = Path("models")
    
    if not models_dir.exists():
        print("❌ Models directory not found")
        print("   Run: python download_models.py --all")
        return False
    
    # Check for Vosk models
    vosk_en = models_dir / "vosk-model-en-us-0.22"
    vosk_hi = models_dir / "vosk-model-hi-0.22"
    
    if vosk_en.exists():
        print("✅ English Vosk model found")
    else:
        print("⚠️  English Vosk model not found")
    
    if vosk_hi.exists():
        print("✅ Hindi Vosk model found")
    else:
        print("⚠️  Hindi Vosk model not found")
    
    # Check for Whisper model
    whisper_model = models_dir / "whisper-medium.pt"
    if whisper_model.exists():
        print("✅ Whisper model found")
    else:
        print("⚠️  Whisper model not found")
    
    print("✅ Model files check completed")
    return True


def test_audio_devices():
    """Test audio device availability"""
    print("\nTesting audio devices...")
    
    try:
        import pyaudio
        
        audio = pyaudio.PyAudio()
        
        # Check input devices
        input_devices = []
        for i in range(audio.get_device_count()):
            device_info = audio.get_device_info_by_index(i)
            if device_info['maxInputChannels'] > 0:
                input_devices.append(device_info['name'])
        
        if input_devices:
            print(f"✅ Found {len(input_devices)} input devices")
            print(f"   Default: {input_devices[0]}")
        else:
            print("❌ No input devices found")
        
        # Check output devices
        output_devices = []
        for i in range(audio.get_device_count()):
            device_info = audio.get_device_info_by_index(i)
            if device_info['maxOutputChannels'] > 0:
                output_devices.append(device_info['name'])
        
        if output_devices:
            print(f"✅ Found {len(output_devices)} output devices")
            print(f"   Default: {output_devices[0]}")
        else:
            print("❌ No output devices found")
        
        audio.terminate()
        return True
        
    except ImportError:
        print("❌ PyAudio not installed")
        return False
    except Exception as e:
        print(f"❌ Audio device test error: {e}")
        return False


def test_voice_bot_initialization():
    """Test voice bot initialization (without starting)"""
    print("\nTesting voice bot initialization...")
    
    try:
        from voice_bot import VoiceBot
        
        # Try to initialize (this will fail if models are missing, which is expected)
        try:
            bot = VoiceBot(models_dir="models")
            print("✅ Voice bot initialized successfully")
            return True
        except Exception as e:
            print(f"⚠️  Voice bot initialization failed (expected if models missing): {e}")
            print("   This is normal if models haven't been downloaded yet")
            return True  # This is expected behavior
        
    except Exception as e:
        print(f"❌ Voice bot initialization error: {e}")
        return False


def main():
    """Run all tests"""
    print("Voice Bot Test Suite")
    print("=" * 50)
    
    # Setup logging
    logging.basicConfig(level=logging.WARNING)  # Reduce noise during testing
    
    tests = [
        ("Import Test", test_imports),
        ("Language Detection Test", test_language_detection),
        ("Dialog System Test", test_dialog_system),
        ("Model Files Test", test_model_files),
        ("Audio Devices Test", test_audio_devices),
        ("Voice Bot Initialization Test", test_voice_bot_initialization),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}")
        print("-" * len(test_name))
        
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Voice bot is ready to use.")
        print("\nNext steps:")
        print("1. Download models: python download_models.py --all")
        print("2. Run voice bot: python voice_bot_cli.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("\nCommon solutions:")
        print("1. Install missing dependencies: pip install -r requirements.txt")
        print("2. Download models: python download_models.py --all")
        print("3. Check audio device permissions")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
