#!/usr/bin/env python3
"""
Lightweight test for dialog integration
Tests the integration without loading heavy models
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_dialog_integration_lightweight():
    """Test dialog integration without heavy model loading"""
    print("🧪 Testing Dialog Integration (Lightweight)")
    print("=" * 50)
    
    try:
        # Test 1: Import components
        print("1. Testing component imports...")
        from voice_bot.dialog_system import DialogManager
        from voice_bot.language_detection import LanguageDetector
        print("   ✅ Components imported successfully")
        
        # Test 2: Test language detection
        print("2. Testing language detection...")
        detector = LanguageDetector()
        lang, conf = detector.detect_language("Hello, how are you?")
        print(f"   ✅ Language detection: {lang} (confidence: {conf:.2f})")
        
        # Test 3: Test dialog system
        print("3. Testing dialog system...")
        dialog_manager = DialogManager()
        response = dialog_manager.process_input("Hello", "en")
        print(f"   ✅ Dialog response: '{response}'")
        
        print("\n🎉 Lightweight dialog integration tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Dialog integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_cli_integration_lightweight():
    """Test CLI integration without heavy initialization"""
    print("\n🧪 Testing CLI Integration (Lightweight)")
    print("=" * 40)
    
    try:
        # Test CLI import
        print("1. Testing CLI import...")
        from voice_bot_cli import VoiceBotCLI
        print("   ✅ CLI imported successfully")
        
        # Test CLI class exists
        print("2. Testing CLI class...")
        cli = VoiceBotCLI()
        print("   ✅ CLI class instantiated successfully")
        
        # Test methods exist
        print("3. Testing CLI methods...")
        assert hasattr(cli, 'run_manual_mode'), "run_manual_mode method missing"
        assert hasattr(cli, 'initialize_bot'), "initialize_bot method missing"
        print("   ✅ CLI methods exist")
        
        print("\n🎉 Lightweight CLI integration tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ CLI integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Starting Lightweight Dialog Integration Tests")
    print("=" * 60)
    
    # Run tests
    dialog_success = test_dialog_integration_lightweight()
    cli_success = test_cli_integration_lightweight()
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 20)
    print(f"Dialog Integration: {'✅ PASSED' if dialog_success else '❌ FAILED'}")
    print(f"CLI Integration: {'✅ PASSED' if cli_success else '❌ FAILED'}")
    
    if dialog_success and cli_success:
        print("\n🎉 All lightweight tests passed! Dialog integration is ready.")
        print("💡 Note: Full testing requires model loading which may cause memory issues.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Check the errors above.")
        sys.exit(1)
