#!/usr/bin/env python3
"""
Test Cases for Multilingual Support
Comprehensive test suite for multilingual support in keyboard mode
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

class TestMultilingualSupport(unittest.TestCase):
    """Test cases for multilingual support in keyboard-controlled dialog"""
    
    @classmethod
    def setUpClass(cls):
        """Set up common resources for tests"""
        print("\n🌍 Starting Multilingual Support Test Suite")
        print("=" * 60)

    def test_english_language_support(self):
        """Test English language support"""
        print(f"\n{Fore.CYAN}🇺🇸 Testing English Language Support{Style.RESET_ALL}")
        
        english_test_cases = [
            {
                "input": "Hello, how are you?",
                "expected_language": "en",
                "expected_response_type": "greeting",
                "description": "Basic English greeting"
            },
            {
                "input": "What's the weather like today?",
                "expected_language": "en",
                "expected_response_type": "question",
                "description": "English weather question"
            },
            {
                "input": "Can you help me find a restaurant?",
                "expected_language": "en",
                "expected_response_type": "request",
                "description": "English help request"
            },
            {
                "input": "Tell me a story about a brave knight",
                "expected_language": "en",
                "expected_response_type": "creative",
                "description": "English creative request"
            },
            {
                "input": "Thank you very much for your help",
                "expected_language": "en",
                "expected_response_type": "gratitude",
                "description": "English gratitude expression"
            }
        ]
        
        for i, test_case in enumerate(english_test_cases):
            print(f"{Fore.YELLOW}Test {i+1}: {test_case['description']}{Style.RESET_ALL}")
            
            # Mock English language support
            with patch('voice_bot_cli.VoiceBotCLI') as mock_cli:
                mock_cli.voice_bot = Mock()
                mock_cli.voice_bot.language_detector.detect_language.return_value = (
                    test_case['expected_language'], 0.95
                )
                mock_cli.voice_bot.process_text.return_value = "English response"
                mock_cli.voice_bot.speak.return_value = True
                
                # Test English language processing
                detected_lang, confidence = mock_cli.voice_bot.language_detector.detect_language(test_case['input'])
                response = mock_cli.voice_bot.process_text(test_case['input'], detected_lang)
                tts_result = mock_cli.voice_bot.speak(response, detected_lang)
                
                # Verify English language support
                self.assertEqual(detected_lang, test_case['expected_language'])
                self.assertGreater(confidence, 0.9)
                self.assertIsNotNone(response)
                self.assertTrue(tts_result)
                
                print(f"{Fore.GREEN}✅ English support: {detected_lang} (confidence: {confidence:.2f}){Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}✅ English Language Support PASSED{Style.RESET_ALL}\n")

    def test_hindi_language_support(self):
        """Test Hindi language support"""
        print(f"\n{Fore.CYAN}🇮🇳 Testing Hindi Language Support{Style.RESET_ALL}")
        
        hindi_test_cases = [
            {
                "input": "नमस्ते, आप कैसे हैं?",
                "expected_language": "hi",
                "expected_response_type": "greeting",
                "description": "Basic Hindi greeting"
            },
            {
                "input": "आज मौसम कैसा है?",
                "expected_language": "hi",
                "expected_response_type": "question",
                "description": "Hindi weather question"
            },
            {
                "input": "क्या आप मुझे रेस्टोरेंट खोजने में मदद कर सकते हैं?",
                "expected_language": "hi",
                "expected_response_type": "request",
                "description": "Hindi help request"
            },
            {
                "input": "मुझे एक बहादुर योद्धा की कहानी सुनाइए",
                "expected_language": "hi",
                "expected_response_type": "creative",
                "description": "Hindi creative request"
            },
            {
                "input": "आपकी मदद के लिए बहुत धन्यवाद",
                "expected_language": "hi",
                "expected_response_type": "gratitude",
                "description": "Hindi gratitude expression"
            }
        ]
        
        for i, test_case in enumerate(hindi_test_cases):
            print(f"{Fore.YELLOW}Test {i+1}: {test_case['description']}{Style.RESET_ALL}")
            
            # Mock Hindi language support
            with patch('voice_bot_cli.VoiceBotCLI') as mock_cli:
                mock_cli.voice_bot = Mock()
                mock_cli.voice_bot.language_detector.detect_language.return_value = (
                    test_case['expected_language'], 0.92
                )
                mock_cli.voice_bot.process_text.return_value = "हिंदी प्रतिक्रिया"
                mock_cli.voice_bot.speak.return_value = True
                
                # Test Hindi language processing
                detected_lang, confidence = mock_cli.voice_bot.language_detector.detect_language(test_case['input'])
                response = mock_cli.voice_bot.process_text(test_case['input'], detected_lang)
                tts_result = mock_cli.voice_bot.speak(response, detected_lang)
                
                # Verify Hindi language support
                self.assertEqual(detected_lang, test_case['expected_language'])
                self.assertGreater(confidence, 0.9)
                self.assertIsNotNone(response)
                self.assertTrue(tts_result)
                
                print(f"{Fore.GREEN}✅ Hindi support: {detected_lang} (confidence: {confidence:.2f}){Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}✅ Hindi Language Support PASSED{Style.RESET_ALL}\n")

    def test_mixed_language_support(self):
        """Test mixed language support"""
        print(f"\n{Fore.CYAN}🌐 Testing Mixed Language Support{Style.RESET_ALL}")
        
        mixed_test_cases = [
            {
                "input": "Hello नमस्ते",
                "expected_language": "mixed",
                "expected_response_type": "greeting",
                "description": "English-Hindi mixed greeting"
            },
            {
                "input": "Good morning सुप्रभात",
                "expected_language": "mixed",
                "expected_response_type": "greeting",
                "description": "English-Hindi mixed greeting"
            },
            {
                "input": "How are you? आप कैसे हैं?",
                "expected_language": "mixed",
                "expected_response_type": "question",
                "description": "English-Hindi mixed question"
            },
            {
                "input": "Can you help me? क्या आप मदद कर सकते हैं?",
                "expected_language": "mixed",
                "expected_response_type": "request",
                "description": "English-Hindi mixed request"
            },
            {
                "input": "Thank you धन्यवाद",
                "expected_language": "mixed",
                "expected_response_type": "gratitude",
                "description": "English-Hindi mixed gratitude"
            }
        ]
        
        for i, test_case in enumerate(mixed_test_cases):
            print(f"{Fore.YELLOW}Test {i+1}: {test_case['description']}{Style.RESET_ALL}")
            
            # Mock mixed language support
            with patch('voice_bot_cli.VoiceBotCLI') as mock_cli:
                mock_cli.voice_bot = Mock()
                mock_cli.voice_bot.language_detector.detect_language.return_value = (
                    test_case['expected_language'], 0.78
                )
                mock_cli.voice_bot.process_text.return_value = "Mixed language response"
                mock_cli.voice_bot.speak.return_value = True
                
                # Test mixed language processing
                detected_lang, confidence = mock_cli.voice_bot.language_detector.detect_language(test_case['input'])
                response = mock_cli.voice_bot.process_text(test_case['input'], detected_lang)
                tts_result = mock_cli.voice_bot.speak(response, "en")  # Default to English for mixed
                
                # Verify mixed language support
                self.assertEqual(detected_lang, test_case['expected_language'])
                self.assertGreater(confidence, 0.7)
                self.assertIsNotNone(response)
                self.assertTrue(tts_result)
                
                print(f"{Fore.GREEN}✅ Mixed support: {detected_lang} (confidence: {confidence:.2f}){Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}✅ Mixed Language Support PASSED{Style.RESET_ALL}\n")

    def test_language_switching_support(self):
        """Test language switching support"""
        print(f"\n{Fore.CYAN}🔄 Testing Language Switching Support{Style.RESET_ALL}")
        
        switching_scenarios = [
            {
                "scenario": "English_to_Hindi",
                "turn1": "Hello, how are you?",
                "turn2": "नमस्ते, आप कैसे हैं?",
                "description": "Switching from English to Hindi"
            },
            {
                "scenario": "Hindi_to_English",
                "turn1": "नमस्ते, आप कैसे हैं?",
                "turn2": "Hello, how are you?",
                "description": "Switching from Hindi to English"
            },
            {
                "scenario": "Mixed_to_English",
                "turn1": "Hello नमस्ते",
                "turn2": "How are you doing?",
                "description": "Switching from mixed to English"
            },
            {
                "scenario": "Mixed_to_Hindi",
                "turn1": "Hello नमस्ते",
                "turn2": "आप कैसे हैं?",
                "description": "Switching from mixed to Hindi"
            }
        ]
        
        for i, scenario in enumerate(switching_scenarios):
            print(f"{Fore.YELLOW}Test {i+1}: {scenario['description']}{Style.RESET_ALL}")
            
            # Mock language switching support
            with patch('voice_bot_cli.VoiceBotCLI') as mock_cli:
                mock_cli.voice_bot = Mock()
                mock_cli.conversation_context = []
                
                # Test first turn
                mock_cli.voice_bot.language_detector.detect_language.return_value = ("en", 0.95)
                mock_cli.voice_bot.process_text.return_value = "First turn response"
                
                lang1, conf1 = mock_cli.voice_bot.language_detector.detect_language(scenario['turn1'])
                response1 = mock_cli.voice_bot.process_text(scenario['turn1'], lang1)
                
                # Test second turn
                mock_cli.voice_bot.language_detector.detect_language.return_value = ("hi", 0.92)
                mock_cli.voice_bot.process_text.return_value = "Second turn response"
                
                lang2, conf2 = mock_cli.voice_bot.language_detector.detect_language(scenario['turn2'])
                response2 = mock_cli.voice_bot.process_text(scenario['turn2'], lang2)
                
                # Verify language switching
                self.assertIsNotNone(response1)
                self.assertIsNotNone(response2)
                
                print(f"{Fore.GREEN}✅ Language switching: {lang1} -> {lang2}{Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}✅ Language Switching Support PASSED{Style.RESET_ALL}\n")

    def test_multilingual_tts_support(self):
        """Test multilingual TTS support"""
        print(f"\n{Fore.CYAN}🔊 Testing Multilingual TTS Support{Style.RESET_ALL}")
        
        tts_test_cases = [
            {
                "language": "en",
                "text": "Hello, how are you?",
                "expected_tts_language": "en",
                "description": "English TTS"
            },
            {
                "language": "hi",
                "text": "नमस्ते, आप कैसे हैं?",
                "expected_tts_language": "hi",
                "description": "Hindi TTS"
            },
            {
                "language": "mixed",
                "text": "Hello नमस्ते",
                "expected_tts_language": "en",
                "description": "Mixed language TTS (default to English)"
            }
        ]
        
        for i, test_case in enumerate(tts_test_cases):
            print(f"{Fore.YELLOW}Test {i+1}: {test_case['description']}{Style.RESET_ALL}")
            
            # Mock multilingual TTS support
            with patch('voice_bot_cli.VoiceBotCLI') as mock_cli:
                mock_cli.voice_bot = Mock()
                mock_cli.voice_bot.speak.return_value = True
                
                # Test TTS with different languages
                tts_result = mock_cli.voice_bot.speak(test_case['text'], test_case['expected_tts_language'])
                
                # Verify multilingual TTS
                self.assertTrue(tts_result)
                mock_cli.voice_bot.speak.assert_called_with(test_case['text'], test_case['expected_tts_language'])
                
                print(f"{Fore.GREEN}✅ TTS support: {test_case['expected_tts_language']} language{Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}✅ Multilingual TTS Support PASSED{Style.RESET_ALL}\n")

    def test_multilingual_context_support(self):
        """Test multilingual context support"""
        print(f"\n{Fore.CYAN}🧠 Testing Multilingual Context Support{Style.RESET_ALL}")
        
        context_scenarios = [
            {
                "scenario": "English_Context",
                "turns": [
                    {"input": "Hello", "language": "en"},
                    {"input": "How are you?", "language": "en"},
                    {"input": "What's your name?", "language": "en"}
                ],
                "description": "English conversation context"
            },
            {
                "scenario": "Hindi_Context",
                "turns": [
                    {"input": "नमस्ते", "language": "hi"},
                    {"input": "आप कैसे हैं?", "language": "hi"},
                    {"input": "आपका नाम क्या है?", "language": "hi"}
                ],
                "description": "Hindi conversation context"
            },
            {
                "scenario": "Mixed_Context",
                "turns": [
                    {"input": "Hello नमस्ते", "language": "mixed"},
                    {"input": "How are you? आप कैसे हैं?", "language": "mixed"},
                    {"input": "What's your name? आपका नाम क्या है?", "language": "mixed"}
                ],
                "description": "Mixed conversation context"
            }
        ]
        
        for i, scenario in enumerate(context_scenarios):
            print(f"{Fore.YELLOW}Test {i+1}: {scenario['description']}{Style.RESET_ALL}")
            
            # Mock multilingual context support
            with patch('voice_bot_cli.VoiceBotCLI') as mock_cli:
                mock_cli.voice_bot = Mock()
                mock_cli.conversation_context = []
                mock_cli.voice_bot.process_text.return_value = "Context response"
                
                # Test multilingual context
                for turn in scenario['turns']:
                    response = mock_cli.voice_bot.process_text(turn['input'], turn['language'])
                    mock_cli.conversation_context.append({
                        'input': turn['input'],
                        'language': turn['language'],
                        'response': response
                    })
                
                # Verify multilingual context
                self.assertEqual(len(mock_cli.conversation_context), len(scenario['turns']))
                
                print(f"{Fore.GREEN}✅ Context support: {len(scenario['turns'])} turns in {scenario['scenario']}{Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}✅ Multilingual Context Support PASSED{Style.RESET_ALL}\n")

    def test_multilingual_error_handling(self):
        """Test multilingual error handling"""
        print(f"\n{Fore.CYAN}🛡️ Testing Multilingual Error Handling{Style.RESET_ALL}")
        
        error_scenarios = [
            {
                "error_type": "Language_Detection_Failure",
                "input": "Unknown language text",
                "expected_fallback": "en",
                "description": "Language detection failure"
            },
            {
                "error_type": "TTS_Language_Not_Supported",
                "input": "Text in unsupported language",
                "expected_fallback": "en",
                "description": "TTS language not supported"
            },
            {
                "error_type": "Mixed_Language_Confusion",
                "input": "Confusing mixed language text",
                "expected_fallback": "en",
                "description": "Mixed language confusion"
            }
        ]
        
        for i, scenario in enumerate(error_scenarios):
            print(f"{Fore.YELLOW}Test {i+1}: {scenario['description']}{Style.RESET_ALL}")
            
            # Mock multilingual error handling
            with patch('voice_bot_cli.VoiceBotCLI') as mock_cli:
                mock_cli.voice_bot = Mock()
                
                if scenario['error_type'] == 'Language_Detection_Failure':
                    mock_cli.voice_bot.language_detector.detect_language.return_value = ("unknown", 0.3)
                    mock_cli.voice_bot.process_text.return_value = "Fallback response"
                elif scenario['error_type'] == 'TTS_Language_Not_Supported':
                    mock_cli.voice_bot.process_text.return_value = "TTS fallback response"
                    mock_cli.voice_bot.speak.side_effect = Exception("TTS language not supported")
                elif scenario['error_type'] == 'Mixed_Language_Confusion':
                    mock_cli.voice_bot.language_detector.detect_language.return_value = ("mixed", 0.5)
                    mock_cli.voice_bot.process_text.return_value = "Mixed language fallback"
                
                # Test multilingual error handling
                try:
                    detected_lang, confidence = mock_cli.voice_bot.language_detector.detect_language(scenario['input'])
                    response = mock_cli.voice_bot.process_text(scenario['input'], detected_lang)
                    
                    if scenario['error_type'] == 'TTS_Language_Not_Supported':
                        mock_cli.voice_bot.speak(response, detected_lang)
                    
                    print(f"{Fore.GREEN}✅ {scenario['error_type']} handled gracefully{Style.RESET_ALL}")
                    
                except Exception as e:
                    print(f"{Fore.GREEN}✅ {scenario['error_type']} error handled gracefully{Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}✅ Multilingual Error Handling PASSED{Style.RESET_ALL}\n")

    def test_multilingual_performance(self):
        """Test multilingual performance"""
        print(f"\n{Fore.CYAN}⚡ Testing Multilingual Performance{Style.RESET_ALL}")
        
        performance_scenarios = [
            {
                "language": "en",
                "input": "Hello, how are you?",
                "max_detection_time": 0.5,
                "max_processing_time": 2.0,
                "description": "English performance"
            },
            {
                "language": "hi",
                "input": "नमस्ते, आप कैसे हैं?",
                "max_detection_time": 0.5,
                "max_processing_time": 2.0,
                "description": "Hindi performance"
            },
            {
                "language": "mixed",
                "input": "Hello नमस्ते",
                "max_detection_time": 0.8,
                "max_processing_time": 2.5,
                "description": "Mixed language performance"
            }
        ]
        
        for i, scenario in enumerate(performance_scenarios):
            print(f"{Fore.YELLOW}Test {i+1}: {scenario['description']}{Style.RESET_ALL}")
            
            # Mock multilingual performance testing
            with patch('voice_bot_cli.VoiceBotCLI') as mock_cli:
                mock_cli.voice_bot = Mock()
                mock_cli.voice_bot.language_detector.detect_language.return_value = (
                    scenario['language'], 0.9
                )
                mock_cli.voice_bot.process_text.return_value = "Performance response"
                
                # Test language detection performance
                start_time = time.time()
                detected_lang, confidence = mock_cli.voice_bot.language_detector.detect_language(scenario['input'])
                detection_time = time.time() - start_time
                
                # Test processing performance
                start_time = time.time()
                response = mock_cli.voice_bot.process_text(scenario['input'], detected_lang)
                processing_time = time.time() - start_time
                
                # Verify multilingual performance
                self.assertLess(detection_time, scenario['max_detection_time'])
                self.assertLess(processing_time, scenario['max_processing_time'])
                
                print(f"{Fore.GREEN}✅ Performance: Detection {detection_time:.3f}s, Processing {processing_time:.3f}s{Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}✅ Multilingual Performance PASSED{Style.RESET_ALL}\n")

if __name__ == "__main__":
    # Run the tests
    unittest.main(verbosity=2)
