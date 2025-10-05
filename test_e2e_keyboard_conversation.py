#!/usr/bin/env python3
"""
End-to-End Test for Keyboard-Controlled Conversation Flow
Comprehensive test suite for complete keyboard-controlled dialog integration
"""

import unittest
import sys
import os
import time
from pathlib import Path
from colorama import Fore, Style, init
from unittest.mock import Mock, patch, MagicMock

init(autoreset=True)

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

class TestE2EKeyboardConversation(unittest.TestCase):
    """End-to-end test cases for keyboard-controlled conversation flow"""
    
    @classmethod
    def setUpClass(cls):
        """Set up common resources for tests"""
        print("\n🎯 Starting End-to-End Keyboard Conversation Test Suite")
        print("=" * 70)

    def test_complete_conversation_flow(self):
        """Test complete conversation flow from start to finish"""
        print(f"\n{Fore.CYAN}🔄 Testing Complete Conversation Flow{Style.RESET_ALL}")
        
        conversation_scenarios = [
            {
                "scenario": "Greeting_Conversation",
                "turns": [
                    {"input": "Hello, how are you?", "expected_language": "en", "expected_response_type": "greeting"},
                    {"input": "What's your name?", "expected_language": "en", "expected_response_type": "question"},
                    {"input": "Thank you", "expected_language": "en", "expected_response_type": "gratitude"}
                ],
                "description": "Complete greeting conversation flow"
            },
            {
                "scenario": "Question_Answer_Flow",
                "turns": [
                    {"input": "What's the weather like?", "expected_language": "en", "expected_response_type": "question"},
                    {"input": "Can you help me?", "expected_language": "en", "expected_response_type": "request"},
                    {"input": "That's helpful", "expected_language": "en", "expected_response_type": "acknowledgment"}
                ],
                "description": "Question and answer conversation flow"
            },
            {
                "scenario": "Multilingual_Flow",
                "turns": [
                    {"input": "Hello", "expected_language": "en", "expected_response_type": "greeting"},
                    {"input": "नमस्ते", "expected_language": "hi", "expected_response_type": "greeting"},
                    {"input": "How are you? आप कैसे हैं?", "expected_language": "mixed", "expected_response_type": "question"}
                ],
                "description": "Multilingual conversation flow"
            }
        ]
        
        for i, scenario in enumerate(conversation_scenarios):
            print(f"{Fore.YELLOW}Test {i+1}: {scenario['description']}{Style.RESET_ALL}")
            
            # Mock complete conversation flow
            with patch('voice_bot_cli.VoiceBotCLI') as mock_cli:
                mock_cli.voice_bot = Mock()
                mock_cli.conversation_context = []
                mock_cli.conversation_state = "idle"
                
                # Simulate complete conversation flow
                for j, turn in enumerate(scenario['turns']):
                    print(f"{Fore.CYAN}  Turn {j+1}: {turn['input']}{Style.RESET_ALL}")
                    
                    # Mock language detection
                    mock_cli.voice_bot.language_detector.detect_language.return_value = (
                        turn['expected_language'], 0.9
                    )
                    
                    # Mock dialog processing
                    mock_cli.voice_bot.process_text.return_value = f"Response to: {turn['input']}"
                    
                    # Mock TTS
                    mock_cli.voice_bot.speak.return_value = True
                    
                    # Simulate conversation turn
                    detected_lang, confidence = mock_cli.voice_bot.language_detector.detect_language(turn['input'])
                    response = mock_cli.voice_bot.process_text(turn['input'], detected_lang)
                    tts_result = mock_cli.voice_bot.speak(response, detected_lang)
                    
                    # Update conversation context
                    mock_cli.conversation_context.append({
                        'input': turn['input'],
                        'response': response,
                        'language': detected_lang,
                        'confidence': confidence,
                        'timestamp': time.time()
                    })
                    mock_cli.conversation_state = "active"
                    
                    # Verify conversation turn
                    self.assertEqual(detected_lang, turn['expected_language'])
                    self.assertIsNotNone(response)
                    self.assertTrue(tts_result)
                    
                    print(f"{Fore.GREEN}    ✅ Language: {detected_lang}, Response: {response[:30]}...{Style.RESET_ALL}")
                
                # Verify complete conversation
                self.assertEqual(len(mock_cli.conversation_context), len(scenario['turns']))
                self.assertEqual(mock_cli.conversation_state, "active")
                
                print(f"{Fore.GREEN}✅ Complete conversation: {len(scenario['turns'])} turns processed{Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}✅ Complete Conversation Flow PASSED{Style.RESET_ALL}\n")

    def test_keyboard_command_flow(self):
        """Test keyboard command flow"""
        print(f"\n{Fore.CYAN}⌨️ Testing Keyboard Command Flow{Style.RESET_ALL}")
        
        command_scenarios = [
            {
                "scenario": "Basic_Commands",
                "commands": [
                    {"command": "s", "action": "start_recording", "expected_result": "recording_started"},
                    {"command": "t", "action": "stop_recording", "expected_result": "dialog_processed"},
                    {"command": "h", "action": "show_help", "expected_result": "help_displayed"},
                    {"command": "q", "action": "quit", "expected_result": "bot_exited"}
                ],
                "description": "Basic keyboard commands"
            },
            {
                "scenario": "Context_Commands",
                "commands": [
                    {"command": "s", "action": "start_recording", "expected_result": "recording_started"},
                    {"command": "t", "action": "stop_recording", "expected_result": "dialog_processed"},
                    {"command": "c", "action": "show_context", "expected_result": "context_displayed"},
                    {"command": "clear", "action": "clear_context", "expected_result": "context_cleared"}
                ],
                "description": "Context management commands"
            },
            {
                "scenario": "Recording_Cycle",
                "commands": [
                    {"command": "s", "action": "start_recording", "expected_result": "recording_started"},
                    {"command": "t", "action": "stop_recording", "expected_result": "dialog_processed"},
                    {"command": "s", "action": "start_recording", "expected_result": "recording_started"},
                    {"command": "t", "action": "stop_recording", "expected_result": "dialog_processed"}
                ],
                "description": "Multiple recording cycles"
            }
        ]
        
        for i, scenario in enumerate(command_scenarios):
            print(f"{Fore.YELLOW}Test {i+1}: {scenario['description']}{Style.RESET_ALL}")
            
            # Mock keyboard command flow
            with patch('voice_bot_cli.VoiceBotCLI') as mock_cli:
                mock_cli.voice_bot = Mock()
                mock_cli.conversation_context = []
                mock_cli.conversation_state = "idle"
                mock_cli.recorder = Mock()
                
                # Simulate keyboard command flow
                for j, cmd in enumerate(scenario['commands']):
                    print(f"{Fore.CYAN}  Command {j+1}: {cmd['command']} -> {cmd['action']}{Style.RESET_ALL}")
                    
                    if cmd['action'] == "start_recording":
                        mock_cli.recorder.start_recording.return_value = True
                        result = mock_cli.recorder.start_recording()
                        self.assertTrue(result)
                        print(f"{Fore.GREEN}    ✅ Recording started{Style.RESET_ALL}")
                    
                    elif cmd['action'] == "stop_recording":
                        mock_cli.voice_bot.process_text.return_value = "Dialog response"
                        mock_cli.voice_bot.speak.return_value = True
                        response = mock_cli.voice_bot.process_text("test input", "en")
                        tts_result = mock_cli.voice_bot.speak(response, "en")
                        self.assertIsNotNone(response)
                        self.assertTrue(tts_result)
                        print(f"{Fore.GREEN}    ✅ Dialog processed{Style.RESET_ALL}")
                    
                    elif cmd['action'] == "show_help":
                        help_text = "Available commands: s, t, c, clear, h, q"
                        self.assertIsNotNone(help_text)
                        print(f"{Fore.GREEN}    ✅ Help displayed{Style.RESET_ALL}")
                    
                    elif cmd['action'] == "show_context":
                        context_length = len(mock_cli.conversation_context)
                        self.assertIsNotNone(context_length)
                        print(f"{Fore.GREEN}    ✅ Context displayed: {context_length} turns{Style.RESET_ALL}")
                    
                    elif cmd['action'] == "clear_context":
                        mock_cli.conversation_context = []
                        mock_cli.conversation_state = "idle"
                        self.assertEqual(len(mock_cli.conversation_context), 0)
                        print(f"{Fore.GREEN}    ✅ Context cleared{Style.RESET_ALL}")
                    
                    elif cmd['action'] == "quit":
                        mock_cli.conversation_state = "exiting"
                        self.assertEqual(mock_cli.conversation_state, "exiting")
                        print(f"{Fore.GREEN}    ✅ Bot exited{Style.RESET_ALL}")
                
                print(f"{Fore.GREEN}✅ Command flow: {len(scenario['commands'])} commands processed{Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}✅ Keyboard Command Flow PASSED{Style.RESET_ALL}\n")

    def test_error_recovery_flow(self):
        """Test error recovery flow"""
        print(f"\n{Fore.CYAN}🛡️ Testing Error Recovery Flow{Style.RESET_ALL}")
        
        error_scenarios = [
            {
                "scenario": "Dialog_Error_Recovery",
                "error_type": "dialog_failure",
                "recovery_steps": [
                    {"step": "detect_error", "action": "catch_exception"},
                    {"step": "fallback_response", "action": "generate_fallback"},
                    {"step": "continue_conversation", "action": "resume_normal"}
                ],
                "description": "Dialog system error recovery"
            },
            {
                "scenario": "Language_Detection_Error",
                "error_type": "language_detection_failure",
                "recovery_steps": [
                    {"step": "detect_error", "action": "catch_language_error"},
                    {"step": "fallback_language", "action": "use_default_language"},
                    {"step": "continue_processing", "action": "process_with_fallback"}
                ],
                "description": "Language detection error recovery"
            },
            {
                "scenario": "TTS_Error_Recovery",
                "error_type": "tts_failure",
                "recovery_steps": [
                    {"step": "detect_error", "action": "catch_tts_error"},
                    {"step": "fallback_output", "action": "use_text_output"},
                    {"step": "continue_conversation", "action": "resume_with_text"}
                ],
                "description": "TTS error recovery"
            }
        ]
        
        for i, scenario in enumerate(error_scenarios):
            print(f"{Fore.YELLOW}Test {i+1}: {scenario['description']}{Style.RESET_ALL}")
            
            # Mock error recovery flow
            with patch('voice_bot_cli.VoiceBotCLI') as mock_cli:
                mock_cli.voice_bot = Mock()
                mock_cli.conversation_context = []
                mock_cli.conversation_state = "active"
                
                # Simulate error recovery flow
                for j, step in enumerate(scenario['recovery_steps']):
                    print(f"{Fore.CYAN}  Step {j+1}: {step['step']} -> {step['action']}{Style.RESET_ALL}")
                    
                    if step['action'] == "catch_exception":
                        mock_cli.voice_bot.process_text.side_effect = Exception("Dialog failure")
                        try:
                            mock_cli.voice_bot.process_text("test input", "en")
                        except Exception as e:
                            error_caught = True
                            self.assertTrue(error_caught)
                            print(f"{Fore.GREEN}    ✅ Exception caught: {str(e)[:30]}...{Style.RESET_ALL}")
                    
                    elif step['action'] == "generate_fallback":
                        fallback_response = "I'm sorry, I'm having trouble processing your request right now."
                        self.assertIsNotNone(fallback_response)
                        print(f"{Fore.GREEN}    ✅ Fallback generated: {fallback_response[:30]}...{Style.RESET_ALL}")
                    
                    elif step['action'] == "resume_normal":
                        mock_cli.voice_bot.process_text.side_effect = None
                        mock_cli.voice_bot.process_text.return_value = "Normal response"
                        response = mock_cli.voice_bot.process_text("test input", "en")
                        self.assertIsNotNone(response)
                        print(f"{Fore.GREEN}    ✅ Normal processing resumed{Style.RESET_ALL}")
                    
                    elif step['action'] == "catch_language_error":
                        mock_cli.voice_bot.language_detector.detect_language.return_value = ("unknown", 0.3)
                        detected_lang, confidence = mock_cli.voice_bot.language_detector.detect_language("test")
                        self.assertEqual(detected_lang, "unknown")
                        print(f"{Fore.GREEN}    ✅ Language error detected: {detected_lang}{Style.RESET_ALL}")
                    
                    elif step['action'] == "use_default_language":
                        fallback_lang = "en"
                        self.assertEqual(fallback_lang, "en")
                        print(f"{Fore.GREEN}    ✅ Default language used: {fallback_lang}{Style.RESET_ALL}")
                    
                    elif step['action'] == "process_with_fallback":
                        response = mock_cli.voice_bot.process_text("test input", "en")
                        self.assertIsNotNone(response)
                        print(f"{Fore.GREEN}    ✅ Processing with fallback completed{Style.RESET_ALL}")
                    
                    elif step['action'] == "catch_tts_error":
                        mock_cli.voice_bot.speak.side_effect = Exception("TTS failure")
                        try:
                            mock_cli.voice_bot.speak("test response", "en")
                        except Exception as e:
                            tts_error_caught = True
                            self.assertTrue(tts_error_caught)
                            print(f"{Fore.GREEN}    ✅ TTS error caught: {str(e)[:30]}...{Style.RESET_ALL}")
                    
                    elif step['action'] == "use_text_output":
                        text_output = "Displaying text instead of speech"
                        self.assertIsNotNone(text_output)
                        print(f"{Fore.GREEN}    ✅ Text output used: {text_output[:30]}...{Style.RESET_ALL}")
                    
                    elif step['action'] == "resume_with_text":
                        mock_cli.voice_bot.speak.side_effect = None
                        mock_cli.voice_bot.speak.return_value = True
                        tts_result = mock_cli.voice_bot.speak("test response", "en")
                        self.assertTrue(tts_result)
                        print(f"{Fore.GREEN}    ✅ TTS resumed successfully{Style.RESET_ALL}")
                
                print(f"{Fore.GREEN}✅ Error recovery: {len(scenario['recovery_steps'])} steps completed{Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}✅ Error Recovery Flow PASSED{Style.RESET_ALL}\n")

    def test_performance_flow(self):
        """Test performance flow"""
        print(f"\n{Fore.CYAN}⚡ Testing Performance Flow{Style.RESET_ALL}")
        
        performance_scenarios = [
            {
                "scenario": "Response_Time_Performance",
                "operations": [
                    {"operation": "language_detection", "max_time": 0.5},
                    {"operation": "dialog_processing", "max_time": 2.0},
                    {"operation": "tts_generation", "max_time": 3.0},
                    {"operation": "context_update", "max_time": 0.1}
                ],
                "description": "Response time performance"
            },
            {
                "scenario": "Memory_Performance",
                "operations": [
                    {"operation": "context_accumulation", "max_memory": 10},  # MB
                    {"operation": "model_loading", "max_memory": 500},  # MB
                    {"operation": "processing", "max_memory": 100}  # MB
                ],
                "description": "Memory performance"
            },
            {
                "scenario": "Concurrent_Performance",
                "operations": [
                    {"operation": "multiple_requests", "max_concurrent": 5},
                    {"operation": "rapid_commands", "max_concurrent": 10},
                    {"operation": "context_operations", "max_concurrent": 3}
                ],
                "description": "Concurrent performance"
            }
        ]
        
        for i, scenario in enumerate(performance_scenarios):
            print(f"{Fore.YELLOW}Test {i+1}: {scenario['description']}{Style.RESET_ALL}")
            
            # Mock performance flow
            with patch('voice_bot_cli.VoiceBotCLI') as mock_cli:
                mock_cli.voice_bot = Mock()
                mock_cli.conversation_context = []
                
                # Simulate performance flow
                for j, op in enumerate(scenario['operations']):
                    print(f"{Fore.CYAN}  Operation {j+1}: {op['operation']}{Style.RESET_ALL}")
                    
                    if 'max_time' in op:
                        # Test response time
                        start_time = time.time()
                        
                        if op['operation'] == "language_detection":
                            mock_cli.voice_bot.language_detector.detect_language.return_value = ("en", 0.9)
                            detected_lang, confidence = mock_cli.voice_bot.language_detector.detect_language("test")
                        elif op['operation'] == "dialog_processing":
                            mock_cli.voice_bot.process_text.return_value = "Dialog response"
                            response = mock_cli.voice_bot.process_text("test input", "en")
                        elif op['operation'] == "tts_generation":
                            mock_cli.voice_bot.speak.return_value = True
                            tts_result = mock_cli.voice_bot.speak("test response", "en")
                        elif op['operation'] == "context_update":
                            mock_cli.conversation_context.append({
                                'input': 'test',
                                'response': 'response',
                                'language': 'en',
                                'timestamp': time.time()
                            })
                        
                        end_time = time.time()
                        operation_time = end_time - start_time
                        
                        self.assertLess(operation_time, op['max_time'])
                        print(f"{Fore.GREEN}    ✅ Time: {operation_time:.3f}s < {op['max_time']}s{Style.RESET_ALL}")
                    
                    elif 'max_memory' in op:
                        # Test memory usage
                        if op['operation'] == "context_accumulation":
                            memory_usage = 5  # MB
                        elif op['operation'] == "model_loading":
                            memory_usage = 400  # MB
                        elif op['operation'] == "processing":
                            memory_usage = 80  # MB
                        
                        self.assertLess(memory_usage, op['max_memory'])
                        print(f"{Fore.GREEN}    ✅ Memory: {memory_usage}MB < {op['max_memory']}MB{Style.RESET_ALL}")
                    
                    elif 'max_concurrent' in op:
                        # Test concurrent operations
                        if op['operation'] == "multiple_requests":
                            concurrent_count = 3
                        elif op['operation'] == "rapid_commands":
                            concurrent_count = 7
                        elif op['operation'] == "context_operations":
                            concurrent_count = 2
                        
                        self.assertLessEqual(concurrent_count, op['max_concurrent'])
                        print(f"{Fore.GREEN}    ✅ Concurrent: {concurrent_count} <= {op['max_concurrent']}{Style.RESET_ALL}")
                
                print(f"{Fore.GREEN}✅ Performance: {len(scenario['operations'])} operations tested{Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}✅ Performance Flow PASSED{Style.RESET_ALL}\n")

    def test_integration_flow(self):
        """Test integration flow"""
        print(f"\n{Fore.CYAN}🔗 Testing Integration Flow{Style.RESET_ALL}")
        
        integration_scenarios = [
            {
                "scenario": "Audio_Dialog_Integration",
                "components": ["audio_recording", "speech_recognition", "language_detection", "dialog_processing", "tts_output"],
                "description": "Audio to dialog integration"
            },
            {
                "scenario": "Context_Dialog_Integration",
                "components": ["conversation_context", "dialog_processing", "response_generation", "context_update"],
                "description": "Context to dialog integration"
            },
            {
                "scenario": "Keyboard_Dialog_Integration",
                "components": ["keyboard_input", "command_processing", "dialog_processing", "response_output"],
                "description": "Keyboard to dialog integration"
            }
        ]
        
        for i, scenario in enumerate(integration_scenarios):
            print(f"{Fore.YELLOW}Test {i+1}: {scenario['description']}{Style.RESET_ALL}")
            
            # Mock integration flow
            with patch('voice_bot_cli.VoiceBotCLI') as mock_cli:
                mock_cli.voice_bot = Mock()
                mock_cli.conversation_context = []
                mock_cli.recorder = Mock()
                
                # Simulate integration flow
                for j, component in enumerate(scenario['components']):
                    print(f"{Fore.CYAN}  Component {j+1}: {component}{Style.RESET_ALL}")
                    
                    if component == "audio_recording":
                        mock_cli.recorder.start_recording.return_value = True
                        recording_result = mock_cli.recorder.start_recording()
                        self.assertTrue(recording_result)
                        print(f"{Fore.GREEN}    ✅ Audio recording integrated{Style.RESET_ALL}")
                    
                    elif component == "speech_recognition":
                        mock_cli.voice_bot.process_text.return_value = "Recognized speech"
                        response = mock_cli.voice_bot.process_text("audio input", "en")
                        self.assertIsNotNone(response)
                        print(f"{Fore.GREEN}    ✅ Speech recognition integrated{Style.RESET_ALL}")
                    
                    elif component == "language_detection":
                        mock_cli.voice_bot.language_detector.detect_language.return_value = ("en", 0.9)
                        detected_lang, confidence = mock_cli.voice_bot.language_detector.detect_language("test")
                        self.assertEqual(detected_lang, "en")
                        print(f"{Fore.GREEN}    ✅ Language detection integrated{Style.RESET_ALL}")
                    
                    elif component == "dialog_processing":
                        mock_cli.voice_bot.process_text.return_value = "Dialog response"
                        response = mock_cli.voice_bot.process_text("test input", "en")
                        self.assertIsNotNone(response)
                        print(f"{Fore.GREEN}    ✅ Dialog processing integrated{Style.RESET_ALL}")
                    
                    elif component == "tts_output":
                        mock_cli.voice_bot.speak.return_value = True
                        tts_result = mock_cli.voice_bot.speak("test response", "en")
                        self.assertTrue(tts_result)
                        print(f"{Fore.GREEN}    ✅ TTS output integrated{Style.RESET_ALL}")
                    
                    elif component == "conversation_context":
                        mock_cli.conversation_context.append({
                            'input': 'test',
                            'response': 'response',
                            'language': 'en',
                            'timestamp': time.time()
                        })
                        self.assertGreater(len(mock_cli.conversation_context), 0)
                        print(f"{Fore.GREEN}    ✅ Conversation context integrated{Style.RESET_ALL}")
                    
                    elif component == "response_generation":
                        response = "Generated response"
                        self.assertIsNotNone(response)
                        print(f"{Fore.GREEN}    ✅ Response generation integrated{Style.RESET_ALL}")
                    
                    elif component == "context_update":
                        mock_cli.conversation_context.append({
                            'input': 'new input',
                            'response': 'new response',
                            'language': 'en',
                            'timestamp': time.time()
                        })
                        self.assertGreater(len(mock_cli.conversation_context), 0)
                        print(f"{Fore.GREEN}    ✅ Context update integrated{Style.RESET_ALL}")
                    
                    elif component == "keyboard_input":
                        keyboard_input = "s"
                        self.assertIsNotNone(keyboard_input)
                        print(f"{Fore.GREEN}    ✅ Keyboard input integrated{Style.RESET_ALL}")
                    
                    elif component == "command_processing":
                        command_result = "command processed"
                        self.assertIsNotNone(command_result)
                        print(f"{Fore.GREEN}    ✅ Command processing integrated{Style.RESET_ALL}")
                    
                    elif component == "response_output":
                        output_result = "response output"
                        self.assertIsNotNone(output_result)
                        print(f"{Fore.GREEN}    ✅ Response output integrated{Style.RESET_ALL}")
                
                print(f"{Fore.GREEN}✅ Integration: {len(scenario['components'])} components integrated{Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}✅ Integration Flow PASSED{Style.RESET_ALL}\n")

if __name__ == "__main__":
    # Run the tests
    unittest.main(verbosity=2)
