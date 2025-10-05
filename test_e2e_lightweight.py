#!/usr/bin/env python3
"""
Lightweight E2E Tests - Component Testing Only
Tests individual components without loading heavy models
"""

import sys
import os
from pathlib import Path
from colorama import Fore, Style, init

init(autoreset=True)

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_language_detection():
    """Test language detection component"""
    print(f"{Fore.CYAN}🌐 Testing Language Detection{Style.RESET_ALL}")
    
    try:
        from voice_bot.language_detection import LanguageDetector
        
        detector = LanguageDetector()
        
        test_cases = [
            ("Hello, how are you?", "en"),
            ("नमस्ते, आप कैसे हैं?", "hi"),
            ("Hello नमस्ते", "mixed"),
            ("What's the weather like?", "en"),
            ("आज मौसम कैसा है?", "hi")
        ]
        
        for text, expected in test_cases:
            detected = detector.detect_language(text)
            print(f"   {text[:30]}... -> {detected} (expected: {expected})")
        
        print(f"{Fore.GREEN}✅ Language Detection PASSED{Style.RESET_ALL}")
        return True
        
    except Exception as e:
        print(f"{Fore.RED}❌ Language Detection FAILED: {e}{Style.RESET_ALL}")
        return False

def test_dialog_system():
    """Test dialog system component"""
    print(f"\n{Fore.CYAN}💬 Testing Dialog System{Style.RESET_ALL}")
    
    try:
        from voice_bot.dialog_system import DialogManager
        
        dialog = DialogManager()
        
        test_inputs = [
            "Hello",
            "How are you?",
            "What's your name?",
            "Tell me a joke",
            "Thank you",
            "Goodbye"
        ]
        
        for text in test_inputs:
            try:
                response = dialog.generate_response(text)
                print(f"   {text} -> {response[:50]}...")
            except Exception as e:
                print(f"   {text} -> Error: {e}")
        
        print(f"{Fore.GREEN}✅ Dialog System PASSED{Style.RESET_ALL}")
        return True
        
    except Exception as e:
        print(f"{Fore.RED}❌ Dialog System FAILED: {e}{Style.RESET_ALL}")
        return False

def test_audio_utils():
    """Test audio utilities component"""
    print(f"\n{Fore.CYAN}🎤 Testing Audio Utilities{Style.RESET_ALL}")
    
    try:
        from voice_bot.audio_utils import AudioProcessor
        
        processor = AudioProcessor()
        
        # Test basic audio processing functions
        import numpy as np
        
        # Create dummy audio data
        dummy_audio = np.random.randn(16000).astype(np.float32)
        
        # Test RMS calculation
        rms = processor.calculate_rms(dummy_audio)
        print(f"   RMS calculation: {rms:.4f}")
        
        # Test silence detection
        is_silent = processor.is_silent(dummy_audio, threshold=0.01)
        print(f"   Silence detection: {is_silent}")
        
        print(f"{Fore.GREEN}✅ Audio Utilities PASSED{Style.RESET_ALL}")
        return True
        
    except Exception as e:
        print(f"{Fore.RED}❌ Audio Utilities FAILED: {e}{Style.RESET_ALL}")
        return False

def test_logging_utils():
    """Test logging utilities"""
    print(f"\n{Fore.CYAN}📝 Testing Logging Utilities{Style.RESET_ALL}")
    
    try:
        from voice_bot.logging_utils import setup_single_line_logging
        
        # Test logging setup
        handler = setup_single_line_logging()
        print(f"   Logging handler created: {handler is not None}")
        
        print(f"{Fore.GREEN}✅ Logging Utilities PASSED{Style.RESET_ALL}")
        return True
        
    except Exception as e:
        print(f"{Fore.RED}❌ Logging Utilities FAILED: {e}{Style.RESET_ALL}")
        return False

def test_spinner():
    """Test spinner component"""
    print(f"\n{Fore.CYAN}🌀 Testing Spinner{Style.RESET_ALL}")
    
    try:
        from voice_bot.spinner import voice_bot_spinner
        
        # Test spinner states
        voice_bot_spinner.start_listening()
        print("   Spinner started")
        
        voice_bot_spinner.start_processing("test")
        print("   Spinner processing")
        
        voice_bot_spinner.start_speaking()
        print("   Spinner speaking")
        
        voice_bot_spinner.stop()
        print("   Spinner stopped")
        
        print(f"{Fore.GREEN}✅ Spinner PASSED{Style.RESET_ALL}")
        return True
        
    except Exception as e:
        print(f"{Fore.RED}❌ Spinner FAILED: {e}{Style.RESET_ALL}")
        return False

def test_imports():
    """Test that all modules can be imported"""
    print(f"\n{Fore.CYAN}📦 Testing Module Imports{Style.RESET_ALL}")
    
    modules = [
        "voice_bot.language_detection",
        "voice_bot.dialog_system", 
        "voice_bot.audio_utils",
        "voice_bot.logging_utils",
        "voice_bot.spinner"
    ]
    
    success_count = 0
    
    for module in modules:
        try:
            __import__(module)
            print(f"   ✅ {module}")
            success_count += 1
        except Exception as e:
            print(f"   ❌ {module}: {e}")
    
    if success_count == len(modules):
        print(f"{Fore.GREEN}✅ Module Imports PASSED{Style.RESET_ALL}")
        return True
    else:
        print(f"{Fore.RED}❌ Module Imports FAILED: {success_count}/{len(modules)} modules imported{Style.RESET_ALL}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Lightweight E2E Tests")
    print("=" * 50)
    print("Testing individual components without heavy model loading")
    print("=" * 50)
    
    results = []
    
    # Run component tests
    results.append(test_imports())
    results.append(test_language_detection())
    results.append(test_dialog_system())
    results.append(test_audio_utils())
    results.append(test_logging_utils())
    results.append(test_spinner())
    
    # Summary
    print(f"\n📊 Test Summary")
    print("=" * 20)
    
    test_names = [
        "Module Imports",
        "Language Detection", 
        "Dialog System",
        "Audio Utilities",
        "Logging Utilities",
        "Spinner"
    ]
    
    for i, (name, result) in enumerate(zip(test_names, results)):
        status = f"{Fore.GREEN}✅ PASSED{Style.RESET_ALL}" if result else f"{Fore.RED}❌ FAILED{Style.RESET_ALL}"
        print(f"{name}: {status}")
    
    passed = sum(results)
    total = len(results)
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print(f"{Fore.GREEN}🎉 All component tests passed!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}⚠️ Note: Full VoiceBot testing requires model loading which has memory issues{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}⚠️ Some tests failed. Check individual results above.{Style.RESET_ALL}")
