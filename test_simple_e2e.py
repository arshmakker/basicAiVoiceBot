#!/usr/bin/env python3
"""
Simple End-to-End Test
Tests basic functionality without complex initialization
"""

import sys
import time
from pathlib import Path
from colorama import Fore, Style, init

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

init(autoreset=True)

def test_imports():
    """Test if all modules can be imported"""
    print(f"{Fore.CYAN}🧪 Testing Imports{Style.RESET_ALL}")
    
    try:
        from voice_bot import VoiceBot, VoiceBotError
        print(f"{Fore.GREEN}✅ VoiceBot import successful{Style.RESET_ALL}")
        return True
    except Exception as e:
        print(f"{Fore.RED}❌ VoiceBot import failed: {e}{Style.RESET_ALL}")
        return False

def test_models_directory():
    """Test if models directory exists"""
    print(f"\n{Fore.CYAN}📁 Testing Models Directory{Style.RESET_ALL}")
    
    models_dir = Path("models")
    if models_dir.exists():
        print(f"{Fore.GREEN}✅ Models directory exists{Style.RESET_ALL}")
        
        # Check for specific model files
        vosk_en = models_dir / "vosk-model-en-us-0.22"
        vosk_hi = models_dir / "vosk-model-hi-0.22"
        
        if vosk_en.exists():
            print(f"{Fore.GREEN}✅ English Vosk model found{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}⚠️  English Vosk model not found{Style.RESET_ALL}")
            
        if vosk_hi.exists():
            print(f"{Fore.GREEN}✅ Hindi Vosk model found{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}⚠️  Hindi Vosk model not found{Style.RESET_ALL}")
            
        return True
    else:
        print(f"{Fore.RED}❌ Models directory not found{Style.RESET_ALL}")
        return False

def test_audio_devices():
    """Test audio device detection"""
    print(f"\n{Fore.CYAN}🎤 Testing Audio Devices{Style.RESET_ALL}")
    
    try:
        import pyaudio
        
        p = pyaudio.PyAudio()
        device_count = p.get_device_count()
        
        input_devices = []
        output_devices = []
        
        for i in range(device_count):
            device_info = p.get_device_info_by_index(i)
            if device_info['maxInputChannels'] > 0:
                input_devices.append((i, device_info['name']))
            if device_info['maxOutputChannels'] > 0:
                output_devices.append((i, device_info['name']))
        
        p.terminate()
        
        print(f"{Fore.GREEN}✅ Found {len(input_devices)} input devices{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✅ Found {len(output_devices)} output devices{Style.RESET_ALL}")
        
        if len(input_devices) > 0:
            print(f"{Fore.GREEN}✅ Audio input available{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.RED}❌ No audio input devices found{Style.RESET_ALL}")
            return False
            
    except Exception as e:
        print(f"{Fore.RED}❌ Audio device test failed: {e}{Style.RESET_ALL}")
        return False

def test_voice_bot_creation():
    """Test voice bot creation without starting it"""
    print(f"\n{Fore.CYAN}🤖 Testing Voice Bot Creation{Style.RESET_ALL}")
    
    try:
        from voice_bot import VoiceBot
        
        # Check if models directory exists
        models_dir = Path("models")
        if not models_dir.exists():
            print(f"{Fore.RED}❌ Models directory not found{Style.RESET_ALL}")
            return False
        
        print(f"{Fore.YELLOW}⏳ Creating voice bot instance...{Style.RESET_ALL}")
        
        # Create voice bot with minimal settings
        voice_bot = VoiceBot(
            models_dir=str(models_dir),
            vosk_en_model="vosk-model-en-us-0.22",
            vosk_hi_model="vosk-model-hi-0.22",
            tts_language="en",
            use_gpu=False,
            sample_rate=16000,
            chunk_size=1024
        )
        
        print(f"{Fore.GREEN}✅ Voice bot created successfully{Style.RESET_ALL}")
        return True
        
    except Exception as e:
        print(f"{Fore.RED}❌ Voice bot creation failed: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        return False

def test_basic_text_processing():
    """Test basic text processing without audio"""
    print(f"\n{Fore.CYAN}💬 Testing Basic Text Processing{Style.RESET_ALL}")
    
    try:
        from voice_bot import VoiceBot
        
        models_dir = Path("models")
        if not models_dir.exists():
            print(f"{Fore.RED}❌ Models directory not found{Style.RESET_ALL}")
            return False
        
        voice_bot = VoiceBot(
            models_dir=str(models_dir),
            vosk_en_model="vosk-model-en-us-0.22",
            vosk_hi_model="vosk-model-hi-0.22",
            tts_language="en",
            use_gpu=False,
            sample_rate=16000,
            chunk_size=1024
        )
        
        # Test text processing
        test_inputs = [
            "Hello",
            "How are you?",
            "Goodbye"
        ]
        
        success_count = 0
        
        for test_input in test_inputs:
            print(f"{Fore.YELLOW}Testing: '{test_input}'{Style.RESET_ALL}")
            
            try:
                response = voice_bot.process_text(test_input)
                if response and len(response) > 0:
                    print(f"{Fore.GREEN}✅ Response: '{response}'{Style.RESET_ALL}")
                    success_count += 1
                else:
                    print(f"{Fore.RED}❌ No response{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")
        
        success_rate = success_count / len(test_inputs)
        print(f"{Fore.CYAN}Text processing: {success_count}/{len(test_inputs)} passed ({success_rate:.1%}){Style.RESET_ALL}")
        
        return success_rate >= 0.5  # At least 50% success
        
    except Exception as e:
        print(f"{Fore.RED}❌ Text processing test failed: {e}{Style.RESET_ALL}")
        return False

def main():
    """Run simple E2E tests"""
    print(f"{Fore.BLUE}🚀 Simple End-to-End Tests{Style.RESET_ALL}")
    print(f"{Fore.BLUE}=========================={Style.RESET_ALL}")
    
    tests = [
        ("Imports", test_imports),
        ("Models Directory", test_models_directory),
        ("Audio Devices", test_audio_devices),
        ("Voice Bot Creation", test_voice_bot_creation),
        ("Basic Text Processing", test_basic_text_processing),
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed_tests += 1
                print(f"{Fore.GREEN}✅ {test_name} PASSED{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ {test_name} FAILED{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}❌ {test_name} ERROR: {e}{Style.RESET_ALL}")
    
    # Summary
    success_rate = passed_tests / total_tests
    print(f"\n{Fore.BLUE}📊 Test Summary{Style.RESET_ALL}")
    print(f"{Fore.BLUE}==============={Style.RESET_ALL}")
    print(f"Passed: {passed_tests}/{total_tests} ({success_rate:.1%})")
    
    if success_rate >= 0.8:
        print(f"{Fore.GREEN}🎉 Simple E2E Tests PASSED{Style.RESET_ALL}")
        return True
    else:
        print(f"{Fore.RED}❌ Simple E2E Tests FAILED{Style.RESET_ALL}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)


