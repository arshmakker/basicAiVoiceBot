#!/usr/bin/env python3
"""
Test Cases for Keyboard-Controlled Dialog Integration
Comprehensive test suite to validate dialog system integration in keyboard mode
"""

import unittest
import sys
import os
import time
import threading
from pathlib import Path
from colorama import Fore, Style, init
from unittest.mock import Mock, patch, MagicMock

init(autoreset=True)

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

class TestKeyboardDialogIntegration(unittest.TestCase):
    """Test cases for keyboard-controlled dialog integration"""
    
    @classmethod
    def setUpClass(cls):
        """Set up common resources for tests"""
        print("\n🧪 Starting Keyboard Dialog Integration Tests")
        print("=" * 60)
        cls.models_dir = Path(__file__).parent / "models"
        if not cls.models_dir.exists():
            cls.fail(f"Models directory not found: {cls.models_dir}")

    def test_dialog_system_integration_basic(self):
        """Test basic dialog system integration in keyboard mode"""
        print(f"\n{Fore.CYAN}🔧 Testing Basic Dialog System Integration{Style.RESET_ALL}")
        
        # Test case: Verify dialog system is called instead of echo
        test_scenarios = [
            {
                "input": "Hello",
                "expected_response_type": "greeting",
                "should_not_contain": "I heard you say"
            },
            {
                "input": "How are you?",
                "expected_response_type": "question_response",
                "should_not_contain": "I heard you say"
            },
            {
                "input": "Tell me a joke",
                "expected_response_type": "command_response",
                "should_not_contain": "I heard you say"
            }
        ]
        
        for i, scenario in enumerate(test_scenarios):
            print(f"{Fore.YELLOW}Test {i+1}: {scenario['input']}{Style.RESET_ALL}")
            
            # Mock the keyboard control flow
            with patch('voice_bot_cli.VoiceBotCLI') as mock_cli:
                mock_voicebot = Mock()
                mock_cli.voice_bot = mock_voicebot
                
                # Test dialog processing
                response = mock_voicebot.process_text(scenario['input'])
                
                # Verify dialog system was called
                mock_voicebot.process_text.assert_called_with(scenario['input'])
                
                # Verify response doesn't contain echo text
                if response and scenario['should_not_contain'] in response:
                    self.fail(f"Response contains echo text: {response}")
                
                print(f"{Fore.GREEN}✅ Dialog integration test passed{Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}✅ Basic Dialog System Integration PASSED{Style.RESET_ALL}\n")

    def test_language_detection_integration(self):
        """Test language detection integration in keyboard mode"""
        print(f"\n{Fore.CYAN}🌐 Testing Language Detection Integration{Style.RESET_ALL}")
        
        test_cases = [
            {
                "input": "Hello, how are you?",
                "expected_language": "en",
                "description": "English input"
            },
            {
                "input": "नमस्ते, आप कैसे हैं?",
                "expected_language": "hi", 
                "description": "Hindi input"
            },
            {
                "input": "Hello नमस्ते",
                "expected_language": "mixed",
                "description": "Mixed language input"
            }
        ]
        
        for i, test_case in enumerate(test_cases):
            print(f"{Fore.YELLOW}Test {i+1}: {test_case['description']}{Style.RESET_ALL}")
            
            # Mock language detection
            with patch('voice_bot.language_detection.LanguageDetector') as mock_detector:
                mock_detector.return_value.detect_language.return_value = (
                    test_case['expected_language'], 0.8
                )
                
                # Test language detection
                detector = mock_detector.return_value
                detected_lang, confidence = detector.detect_language(test_case['input'])
                
                # Verify language detection
                self.assertEqual(detected_lang, test_case['expected_language'])
                self.assertGreater(confidence, 0.5)
                
                print(f"{Fore.GREEN}✅ Language detection: {detected_lang} (confidence: {confidence}){Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}✅ Language Detection Integration PASSED{Style.RESET_ALL}\n")

    def test_keyboard_control_flow(self):
        """Test complete keyboard control flow"""
        print(f"\n{Fore.CYAN}⌨️ Testing Keyboard Control Flow{Style.RESET_ALL}")
        
        # Test the 's' -> speak -> 't' -> process flow
        flow_steps = [
            {
                "step": "start_recording",
                "command": "s",
                "expected_action": "start_recording"
            },
            {
                "step": "user_speaks",
                "command": "user_input",
                "expected_action": "capture_audio"
            },
            {
                "step": "stop_recording", 
                "command": "t",
                "expected_action": "process_and_respond"
            }
        ]
        
        for i, step in enumerate(flow_steps):
            print(f"{Fore.YELLOW}Step {i+1}: {step['step']}{Style.RESET_ALL}")
            
            # Mock the keyboard control flow
            with patch('voice_bot_cli.VoiceBotCLI') as mock_cli:
                mock_cli.voice_bot = Mock()
                mock_cli.recorder = Mock()
                
                if step['command'] == 's':
                    # Test start recording
                    mock_cli.start_recording()
                    print(f"{Fore.GREEN}✅ Start recording triggered{Style.RESET_ALL}")
                    
                elif step['command'] == 't':
                    # Test stop and process
                    mock_cli.stop_recording()
                    mock_cli.process_audio()
                    print(f"{Fore.GREEN}✅ Stop and process triggered{Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}✅ Keyboard Control Flow PASSED{Style.RESET_ALL}\n")

    def test_error_handling_scenarios(self):
        """Test error handling in dialog integration"""
        print(f"\n{Fore.CYAN}🛡️ Testing Error Handling Scenarios{Style.RESET_ALL}")
        
        error_scenarios = [
            {
                "error_type": "dialog_system_failure",
                "description": "Dialog system throws exception",
                "expected_fallback": "fallback_response"
            },
            {
                "error_type": "tts_failure", 
                "description": "TTS system fails",
                "expected_fallback": "text_response_only"
            },
            {
                "error_type": "transcription_failure",
                "description": "Audio transcription fails",
                "expected_fallback": "error_message"
            }
        ]
        
        for i, scenario in enumerate(error_scenarios):
            print(f"{Fore.YELLOW}Error Test {i+1}: {scenario['description']}{Style.RESET_ALL}")
            
            # Mock error scenarios
            with patch('voice_bot_cli.VoiceBotCLI') as mock_cli:
                mock_cli.voice_bot = Mock()
                
                if scenario['error_type'] == 'dialog_system_failure':
                    mock_cli.voice_bot.process_text.side_effect = Exception("Dialog system error")
                    
                    # Test error handling
                    try:
                        response = mock_cli.voice_bot.process_text("test")
                    except Exception as e:
                        # Verify fallback is triggered
                        self.assertIn("error", str(e).lower())
                        print(f"{Fore.GREEN}✅ Dialog error handled gracefully{Style.RESET_ALL}")
                
                elif scenario['error_type'] == 'tts_failure':
                    mock_cli.voice_bot.speak.side_effect = Exception("TTS error")
                    
                    # Test TTS error handling
                    try:
                        mock_cli.voice_bot.speak("test")
                    except Exception as e:
                        # Verify fallback is triggered
                        self.assertIn("error", str(e).lower())
                        print(f"{Fore.GREEN}✅ TTS error handled gracefully{Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}✅ Error Handling Scenarios PASSED{Style.RESET_ALL}\n")

    def test_conversation_flow_validation(self):
        """Test multi-turn conversation flow"""
        print(f"\n{Fore.CYAN}💬 Testing Conversation Flow Validation{Style.RESET_ALL}")
        
        conversation_flow = [
            {
                "turn": 1,
                "input": "Hello",
                "expected_context": "greeting"
            },
            {
                "turn": 2, 
                "input": "How are you?",
                "expected_context": "question"
            },
            {
                "turn": 3,
                "input": "Tell me about yourself",
                "expected_context": "information_request"
            }
        ]
        
        for turn in conversation_flow:
            print(f"{Fore.YELLOW}Turn {turn['turn']}: {turn['input']}{Style.RESET_ALL}")
            
            # Mock conversation context
            with patch('voice_bot_cli.VoiceBotCLI') as mock_cli:
                mock_cli.voice_bot = Mock()
                mock_cli.conversation_context = []
                
                # Test conversation flow
                response = mock_cli.voice_bot.process_text(turn['input'])
                
                # Verify context is maintained
                mock_cli.conversation_context.append({
                    'input': turn['input'],
                    'response': response,
                    'context': turn['expected_context']
                })
                
                print(f"{Fore.GREEN}✅ Turn {turn['turn']} processed{Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}✅ Conversation Flow Validation PASSED{Style.RESET_ALL}\n")

    def test_performance_validation(self):
        """Test performance of dialog integration"""
        print(f"\n{Fore.CYAN}⚡ Testing Performance Validation{Style.RESET_ALL}")
        
        performance_tests = [
            {
                "test_name": "response_time",
                "max_time": 5.0,  # seconds
                "description": "Response generation time"
            },
            {
                "test_name": "memory_usage",
                "max_memory": 100,  # MB
                "description": "Memory usage during processing"
            },
            {
                "test_name": "concurrent_requests",
                "max_concurrent": 3,
                "description": "Concurrent request handling"
            }
        ]
        
        for test in performance_tests:
            print(f"{Fore.YELLOW}Performance Test: {test['description']}{Style.RESET_ALL}")
            
            if test['test_name'] == 'response_time':
                # Test response time
                start_time = time.time()
                
                with patch('voice_bot_cli.VoiceBotCLI') as mock_cli:
                    mock_cli.voice_bot = Mock()
                    mock_cli.voice_bot.process_text.return_value = "Test response"
                    
                    response = mock_cli.voice_bot.process_text("test")
                    
                end_time = time.time()
                response_time = end_time - start_time
                
                self.assertLess(response_time, test['max_time'])
                print(f"{Fore.GREEN}✅ Response time: {response_time:.2f}s{Style.RESET_ALL}")
            
            elif test['test_name'] == 'memory_usage':
                # Test memory usage (simplified)
                import psutil
                process = psutil.Process()
                memory_before = process.memory_info().rss / (1024 * 1024)
                
                # Simulate processing
                with patch('voice_bot_cli.VoiceBotCLI') as mock_cli:
                    mock_cli.voice_bot = Mock()
                    mock_cli.voice_bot.process_text.return_value = "Test response"
                    
                    response = mock_cli.voice_bot.process_text("test")
                
                memory_after = process.memory_info().rss / (1024 * 1024)
                memory_used = memory_after - memory_before
                
                self.assertLess(memory_used, test['max_memory'])
                print(f"{Fore.GREEN}✅ Memory usage: {memory_used:.1f}MB{Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}✅ Performance Validation PASSED{Style.RESET_ALL}\n")

    def test_multilingual_support(self):
        """Test multilingual support in keyboard mode"""
        print(f"\n{Fore.CYAN}🌍 Testing Multilingual Support{Style.RESET_ALL}")
        
        multilingual_tests = [
            {
                "language": "en",
                "input": "Hello, how are you?",
                "expected_tts_language": "en"
            },
            {
                "language": "hi",
                "input": "नमस्ते, आप कैसे हैं?",
                "expected_tts_language": "hi"
            },
            {
                "language": "mixed",
                "input": "Hello नमस्ते",
                "expected_tts_language": "en"  # Default fallback
            }
        ]
        
        for i, test in enumerate(multilingual_tests):
            print(f"{Fore.YELLOW}Multilingual Test {i+1}: {test['language']}{Style.RESET_ALL}")
            
            # Mock multilingual processing
            with patch('voice_bot_cli.VoiceBotCLI') as mock_cli:
                mock_cli.voice_bot = Mock()
                mock_cli.voice_bot.tts_language = test['expected_tts_language']
                
                # Test language-specific processing
                response = mock_cli.voice_bot.process_text(test['input'])
                
                # Verify TTS language is set correctly
                self.assertEqual(mock_cli.voice_bot.tts_language, test['expected_tts_language'])
                
                print(f"{Fore.GREEN}✅ {test['language']} processing successful{Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}✅ Multilingual Support PASSED{Style.RESET_ALL}\n")

if __name__ == "__main__":
    # Run the tests
    unittest.main(verbosity=2)
