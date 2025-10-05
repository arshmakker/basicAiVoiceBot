#!/usr/bin/env python3
"""
Ultra-Simple E2E Test
Just tests basic imports and simple functionality
"""

import sys
from pathlib import Path
from colorama import Fore, Style, init

init(autoreset=True)

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_basic_imports():
    """Test basic imports only"""
    print("🧪 Ultra-Simple E2E Test")
    print("=" * 30)
    
    try:
        print("Testing basic imports...")
        
        # Test individual module imports
        from voice_bot.language_detection import LanguageDetector
        print("✅ Language detection imported")
        
        from voice_bot.dialog_system import DialogManager
        print("✅ Dialog system imported")
        
        from voice_bot.audio_utils import AudioProcessor
        print("✅ Audio utils imported")
        
        from voice_bot.logging_utils import setup_single_line_logging
        print("✅ Logging utils imported")
        
        from voice_bot.spinner import voice_bot_spinner
        print("✅ Spinner imported")
        
        print("\n✅ All basic imports successful!")
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_simple_functionality():
    """Test very simple functionality"""
    print("\nTesting simple functionality...")
    
    try:
        # Test language detection with simple text
        from voice_bot.language_detection import LanguageDetector
        detector = LanguageDetector()
        
        result = detector.detect_language("Hello")
        print(f"✅ Language detection: {result}")
        
        # Test dialog system creation
        from voice_bot.dialog_system import DialogManager
        dialog = DialogManager()
        print("✅ Dialog manager created")
        
        # Test audio processor creation
        from voice_bot.audio_utils import AudioProcessor
        processor = AudioProcessor()
        print("✅ Audio processor created")
        
        print("\n✅ All simple functionality tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        return False

def test_models_directory():
    """Test that models directory exists"""
    print("\nTesting models directory...")
    
    try:
        models_dir = Path(__file__).parent / "models"
        
        if not models_dir.exists():
            print(f"❌ Models directory not found: {models_dir}")
            return False
        
        print(f"✅ Models directory found: {models_dir}")
        
        # Check for required model files
        en_model = models_dir / "vosk-model-en-us-0.22"
        hi_model = models_dir / "vosk-model-hi-0.22"
        
        if en_model.exists():
            print("✅ English model found")
        else:
            print("❌ English model not found")
            return False
            
        if hi_model.exists():
            print("✅ Hindi model found")
        else:
            print("❌ Hindi model not found")
            return False
        
        print("\n✅ Models directory test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Models directory test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Ultra-Simple E2E Test")
    print("=" * 40)
    
    results = []
    
    # Run tests
    results.append(test_basic_imports())
    results.append(test_simple_functionality())
    results.append(test_models_directory())
    
    # Summary
    print(f"\n📊 Test Summary")
    print("=" * 20)
    
    test_names = ["Basic Imports", "Simple Functionality", "Models Directory"]
    for i, (name, result) in enumerate(zip(test_names, results)):
        status = f"{Fore.GREEN}✅ PASSED{Style.RESET_ALL}" if result else f"{Fore.RED}❌ FAILED{Style.RESET_ALL}"
        print(f"{name}: {status}")
    
    passed = sum(results)
    total = len(results)
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print(f"{Fore.GREEN}🎉 All basic tests passed!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}⚠️ Note: Full VoiceBot testing requires model loading{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}⚠️ Memory issues prevent full e2e testing at this time{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}⚠️ Some tests failed. Check individual results above.{Style.RESET_ALL}")
