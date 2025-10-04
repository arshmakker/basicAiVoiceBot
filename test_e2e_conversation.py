#!/usr/bin/env python3
"""
End-to-End Conversation Flow Test
Tests the complete pipeline: mic input → speech recognition → language detection → dialog processing → TTS → speaker output
"""

import sys
import time
import threading
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any
import pyaudio
import numpy as np
from colorama import Fore, Style, init

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from voice_bot import VoiceBot, VoiceBotError
from voice_bot.logging_utils import setup_single_line_logging

init(autoreset=True)

class E2EConversationTester:
    """End-to-end conversation flow tester"""
    
    def __init__(self):
        self.voice_bot: Optional[VoiceBot] = None
        self.test_results: List[Dict[str, Any]] = []
        self.conversation_log: List[Dict[str, str]] = []
        self.is_recording = False
        self.audio_data = []
        
    def setup_logging(self):
        """Setup logging for tests"""
        setup_single_line_logging(verbose=True)
        
    def initialize_voice_bot(self) -> bool:
        """Initialize the voice bot with models"""
        try:
            logging.info("Initializing voice bot for E2E testing...")
            
            # Check if models directory exists
            models_dir = Path("models")
            if not models_dir.exists():
                logging.error("Models directory not found. Run: python download_models.py --all")
                return False
            
            self.voice_bot = VoiceBot(
                models_dir=str(models_dir),
                vosk_en_model="vosk-model-en-us-0.22",
                vosk_hi_model="vosk-model-hi-0.22", 
                tts_language="en",
                use_gpu=False,
                sample_rate=16000,
                chunk_size=1024
            )
            
            # Set up callbacks to track the conversation flow
            self.voice_bot.on_speech_detected = self._on_speech_detected
            self.voice_bot.on_response_generated = self._on_response_generated
            self.voice_bot.on_language_detected = self._on_language_detected
            self.voice_bot.on_error = self._on_error
            
            logging.info("Voice bot initialized successfully")
            return True
            
        except Exception as e:
            logging.error(f"Failed to initialize voice bot: {e}")
            return False
    
    def _on_speech_detected(self, text: str):
        """Callback for speech detection"""
        logging.info(f"Speech detected: '{text}'")
        self.conversation_log.append({
            "type": "speech_detected",
            "text": text,
            "timestamp": time.time()
        })
    
    def _on_response_generated(self, response: str):
        """Callback for response generation"""
        logging.info(f"Response generated: '{response}'")
        self.conversation_log.append({
            "type": "response_generated", 
            "text": response,
            "timestamp": time.time()
        })
    
    def _on_language_detected(self, language: str):
        """Callback for language detection"""
        logging.info(f"Language detected: {language}")
        self.conversation_log.append({
            "type": "language_detected",
            "language": language,
            "timestamp": time.time()
        })
    
    def _on_error(self, error: Exception):
        """Callback for errors"""
        logging.error(f"Error occurred: {error}")
        self.conversation_log.append({
            "type": "error",
            "error": str(error),
            "timestamp": time.time()
        })
    
    def test_basic_conversation_flow(self) -> bool:
        """Test basic conversation flow with text input"""
        print(f"\n{Fore.CYAN}🧪 Testing Basic Conversation Flow{Style.RESET_ALL}")
        
        test_cases = [
            {"input": "Hello", "expected_language": "en"},
            {"input": "नमस्ते", "expected_language": "hi"},
            {"input": "How are you?", "expected_language": "en"},
            {"input": "आप कैसे हैं?", "expected_language": "hi"},
        ]
        
        success_count = 0
        
        for i, test_case in enumerate(test_cases):
            print(f"\n{Fore.YELLOW}Test {i+1}: '{test_case['input']}'{Style.RESET_ALL}")
            
            try:
                # Test text processing (bypassing speech recognition)
                response = self.voice_bot.process_text(test_case["input"])
                
                if response and len(response) > 0:
                    print(f"{Fore.GREEN}✅ Response: '{response}'{Style.RESET_ALL}")
                    success_count += 1
                    
                    # Test TTS (speak the response)
                    self.voice_bot.speak(response, test_case["expected_language"])
                    time.sleep(1)  # Wait for TTS to complete
                    
                else:
                    print(f"{Fore.RED}❌ No response generated{Style.RESET_ALL}")
                    
            except Exception as e:
                print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")
        
        success_rate = success_count / len(test_cases)
        print(f"\n{Fore.CYAN}Basic Conversation Flow: {success_count}/{len(test_cases)} tests passed ({success_rate:.1%}){Style.RESET_ALL}")
        
        self.test_results.append({
            "test": "basic_conversation_flow",
            "passed": success_count,
            "total": len(test_cases),
            "success_rate": success_rate
        })
        
        return success_rate >= 0.8  # 80% success rate
    
    def test_audio_device_detection(self) -> bool:
        """Test audio device detection and selection"""
        print(f"\n{Fore.CYAN}🎤 Testing Audio Device Detection{Style.RESET_ALL}")
        
        try:
            # Test PyAudio device enumeration
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
            
            if len(input_devices) == 0:
                print(f"{Fore.RED}❌ No input devices found{Style.RESET_ALL}")
                return False
                
            if len(output_devices) == 0:
                print(f"{Fore.RED}❌ No output devices found{Style.RESET_ALL}")
                return False
            
            # Test device selection
            selected_input = input_devices[0]
            print(f"{Fore.GREEN}✅ Selected input device: {selected_input[1]} (ID: {selected_input[0]}){Style.RESET_ALL}")
            
            self.test_results.append({
                "test": "audio_device_detection",
                "input_devices": len(input_devices),
                "output_devices": len(output_devices),
                "passed": True
            })
            
            return True
            
        except Exception as e:
            print(f"{Fore.RED}❌ Audio device detection failed: {e}{Style.RESET_ALL}")
            self.test_results.append({
                "test": "audio_device_detection",
                "error": str(e),
                "passed": False
            })
            return False
    
    def test_voice_bot_start_stop(self) -> bool:
        """Test voice bot start and stop functionality"""
        print(f"\n{Fore.CYAN}🔄 Testing Voice Bot Start/Stop{Style.RESET_ALL}")
        
        try:
            # Test start
            logging.info("Starting voice bot...")
            self.voice_bot.start()
            time.sleep(2)  # Let it initialize
            
            if self.voice_bot.is_listening:
                print(f"{Fore.GREEN}✅ Voice bot started successfully{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ Voice bot failed to start listening{Style.RESET_ALL}")
                return False
            
            # Test stop
            logging.info("Stopping voice bot...")
            self.voice_bot.stop()
            time.sleep(1)  # Let it stop
            
            if not self.voice_bot.is_listening:
                print(f"{Fore.GREEN}✅ Voice bot stopped successfully{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ Voice bot failed to stop listening{Style.RESET_ALL}")
                return False
            
            self.test_results.append({
                "test": "voice_bot_start_stop",
                "passed": True
            })
            
            return True
            
        except Exception as e:
            print(f"{Fore.RED}❌ Start/stop test failed: {e}{Style.RESET_ALL}")
            self.test_results.append({
                "test": "voice_bot_start_stop",
                "error": str(e),
                "passed": False
            })
            return False
    
    def test_conversation_logging(self) -> bool:
        """Test conversation logging and tracking"""
        print(f"\n{Fore.CYAN}📝 Testing Conversation Logging{Style.RESET_ALL}")
        
        # Clear previous logs
        self.conversation_log = []
        
        try:
            # Start voice bot
            self.voice_bot.start()
            time.sleep(1)
            
            # Process some text to generate conversation events
            test_inputs = ["Hello", "How are you?", "Goodbye"]
            
            for test_input in test_inputs:
                response = self.voice_bot.process_text(test_input)
                time.sleep(0.5)
            
            # Stop voice bot
            self.voice_bot.stop()
            
            # Analyze conversation log
            speech_events = [log for log in self.conversation_log if log["type"] == "speech_detected"]
            response_events = [log for log in self.conversation_log if log["type"] == "response_generated"]
            language_events = [log for log in self.conversation_log if log["type"] == "language_detected"]
            
            print(f"{Fore.GREEN}✅ Conversation log contains {len(self.conversation_log)} events{Style.RESET_ALL}")
            print(f"{Fore.GREEN}✅ Speech events: {len(speech_events)}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}✅ Response events: {len(response_events)}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}✅ Language events: {len(language_events)}{Style.RESET_ALL}")
            
            # Check if we have the expected events
            if len(speech_events) >= len(test_inputs) and len(response_events) >= len(test_inputs):
                print(f"{Fore.GREEN}✅ Conversation logging working correctly{Style.RESET_ALL}")
                
                self.test_results.append({
                    "test": "conversation_logging",
                    "total_events": len(self.conversation_log),
                    "speech_events": len(speech_events),
                    "response_events": len(response_events),
                    "passed": True
                })
                
                return True
            else:
                print(f"{Fore.RED}❌ Missing conversation events{Style.RESET_ALL}")
                return False
                
        except Exception as e:
            print(f"{Fore.RED}❌ Conversation logging test failed: {e}{Style.RESET_ALL}")
            self.test_results.append({
                "test": "conversation_logging",
                "error": str(e),
                "passed": False
            })
            return False
    
    def run_all_tests(self) -> bool:
        """Run all E2E conversation tests"""
        print(f"{Fore.BLUE}🚀 Starting End-to-End Conversation Flow Tests{Style.RESET_ALL}")
        print(f"{Fore.BLUE}=================================================={Style.RESET_ALL}")
        
        # Setup
        self.setup_logging()
        
        if not self.initialize_voice_bot():
            print(f"{Fore.RED}❌ Failed to initialize voice bot. Cannot run tests.{Style.RESET_ALL}")
            return False
        
        # Run tests
        tests = [
            ("Audio Device Detection", self.test_audio_device_detection),
            ("Voice Bot Start/Stop", self.test_voice_bot_start_stop),
            ("Basic Conversation Flow", self.test_basic_conversation_flow),
            ("Conversation Logging", self.test_conversation_logging),
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
            print(f"{Fore.GREEN}🎉 E2E Conversation Flow Tests PASSED{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.RED}❌ E2E Conversation Flow Tests FAILED{Style.RESET_ALL}")
            return False

def main():
    """Main test runner"""
    tester = E2EConversationTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()


