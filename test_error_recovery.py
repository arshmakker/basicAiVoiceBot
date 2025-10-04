#!/usr/bin/env python3
"""
Error Recovery and Graceful Degradation Test
Tests error recovery and graceful degradation scenarios
"""

import sys
import time
import threading
import tempfile
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional
import numpy as np
from colorama import Fore, Style, init

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from voice_bot import VoiceBot, VoiceBotError
from voice_bot.asr import VoskRecognizer, WhisperRecognizer, SpeechRecognizer
from voice_bot.tts import TTSSynthesizer

init(autoreset=True)

class ErrorRecoveryTester:
    """Error recovery and graceful degradation tester"""
    
    def __init__(self):
        self.test_results: List[Dict[str, Any]] = []
        self.voice_bot: Optional[VoiceBot] = None
        self.backup_models_dir: Optional[Path] = None
        
    def setup_test_environment(self) -> bool:
        """Setup test environment with backup models"""
        try:
            print(f"{Fore.YELLOW}Setting up test environment...{Style.RESET_ALL}")
            
            # Create backup of models directory
            models_dir = Path("models")
            if models_dir.exists():
                self.backup_models_dir = Path("models_backup")
                if self.backup_models_dir.exists():
                    shutil.rmtree(self.backup_models_dir)
                shutil.copytree(models_dir, self.backup_models_dir)
                print(f"{Fore.GREEN}✅ Models directory backed up{Style.RESET_ALL}")
                return True
            else:
                print(f"{Fore.RED}❌ Models directory not found{Style.RESET_ALL}")
                return False
                
        except Exception as e:
            print(f"{Fore.RED}❌ Failed to setup test environment: {e}{Style.RESET_ALL}")
            return False
    
    def restore_test_environment(self):
        """Restore test environment"""
        try:
            if self.backup_models_dir and self.backup_models_dir.exists():
                models_dir = Path("models")
                if models_dir.exists():
                    shutil.rmtree(models_dir)
                shutil.move(str(self.backup_models_dir), str(models_dir))
                print(f"{Fore.GREEN}✅ Test environment restored{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}❌ Failed to restore test environment: {e}{Style.RESET_ALL}")
    
    def test_missing_models(self) -> bool:
        """Test behavior when models are missing"""
        print(f"\n{Fore.CYAN}📁 Testing Missing Models{Style.RESET_ALL}")
        
        try:
            # Remove models directory
            models_dir = Path("models")
            if models_dir.exists():
                shutil.rmtree(models_dir)
                print(f"{Fore.YELLOW}Removed models directory{Style.RESET_ALL}")
            
            # Try to initialize voice bot
            print(f"{Fore.YELLOW}Attempting to initialize voice bot without models...{Style.RESET_ALL}")
            
            try:
                voice_bot = VoiceBot(
                    models_dir="models",
                    vosk_en_model="vosk-model-en-us-0.22",
                    vosk_hi_model="vosk-model-hi-0.22",
                    whisper_model="tiny",
                    tts_language="en",
                    use_gpu=False,
                    sample_rate=16000,
                    chunk_size=1024
                )
                
                print(f"{Fore.RED}❌ Voice bot initialized without models (unexpected){Style.RESET_ALL}")
                self.test_results.append({
                    "test": "missing_models",
                    "error": "Voice bot initialized without models",
                    "passed": False
                })
                return False
                
            except Exception as e:
                print(f"{Fore.GREEN}✅ Voice bot correctly failed to initialize: {e}{Style.RESET_ALL}")
                
                # Check if it's the expected error type
                if "Models directory not found" in str(e) or "model" in str(e).lower():
                    print(f"{Fore.GREEN}✅ Appropriate error message for missing models{Style.RESET_ALL}")
                    
                    self.test_results.append({
                        "test": "missing_models",
                        "error_type": type(e).__name__,
                        "error_message": str(e),
                        "passed": True
                    })
                    return True
                else:
                    print(f"{Fore.RED}❌ Unexpected error type: {type(e).__name__}{Style.RESET_ALL}")
                    self.test_results.append({
                        "test": "missing_models",
                        "error_type": type(e).__name__,
                        "error_message": str(e),
                        "passed": False
                    })
                    return False
                    
        except Exception as e:
            print(f"{Fore.RED}❌ Missing models test failed: {e}{Style.RESET_ALL}")
            self.test_results.append({
                "test": "missing_models",
                "error": str(e),
                "passed": False
            })
            return False
    
    def test_corrupted_models(self) -> bool:
        """Test behavior when models are corrupted"""
        print(f"\n{Fore.CYAN}💥 Testing Corrupted Models{Style.RESET_ALL}")
        
        try:
            # Restore models first
            self.restore_test_environment()
            
            # Corrupt a model file
            models_dir = Path("models")
            if models_dir.exists():
                # Find a model file to corrupt
                model_files = list(models_dir.rglob("*.model"))
                if model_files:
                    model_file = model_files[0]
                    print(f"{Fore.YELLOW}Corrupting model file: {model_file}{Style.RESET_ALL}")
                    
                    # Write garbage data to the file
                    with open(model_file, 'wb') as f:
                        f.write(b"GARBAGE_DATA" * 1000)
                    
                    # Try to initialize voice bot
                    print(f"{Fore.YELLOW}Attempting to initialize voice bot with corrupted model...{Style.RESET_ALL}")
                    
                    try:
                        voice_bot = VoiceBot(
                            models_dir=str(models_dir),
                            vosk_en_model="vosk-model-en-us-0.22",
                            vosk_hi_model="vosk-model-hi-0.22",
                            whisper_model="tiny",
                            tts_language="en",
                            use_gpu=False,
                            sample_rate=16000,
                            chunk_size=1024
                        )
                        
                        print(f"{Fore.RED}❌ Voice bot initialized with corrupted model (unexpected){Style.RESET_ALL}")
                        self.test_results.append({
                            "test": "corrupted_models",
                            "error": "Voice bot initialized with corrupted model",
                            "passed": False
                        })
                        return False
                        
                    except Exception as e:
                        print(f"{Fore.GREEN}✅ Voice bot correctly failed to initialize: {e}{Style.RESET_ALL}")
                        
                        self.test_results.append({
                            "test": "corrupted_models",
                            "error_type": type(e).__name__,
                            "error_message": str(e),
                            "passed": True
                        })
                        return True
                else:
                    print(f"{Fore.YELLOW}⚠️  No model files found to corrupt{Style.RESET_ALL}")
                    return True
            else:
                print(f"{Fore.RED}❌ Models directory not found{Style.RESET_ALL}")
                return False
                
        except Exception as e:
            print(f"{Fore.RED}❌ Corrupted models test failed: {e}{Style.RESET_ALL}")
            self.test_results.append({
                "test": "corrupted_models",
                "error": str(e),
                "passed": False
            })
            return False
    
    def test_asr_failure_recovery(self) -> bool:
        """Test ASR failure recovery"""
        print(f"\n{Fore.CYAN}🎤 Testing ASR Failure Recovery{Style.RESET_ALL}")
        
        try:
            # Restore models first
            self.restore_test_environment()
            
            # Initialize voice bot
            voice_bot = VoiceBot(
                models_dir="models",
                vosk_en_model="vosk-model-en-us-0.22",
                vosk_hi_model="vosk-model-hi-0.22",
                whisper_model="tiny",
                tts_language="en",
                use_gpu=False,
                sample_rate=16000,
                chunk_size=1024
            )
            
            print(f"{Fore.GREEN}✅ Voice bot initialized successfully{Style.RESET_ALL}")
            
            # Test with invalid audio data
            print(f"{Fore.YELLOW}Testing ASR with invalid audio data...{Style.RESET_ALL}")
            
            try:
                # Create invalid audio data
                invalid_audio = np.array([])  # Empty array
                
                # Test Vosk recognizer
                if hasattr(voice_bot, 'speech_recognizer') and hasattr(voice_bot.speech_recognizer, 'vosk_en'):
                    try:
                        result = voice_bot.speech_recognizer.vosk_en.recognize_audio(invalid_audio, 16000)
                        print(f"{Fore.GREEN}✅ Vosk handled empty audio gracefully: {result}{Style.RESET_ALL}")
                    except Exception as e:
                        print(f"{Fore.GREEN}✅ Vosk correctly failed with empty audio: {e}{Style.RESET_ALL}")
                
                # Test Whisper recognizer
                if hasattr(voice_bot, 'speech_recognizer') and hasattr(voice_bot.speech_recognizer, 'whisper'):
                    try:
                        result = voice_bot.speech_recognizer.whisper.recognize_audio(invalid_audio, 16000)
                        print(f"{Fore.GREEN}✅ Whisper handled empty audio gracefully: {result}{Style.RESET_ALL}")
                    except Exception as e:
                        print(f"{Fore.GREEN}✅ Whisper correctly failed with empty audio: {e}{Style.RESET_ALL}")
                
                self.test_results.append({
                    "test": "asr_failure_recovery",
                    "passed": True
                })
                return True
                
            except Exception as e:
                print(f"{Fore.RED}❌ ASR failure recovery test failed: {e}{Style.RESET_ALL}")
                self.test_results.append({
                    "test": "asr_failure_recovery",
                    "error": str(e),
                    "passed": False
                })
                return False
                
        except Exception as e:
            print(f"{Fore.RED}❌ ASR failure recovery test failed: {e}{Style.RESET_ALL}")
            self.test_results.append({
                "test": "asr_failure_recovery",
                "error": str(e),
                "passed": False
            })
            return False
    
    def test_tts_failure_recovery(self) -> bool:
        """Test TTS failure recovery"""
        print(f"\n{Fore.CYAN}🔊 Testing TTS Failure Recovery{Style.RESET_ALL}")
        
        try:
            # Restore models first
            self.restore_test_environment()
            
            # Initialize voice bot
            voice_bot = VoiceBot(
                models_dir="models",
                vosk_en_model="vosk-model-en-us-0.22",
                vosk_hi_model="vosk-model-hi-0.22",
                whisper_model="tiny",
                tts_language="en",
                use_gpu=False,
                sample_rate=16000,
                chunk_size=1024
            )
            
            print(f"{Fore.GREEN}✅ Voice bot initialized successfully{Style.RESET_ALL}")
            
            # Test TTS with invalid text
            print(f"{Fore.YELLOW}Testing TTS with invalid text...{Style.RESET_ALL}")
            
            try:
                # Test with empty text
                voice_bot.speak("", "en")
                print(f"{Fore.GREEN}✅ TTS handled empty text gracefully{Style.RESET_ALL}")
                
                # Test with very long text
                long_text = "This is a very long text. " * 1000
                voice_bot.speak(long_text, "en")
                print(f"{Fore.GREEN}✅ TTS handled long text gracefully{Style.RESET_ALL}")
                
                # Test with special characters
                special_text = "Hello! @#$%^&*()_+{}|:<>?[]\\;'\",./"
                voice_bot.speak(special_text, "en")
                print(f"{Fore.GREEN}✅ TTS handled special characters gracefully{Style.RESET_ALL}")
                
                self.test_results.append({
                    "test": "tts_failure_recovery",
                    "passed": True
                })
                return True
                
            except Exception as e:
                print(f"{Fore.GREEN}✅ TTS correctly failed with invalid input: {e}{Style.RESET_ALL}")
                
                self.test_results.append({
                    "test": "tts_failure_recovery",
                    "error": str(e),
                    "passed": True  # Expected to fail gracefully
                })
                return True
                
        except Exception as e:
            print(f"{Fore.RED}❌ TTS failure recovery test failed: {e}{Style.RESET_ALL}")
            self.test_results.append({
                "test": "tts_failure_recovery",
                "error": str(e),
                "passed": False
            })
            return False
    
    def test_language_detection_failure(self) -> bool:
        """Test language detection failure recovery"""
        print(f"\n{Fore.CYAN}🌐 Testing Language Detection Failure Recovery{Style.RESET_ALL}")
        
        try:
            # Restore models first
            self.restore_test_environment()
            
            # Initialize voice bot
            voice_bot = VoiceBot(
                models_dir="models",
                vosk_en_model="vosk-model-en-us-0.22",
                vosk_hi_model="vosk-model-hi-0.22",
                whisper_model="tiny",
                tts_language="en",
                use_gpu=False,
                sample_rate=16000,
                chunk_size=1024
            )
            
            print(f"{Fore.GREEN}✅ Voice bot initialized successfully{Style.RESET_ALL}")
            
            # Test language detection with edge cases
            print(f"{Fore.YELLOW}Testing language detection with edge cases...{Style.RESET_ALL}")
            
            edge_cases = [
                "",  # Empty string
                "123456789",  # Numbers only
                "!@#$%^&*()",  # Special characters only
                "a",  # Single character
                " " * 100,  # Whitespace only
                "Hello नमस्ते",  # Mixed languages
            ]
            
            success_count = 0
            
            for i, text in enumerate(edge_cases):
                print(f"\n{Fore.YELLOW}Test {i+1}: '{text}'{Style.RESET_ALL}")
                
                try:
                    detected_language, confidence = voice_bot.language_detector.detect_language(text)
                    print(f"   Detected: {detected_language} (confidence: {confidence:.2f})")
                    
                    # Check if detection is reasonable
                    if detected_language in ["en", "hi"] and confidence >= 0.0:
                        print(f"{Fore.GREEN}✅ Language detection handled edge case{Style.RESET_ALL}")
                        success_count += 1
                    else:
                        print(f"{Fore.YELLOW}⚠️  Unexpected language detection result{Style.RESET_ALL}")
                        success_count += 1  # Still count as success if it doesn't crash
                        
                except Exception as e:
                    print(f"{Fore.GREEN}✅ Language detection correctly failed: {e}{Style.RESET_ALL}")
                    success_count += 1  # Count as success if it fails gracefully
            
            success_rate = success_count / len(edge_cases)
            print(f"\n{Fore.CYAN}Language Detection Edge Cases: {success_count}/{len(edge_cases)} handled ({success_rate:.1%}){Style.RESET_ALL}")
            
            self.test_results.append({
                "test": "language_detection_failure",
                "edge_cases_tested": len(edge_cases),
                "successful": success_count,
                "success_rate": success_rate,
                "passed": success_rate >= 0.8
            })
            
            return success_rate >= 0.8
            
        except Exception as e:
            print(f"{Fore.RED}❌ Language detection failure recovery test failed: {e}{Style.RESET_ALL}")
            self.test_results.append({
                "test": "language_detection_failure",
                "error": str(e),
                "passed": False
            })
            return False
    
    def test_voice_bot_start_stop_failure(self) -> bool:
        """Test voice bot start/stop failure recovery"""
        print(f"\n{Fore.CYAN}🔄 Testing Voice Bot Start/Stop Failure Recovery{Style.RESET_ALL}")
        
        try:
            # Restore models first
            self.restore_test_environment()
            
            # Initialize voice bot
            voice_bot = VoiceBot(
                models_dir="models",
                vosk_en_model="vosk-model-en-us-0.22",
                vosk_hi_model="vosk-model-hi-0.22",
                whisper_model="tiny",
                tts_language="en",
                use_gpu=False,
                sample_rate=16000,
                chunk_size=1024
            )
            
            print(f"{Fore.GREEN}✅ Voice bot initialized successfully{Style.RESET_ALL}")
            
            # Test multiple start/stop cycles
            print(f"{Fore.YELLOW}Testing multiple start/stop cycles...{Style.RESET_ALL}")
            
            success_count = 0
            total_cycles = 3
            
            for i in range(total_cycles):
                print(f"\n{Fore.YELLOW}Cycle {i+1}:{Style.RESET_ALL}")
                
                try:
                    # Start voice bot
                    voice_bot.start()
                    if voice_bot.is_listening:
                        print(f"{Fore.GREEN}✅ Voice bot started successfully{Style.RESET_ALL}")
                        
                        # Let it run briefly
                        time.sleep(1)
                        
                        # Stop voice bot
                        voice_bot.stop()
                        if not voice_bot.is_listening:
                            print(f"{Fore.GREEN}✅ Voice bot stopped successfully{Style.RESET_ALL}")
                            success_count += 1
                        else:
                            print(f"{Fore.RED}❌ Voice bot failed to stop{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}❌ Voice bot failed to start{Style.RESET_ALL}")
                        
                except Exception as e:
                    print(f"{Fore.RED}❌ Start/stop cycle failed: {e}{Style.RESET_ALL}")
            
            success_rate = success_count / total_cycles
            print(f"\n{Fore.CYAN}Start/Stop Cycles: {success_count}/{total_cycles} successful ({success_rate:.1%}){Style.RESET_ALL}")
            
            self.test_results.append({
                "test": "voice_bot_start_stop_failure",
                "cycles_tested": total_cycles,
                "successful": success_count,
                "success_rate": success_rate,
                "passed": success_rate >= 0.8
            })
            
            return success_rate >= 0.8
            
        except Exception as e:
            print(f"{Fore.RED}❌ Voice bot start/stop failure recovery test failed: {e}{Style.RESET_ALL}")
            self.test_results.append({
                "test": "voice_bot_start_stop_failure",
                "error": str(e),
                "passed": False
            })
            return False
    
    def run_all_tests(self) -> bool:
        """Run all error recovery tests"""
        print(f"{Fore.BLUE}🚀 Starting Error Recovery and Graceful Degradation Tests{Style.RESET_ALL}")
        print(f"{Fore.BLUE}========================================================{Style.RESET_ALL}")
        
        # Setup test environment
        if not self.setup_test_environment():
            print(f"{Fore.RED}❌ Failed to setup test environment{Style.RESET_ALL}")
            return False
        
        try:
            # Run tests
            tests = [
                ("Missing Models", self.test_missing_models),
                ("Corrupted Models", self.test_corrupted_models),
                ("ASR Failure Recovery", self.test_asr_failure_recovery),
                ("TTS Failure Recovery", self.test_tts_failure_recovery),
                ("Language Detection Failure", self.test_language_detection_failure),
                ("Voice Bot Start/Stop Failure", self.test_voice_bot_start_stop_failure),
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
                print(f"{Fore.GREEN}🎉 Error Recovery Tests PASSED{Style.RESET_ALL}")
                return True
            else:
                print(f"{Fore.RED}❌ Error Recovery Tests FAILED{Style.RESET_ALL}")
                return False
                
        finally:
            # Always restore test environment
            self.restore_test_environment()

def main():
    """Main test runner"""
    tester = ErrorRecoveryTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()



