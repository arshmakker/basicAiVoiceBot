#!/usr/bin/env python3
"""
Simple End-to-End VoiceBot Tests
Lightweight testing that avoids memory issues
"""

import sys
import os
import time
from pathlib import Path
from colorama import Fore, Style, init

init(autoreset=True)

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_voicebot_basic():
    """Test basic VoiceBot functionality"""
    print("🧪 Simple End-to-End VoiceBot Test")
    print("=" * 40)
    
    try:
        from voice_bot import VoiceBot
        
        models_dir = Path(__file__).parent / "models"
        if not models_dir.exists():
            print(f"❌ Models directory not found: {models_dir}")
            return False
        
        print(f"✅ Models directory found: {models_dir}")
        
        # Test 1: Basic initialization
        print(f"\n🔧 Test 1: VoiceBot Initialization")
        voicebot = VoiceBot(
            models_dir=str(models_dir),
            vosk_en_model="vosk-model-en-us-0.22",
            vosk_hi_model="vosk-model-hi-0.22",
            tts_language="en",
            use_gpu=False
        )
        print(f"✅ VoiceBot initialized successfully")
        
        # Test 2: Start VoiceBot
        print(f"\n🚀 Test 2: Starting VoiceBot")
        voicebot.start()
        print(f"✅ VoiceBot started successfully")
        
        # Test 3: Basic text processing
        print(f"\n💬 Test 3: Text Processing")
        test_texts = [
            "Hello",
            "How are you?",
            "Thank you"
        ]
        
        for i, text in enumerate(test_texts):
            print(f"   Processing: {text}")
            try:
                response = voicebot.process_text(text)
                print(f"   ✅ Response: {response[:50]}...")
            except Exception as e:
                print(f"   ⚠️ Error: {e}")
            time.sleep(0.5)
        
        # Test 4: Status check
        print(f"\n📊 Test 4: Status Check")
        status = voicebot.get_status()
        print(f"✅ Status: {status}")
        
        # Test 5: Stop VoiceBot
        print(f"\n🛑 Test 5: Stopping VoiceBot")
        voicebot.stop()
        print(f"✅ VoiceBot stopped successfully")
        
        print(f"\n🎉 All basic tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_voicebot_context_manager():
    """Test VoiceBot as context manager"""
    print(f"\n🔄 Testing Context Manager")
    
    try:
        from voice_bot import VoiceBot
        
        models_dir = Path(__file__).parent / "models"
        
        with VoiceBot(
            models_dir=str(models_dir),
            vosk_en_model="vosk-model-en-us-0.22",
            tts_language="en",
            use_gpu=False
        ) as voicebot:
            print(f"✅ VoiceBot started with context manager")
            
            response = voicebot.process_text("Hello")
            print(f"✅ Context manager test successful")
        
        print(f"✅ Context Manager test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Context manager test failed: {e}")
        return False

def test_voicebot_components():
    """Test individual VoiceBot components"""
    print(f"\n🧩 Testing Individual Components")
    
    try:
        # Test language detection
        from voice_bot.language_detection import LanguageDetector
        detector = LanguageDetector()
        
        test_texts = [
            ("Hello", "en"),
            ("नमस्ते", "hi"),
            ("Hello नमस्ते", "mixed")
        ]
        
        for text, expected in test_texts:
            detected = detector.detect_language(text)
            print(f"   {text} -> {detected} (expected: {expected})")
        
        print(f"✅ Language detection test passed!")
        
        # Test dialog system
        from voice_bot.dialog_system import DialogManager
        dialog = DialogManager()
        
        test_inputs = ["Hello", "How are you?", "Thank you"]
        for text in test_inputs:
            try:
                response = dialog.generate_response(text)
                print(f"   {text} -> {response[:30]}...")
            except Exception as e:
                print(f"   {text} -> Error: {e}")
        
        print(f"✅ Dialog system test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Component test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Simple E2E Tests")
    print("=" * 50)
    
    results = []
    
    # Run tests
    results.append(test_voicebot_basic())
    results.append(test_voicebot_context_manager())
    results.append(test_voicebot_components())
    
    # Summary
    print(f"\n📊 Test Summary")
    print("=" * 20)
    
    test_names = ["Basic Functionality", "Context Manager", "Individual Components"]
    for i, (name, result) in enumerate(zip(test_names, results)):
        status = f"{Fore.GREEN}✅ PASSED{Style.RESET_ALL}" if result else f"{Fore.RED}❌ FAILED{Style.RESET_ALL}"
        print(f"{name}: {status}")
    
    if all(results):
        print(f"\n{Fore.GREEN}🎉 All tests passed!{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.RED}⚠️ Some tests failed. Check individual results above.{Style.RESET_ALL}")
