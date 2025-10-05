#!/usr/bin/env python3
"""
Test script for keyboard-controlled dialog integration
Quick test to verify the dialog system integration works
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_dialog_integration():
    """Test the dialog integration components"""
    print("🧪 Testing Dialog Integration Components")
    print("=" * 50)
    
    try:
        # Test 1: Import VoiceBot
        print("1. Testing VoiceBot import...")
        from voice_bot import VoiceBot
        print("   ✅ VoiceBot imported successfully")
        
        # Test 2: Initialize VoiceBot
        print("2. Testing VoiceBot initialization...")
        voice_bot = VoiceBot(models_dir="models")
        print("   ✅ VoiceBot initialized successfully")
        
        # Test 3: Test language detection
        print("3. Testing language detection...")
        lang, conf = voice_bot.language_detector.detect_language("Hello, how are you?")
        print(f"   ✅ Language detection: {lang} (confidence: {conf:.2f})")
        
        # Test 4: Test dialog processing
        print("4. Testing dialog processing...")
        response = voice_bot.process_text("Hello")
        print(f"   ✅ Dialog response: '{response}'")
        
        # Test 5: Test TTS
        print("5. Testing TTS...")
        voice_bot.speak("Test message", blocking=False)
        print("   ✅ TTS working")
        
        print("\n🎉 All dialog integration tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Dialog integration test failed: {e}")
        return False

def test_cli_integration():
    """Test CLI integration"""
    print("\n🧪 Testing CLI Integration")
    print("=" * 30)
    
    try:
        # Test CLI import
        print("1. Testing CLI import...")
        from voice_bot_cli import VoiceBotCLI
        print("   ✅ CLI imported successfully")
        
        # Test CLI initialization
        print("2. Testing CLI initialization...")
        cli = VoiceBotCLI()
        print("   ✅ CLI initialized successfully")
        
        print("\n🎉 CLI integration tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ CLI integration test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Dialog Integration Tests")
    print("=" * 60)
    
    # Run tests
    dialog_success = test_dialog_integration()
    cli_success = test_cli_integration()
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 20)
    print(f"Dialog Integration: {'✅ PASSED' if dialog_success else '❌ FAILED'}")
    print(f"CLI Integration: {'✅ PASSED' if cli_success else '❌ FAILED'}")
    
    if dialog_success and cli_success:
        print("\n🎉 All tests passed! Dialog integration is ready.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Check the errors above.")
        sys.exit(1)
