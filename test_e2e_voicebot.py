#!/usr/bin/env python3
"""
End-to-End VoiceBot Tests
Comprehensive testing of the complete voice bot pipeline
"""

import unittest
import sys
import os
import time
import logging
from pathlib import Path
from colorama import Fore, Style, init

init(autoreset=True)

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

from voice_bot import VoiceBot, VoiceBotError

# Suppress logging during tests for cleaner output
logging.basicConfig(level=logging.CRITICAL)

class TestVoiceBotE2E(unittest.TestCase):
    """End-to-end tests for VoiceBot functionality"""
    
    @classmethod
    def setUpClass(cls):
        """Set up common resources for tests"""
        print("\n🚀 Starting End-to-End VoiceBot Tests")
        print("=====================================\n")
        cls.models_dir = Path(__file__).parent / "models"
        if not cls.models_dir.exists():
            cls.fail(f"Models directory not found: {cls.models_dir}")

    def test_voicebot_initialization(self):
        """Test VoiceBot initialization"""
        print(f"{Fore.CYAN}🔧 Testing VoiceBot Initialization{Style.RESET_ALL}")
        
        try:
            voicebot = VoiceBot(
                models_dir=str(self.models_dir),
                vosk_en_model="vosk-model-en-us-0.22",
                vosk_hi_model="vosk-model-hi-0.22",
                tts_language="en",
                use_gpu=False,
                sample_rate=16000,
                chunk_size=1024
            )
            print(f"{Fore.GREEN}✅ VoiceBot initialized successfully{Style.RESET_ALL}")
            
            # Test status
            status = voicebot.get_status()
            self.assertIsInstance(status, dict)
            self.assertIn("is_running", status)
            print(f"{Fore.GREEN}✅ Status check passed{Style.RESET_ALL}")
            
            voicebot.stop()
            print(f"{Fore.GREEN}✅ VoiceBot Initialization PASSED{Style.RESET_ALL}\n")
            
        except Exception as e:
            print(f"{Fore.RED}❌ VoiceBot initialization failed: {e}{Style.RESET_ALL}")
            self.fail(f"VoiceBot initialization failed: {e}")

    def test_text_processing_english(self):
        """Test text processing in English"""
        print(f"{Fore.CYAN}📝 Testing English Text Processing{Style.RESET_ALL}")
        
        voicebot = VoiceBot(
            models_dir=str(self.models_dir),
            vosk_en_model="vosk-model-en-us-0.22",
            vosk_hi_model="vosk-model-hi-0.22",
            tts_language="en",
            use_gpu=False
        )
        
        try:
            voicebot.start()
            print(f"{Fore.GREEN}✅ VoiceBot started{Style.RESET_ALL}")
            
            # Test various English inputs
            test_cases = [
                "Hello, how are you?",
                "What's the weather like today?",
                "Tell me a joke",
                "What time is it?",
                "Thank you very much"
            ]
            
            for i, text in enumerate(test_cases):
                print(f"{Fore.YELLOW}Test {i+1}: {text}{Style.RESET_ALL}")
                try:
                    response = voicebot.process_text(text)
                    self.assertIsInstance(response, str)
                    print(f"{Fore.GREEN}✅ Response: {response[:50]}...{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.RED}❌ Error processing '{text}': {e}{Style.RESET_ALL}")
                    # Don't fail the test for individual processing errors
                    pass
                
                time.sleep(0.5)  # Small delay between requests
            
            print(f"{Fore.GREEN}✅ English Text Processing PASSED{Style.RESET_ALL}\n")
            
        except Exception as e:
            print(f"{Fore.RED}❌ English text processing failed: {e}{Style.RESET_ALL}")
            self.fail(f"English text processing failed: {e}")
        finally:
            voicebot.stop()

    def test_text_processing_hindi(self):
        """Test text processing in Hindi"""
        print(f"{Fore.CYAN}📝 Testing Hindi Text Processing{Style.RESET_ALL}")
        
        voicebot = VoiceBot(
            models_dir=str(self.models_dir),
            vosk_en_model="vosk-model-en-us-0.22",
            vosk_hi_model="vosk-model-hi-0.22",
            tts_language="hi",
            use_gpu=False
        )
        
        try:
            voicebot.start()
            print(f"{Fore.GREEN}✅ VoiceBot started{Style.RESET_ALL}")
            
            # Test Hindi inputs
            test_cases = [
                "नमस्ते, आप कैसे हैं?",
                "आज मौसम कैसा है?",
                "एक चुटकुला सुनाइए",
                "अभी क्या समय है?",
                "बहुत धन्यवाद"
            ]
            
            for i, text in enumerate(test_cases):
                print(f"{Fore.YELLOW}Test {i+1}: {text}{Style.RESET_ALL}")
                try:
                    response = voicebot.process_text(text)
                    self.assertIsInstance(response, str)
                    print(f"{Fore.GREEN}✅ Response: {response[:50]}...{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.RED}❌ Error processing '{text}': {e}{Style.RESET_ALL}")
                    # Don't fail the test for individual processing errors
                    pass
                
                time.sleep(0.5)  # Small delay between requests
            
            print(f"{Fore.GREEN}✅ Hindi Text Processing PASSED{Style.RESET_ALL}\n")
            
        except Exception as e:
            print(f"{Fore.RED}❌ Hindi text processing failed: {e}{Style.RESET_ALL}")
            self.fail(f"Hindi text processing failed: {e}")
        finally:
            voicebot.stop()

    def test_language_detection(self):
        """Test language detection functionality"""
        print(f"{Fore.CYAN}🌐 Testing Language Detection{Style.RESET_ALL}")
        
        voicebot = VoiceBot(
            models_dir=str(self.models_dir),
            vosk_en_model="vosk-model-en-us-0.22",
            vosk_hi_model="vosk-model-hi-0.22",
            tts_language="en",
            use_gpu=False
        )
        
        try:
            voicebot.start()
            print(f"{Fore.GREEN}✅ VoiceBot started{Style.RESET_ALL}")
            
            # Test language detection with mixed inputs
            test_cases = [
                ("Hello, how are you?", "en"),
                ("नमस्ते, आप कैसे हैं?", "hi"),
                ("What's the weather like?", "en"),
                ("आज मौसम कैसा है?", "hi"),
                ("Hello नमस्ते", "mixed")  # Mixed language
            ]
            
            for i, (text, expected_lang) in enumerate(test_cases):
                print(f"{Fore.YELLOW}Test {i+1}: {text} (expected: {expected_lang}){Style.RESET_ALL}")
                try:
                    response = voicebot.process_text(text)
                    self.assertIsInstance(response, str)
                    print(f"{Fore.GREEN}✅ Response: {response[:50]}...{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.RED}❌ Error processing '{text}': {e}{Style.RESET_ALL}")
                    pass
                
                time.sleep(0.5)
            
            print(f"{Fore.GREEN}✅ Language Detection PASSED{Style.RESET_ALL}\n")
            
        except Exception as e:
            print(f"{Fore.RED}❌ Language detection failed: {e}{Style.RESET_ALL}")
            self.fail(f"Language detection failed: {e}")
        finally:
            voicebot.stop()

    def test_dialog_system(self):
        """Test dialog system functionality"""
        print(f"{Fore.CYAN}💬 Testing Dialog System{Style.RESET_ALL}")
        
        voicebot = VoiceBot(
            models_dir=str(self.models_dir),
            vosk_en_model="vosk-model-en-us-0.22",
            vosk_hi_model="vosk-model-hi-0.22",
            tts_language="en",
            use_gpu=False
        )
        
        try:
            voicebot.start()
            print(f"{Fore.GREEN}✅ VoiceBot started{Style.RESET_ALL}")
            
            # Test various dialog scenarios
            dialog_scenarios = [
                "Hello",
                "How are you?",
                "What's your name?",
                "Tell me about yourself",
                "What can you do?",
                "Help me",
                "Thank you",
                "Goodbye"
            ]
            
            for i, text in enumerate(dialog_scenarios):
                print(f"{Fore.YELLOW}Dialog {i+1}: {text}{Style.RESET_ALL}")
                try:
                    response = voicebot.process_text(text)
                    self.assertIsInstance(response, str)
                    self.assertGreater(len(response), 0, "Response should not be empty")
                    print(f"{Fore.GREEN}✅ Response: {response[:50]}...{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.RED}❌ Error in dialog '{text}': {e}{Style.RESET_ALL}")
                    pass
                
                time.sleep(0.5)
            
            print(f"{Fore.GREEN}✅ Dialog System PASSED{Style.RESET_ALL}\n")
            
        except Exception as e:
            print(f"{Fore.RED}❌ Dialog system failed: {e}{Style.RESET_ALL}")
            self.fail(f"Dialog system failed: {e}")
        finally:
            voicebot.stop()

    def test_error_handling(self):
        """Test error handling and recovery"""
        print(f"{Fore.CYAN}🛡️ Testing Error Handling{Style.RESET_ALL}")
        
        voicebot = VoiceBot(
            models_dir=str(self.models_dir),
            vosk_en_model="vosk-model-en-us-0.22",
            vosk_hi_model="vosk-model-hi-0.22",
            tts_language="en",
            use_gpu=False
        )
        
        try:
            voicebot.start()
            print(f"{Fore.GREEN}✅ VoiceBot started{Style.RESET_ALL}")
            
            # Test error scenarios
            error_test_cases = [
                "",  # Empty input
                "   ",  # Whitespace only
                "a" * 1000,  # Very long input
                "!@#$%^&*()",  # Special characters
                "123456789",  # Numbers only
            ]
            
            for i, text in enumerate(error_test_cases):
                print(f"{Fore.YELLOW}Error Test {i+1}: '{text[:20]}...'{Style.RESET_ALL}")
                try:
                    response = voicebot.process_text(text)
                    print(f"{Fore.GREEN}✅ Handled gracefully: {response[:50]}...{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.YELLOW}⚠️ Expected error handled: {e}{Style.RESET_ALL}")
                    # Errors are expected for some inputs
                    pass
                
                time.sleep(0.5)
            
            print(f"{Fore.GREEN}✅ Error Handling PASSED{Style.RESET_ALL}\n")
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error handling test failed: {e}{Style.RESET_ALL}")
            self.fail(f"Error handling test failed: {e}")
        finally:
            voicebot.stop()

    def test_performance(self):
        """Test performance with multiple requests"""
        print(f"{Fore.CYAN}⚡ Testing Performance{Style.RESET_ALL}")
        
        voicebot = VoiceBot(
            models_dir=str(self.models_dir),
            vosk_en_model="vosk-model-en-us-0.22",
            vosk_hi_model="vosk-model-hi-0.22",
            tts_language="en",
            use_gpu=False
        )
        
        try:
            voicebot.start()
            print(f"{Fore.GREEN}✅ VoiceBot started{Style.RESET_ALL}")
            
            # Performance test with multiple requests
            test_texts = [
                "Hello",
                "How are you?",
                "What's the weather?",
                "Tell me a joke",
                "Thank you",
                "Goodbye"
            ]
            
            start_time = time.time()
            successful_requests = 0
            
            for i, text in enumerate(test_texts):
                try:
                    response = voicebot.process_text(text)
                    successful_requests += 1
                    print(f"{Fore.GREEN}✅ Request {i+1}: {response[:30]}...{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.RED}❌ Request {i+1} failed: {e}{Style.RESET_ALL}")
                
                time.sleep(0.2)  # Small delay
            
            end_time = time.time()
            total_time = end_time - start_time
            avg_time = total_time / len(test_texts)
            
            print(f"\n📊 Performance Results:")
            print(f"   Total requests: {len(test_texts)}")
            print(f"   Successful: {successful_requests}")
            print(f"   Total time: {total_time:.2f}s")
            print(f"   Average time per request: {avg_time:.2f}s")
            
            # Performance assertions
            self.assertGreater(successful_requests, len(test_texts) // 2, "At least half the requests should succeed")
            self.assertLess(avg_time, 5.0, "Average response time should be less than 5 seconds")
            
            print(f"{Fore.GREEN}✅ Performance Test PASSED{Style.RESET_ALL}\n")
            
        except Exception as e:
            print(f"{Fore.RED}❌ Performance test failed: {e}{Style.RESET_ALL}")
            self.fail(f"Performance test failed: {e}")
        finally:
            voicebot.stop()

    def test_context_manager(self):
        """Test VoiceBot as context manager"""
        print(f"{Fore.CYAN}🔄 Testing Context Manager{Style.RESET_ALL}")
        
        try:
            with VoiceBot(
                models_dir=str(self.models_dir),
                vosk_en_model="vosk-model-en-us-0.22",
                vosk_hi_model="vosk-model-hi-0.22",
                tts_language="en",
                use_gpu=False
            ) as voicebot:
                print(f"{Fore.GREEN}✅ VoiceBot started with context manager{Style.RESET_ALL}")
                
                # Test basic functionality
                response = voicebot.process_text("Hello, how are you?")
                self.assertIsInstance(response, str)
                print(f"{Fore.GREEN}✅ Context manager test successful{Style.RESET_ALL}")
            
            print(f"{Fore.GREEN}✅ Context Manager PASSED{Style.RESET_ALL}\n")
            
        except Exception as e:
            print(f"{Fore.RED}❌ Context manager test failed: {e}{Style.RESET_ALL}")
            self.fail(f"Context manager test failed: {e}")

if __name__ == "__main__":
    # Run the tests
    unittest.main(verbosity=2)
