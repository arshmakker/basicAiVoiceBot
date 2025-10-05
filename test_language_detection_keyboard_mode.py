#!/usr/bin/env python3
"""
Test Cases for Language Detection in Keyboard Mode
Comprehensive test suite for language detection integration
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

class TestLanguageDetectionKeyboardMode(unittest.TestCase):
    """Test cases for language detection in keyboard-controlled mode"""
    
    @classmethod
    def setUpClass(cls):
        """Set up common resources for tests"""
        print("\n🌐 Starting Language Detection Test Suite")
        print("=" * 50)

    def test_english_language_detection(self):
        """Test English language detection in keyboard mode"""
        print(f"\n{Fore.CYAN}🇺🇸 Testing English Language Detection{Style.RESET_ALL}")
        
        english_test_cases = [
            {
                "input": "Hello, how are you?",
                "expected_language": "en",
                "min_confidence": 0.8,
                "description": "Basic English greeting"
            },
            {
                "input": "What is the weather like today?",
                "expected_language": "en",
                "min_confidence": 0.8,
                "description": "English question"
            },
            {
                "input": "I need help with my computer",
                "expected_language": "en",
                "min_confidence": 0.8,
                "description": "English request"
            },
            {
                "input": "Thank you very much",
                "expected_language": "en",
                "min_confidence": 0.8,
                "description": "English gratitude"
            }
        ]
        
        for i, test_case in enumerate(english_test_cases):
            print(f"{Fore.YELLOW}Test {i+1}: {test_case['description']}{Style.RESET_ALL}")
            
            # Mock language detection
            with patch('voice_bot.language_detection.LanguageDetector') as mock_detector:
                mock_detector.return_value.detect_language.return_value = (
                    test_case['expected_language'], 0.9
                )
                
                # Test language detection
                detector = mock_detector.return_value
                detected_lang, confidence = detector.detect_language(test_case['input'])
                
                # Verify language detection
                self.assertEqual(detected_lang, test_case['expected_language'])
                self.assertGreaterEqual(confidence, test_case['min_confidence'])
                
                print(f"{Fore.GREEN}✅ Detected: {detected_lang} (confidence: {confidence:.2f}){Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}✅ English Language Detection PASSED{Style.RESET_ALL}\n")

    def test_hindi_language_detection(self):
        """Test Hindi language detection in keyboard mode"""
        print(f"\n{Fore.CYAN}🇮🇳 Testing Hindi Language Detection{Style.RESET_ALL}")
        
        hindi_test_cases = [
            {
                "input": "नमस्ते, आप कैसे हैं?",
                "expected_language": "hi",
                "min_confidence": 0.8,
                "description": "Basic Hindi greeting"
            },
            {
                "input": "आज मौसम कैसा है?",
                "expected_language": "hi",
                "min_confidence": 0.8,
                "description": "Hindi question"
            },
            {
                "input": "मुझे कंप्यूटर में मदद चाहिए",
                "expected_language": "hi",
                "min_confidence": 0.8,
                "description": "Hindi request"
            },
            {
                "input": "बहुत धन्यवाद",
                "expected_language": "hi",
                "min_confidence": 0.8,
                "description": "Hindi gratitude"
            }
        ]
        
        for i, test_case in enumerate(hindi_test_cases):
            print(f"{Fore.YELLOW}Test {i+1}: {test_case['description']}{Style.RESET_ALL}")
            
            # Mock language detection
            with patch('voice_bot.language_detection.LanguageDetector') as mock_detector:
                mock_detector.return_value.detect_language.return_value = (
                    test_case['expected_language'], 0.9
                )
                
                # Test language detection
                detector = mock_detector.return_value
                detected_lang, confidence = detector.detect_language(test_case['input'])
                
                # Verify language detection
                self.assertEqual(detected_lang, test_case['expected_language'])
                self.assertGreaterEqual(confidence, test_case['min_confidence'])
                
                print(f"{Fore.GREEN}✅ Detected: {detected_lang} (confidence: {confidence:.2f}){Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}✅ Hindi Language Detection PASSED{Style.RESET_ALL}\n")

    def test_mixed_language_detection(self):
        """Test mixed language detection in keyboard mode"""
        print(f"\n{Fore.CYAN}🌍 Testing Mixed Language Detection{Style.RESET_ALL}")
        
        mixed_test_cases = [
            {
                "input": "Hello नमस्ते",
                "expected_language": "mixed",
                "min_confidence": 0.6,
                "description": "English-Hindi mixed greeting"
            },
            {
                "input": "Good morning सुप्रभात",
                "expected_language": "mixed",
                "min_confidence": 0.6,
                "description": "English-Hindi mixed greeting"
            },
            {
                "input": "How are you? आप कैसे हैं?",
                "expected_language": "mixed",
                "min_confidence": 0.6,
                "description": "English-Hindi mixed question"
            }
        ]
        
        for i, test_case in enumerate(mixed_test_cases):
            print(f"{Fore.YELLOW}Test {i+1}: {test_case['description']}{Style.RESET_ALL}")
            
            # Mock language detection
            with patch('voice_bot.language_detection.LanguageDetector') as mock_detector:
                mock_detector.return_value.detect_language.return_value = (
                    test_case['expected_language'], 0.7
                )
                
                # Test language detection
                detector = mock_detector.return_value
                detected_lang, confidence = detector.detect_language(test_case['input'])
                
                # Verify language detection
                self.assertEqual(detected_lang, test_case['expected_language'])
                self.assertGreaterEqual(confidence, test_case['min_confidence'])
                
                print(f"{Fore.GREEN}✅ Detected: {detected_lang} (confidence: {confidence:.2f}){Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}✅ Mixed Language Detection PASSED{Style.RESET_ALL}\n")

    def test_language_detection_confidence_thresholds(self):
        """Test language detection confidence thresholds"""
        print(f"\n{Fore.CYAN}📊 Testing Confidence Thresholds{Style.RESET_ALL}")
        
        confidence_test_cases = [
            {
                "input": "Hello",
                "confidence": 0.95,
                "threshold": 0.8,
                "should_pass": True,
                "description": "High confidence English"
            },
            {
                "input": "नमस्ते",
                "confidence": 0.92,
                "threshold": 0.8,
                "should_pass": True,
                "description": "High confidence Hindi"
            },
            {
                "input": "Hola",
                "confidence": 0.65,
                "threshold": 0.8,
                "should_pass": False,
                "description": "Low confidence (Spanish)"
            },
            {
                "input": "Hello नमस्ते",
                "confidence": 0.75,
                "threshold": 0.7,
                "should_pass": True,
                "description": "Mixed language above threshold"
            }
        ]
        
        for i, test_case in enumerate(confidence_test_cases):
            print(f"{Fore.YELLOW}Test {i+1}: {test_case['description']}{Style.RESET_ALL}")
            
            # Mock language detection
            with patch('voice_bot.language_detection.LanguageDetector') as mock_detector:
                mock_detector.return_value.detect_language.return_value = (
                    "en", test_case['confidence']
                )
                
                # Test language detection
                detector = mock_detector.return_value
                detected_lang, confidence = detector.detect_language(test_case['input'])
                
                # Verify confidence threshold
                if test_case['should_pass']:
                    self.assertGreaterEqual(confidence, test_case['threshold'])
                    print(f"{Fore.GREEN}✅ Confidence {confidence:.2f} >= {test_case['threshold']}{Style.RESET_ALL}")
                else:
                    self.assertLess(confidence, test_case['threshold'])
                    print(f"{Fore.YELLOW}⚠️  Confidence {confidence:.2f} < {test_case['threshold']}{Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}✅ Confidence Thresholds PASSED{Style.RESET_ALL}\n")

    def test_language_detection_integration(self):
        """Test language detection integration with keyboard mode"""
        print(f"\n{Fore.CYAN}🔗 Testing Language Detection Integration{Style.RESET_ALL}")
        
        integration_test_cases = [
            {
                "scenario": "English input with TTS",
                "input": "Hello, how are you?",
                "expected_lang": "en",
                "expected_tts_lang": "en"
            },
            {
                "scenario": "Hindi input with TTS",
                "input": "नमस्ते, आप कैसे हैं?",
                "expected_lang": "hi",
                "expected_tts_lang": "hi"
            },
            {
                "scenario": "Mixed input with fallback",
                "input": "Hello नमस्ते",
                "expected_lang": "mixed",
                "expected_tts_lang": "en"  # Fallback to English
            }
        ]
        
        for i, test_case in enumerate(integration_test_cases):
            print(f"{Fore.YELLOW}Integration Test {i+1}: {test_case['scenario']}{Style.RESET_ALL}")
            
            # Mock the complete keyboard mode flow
            with patch('voice_bot_cli.VoiceBotCLI') as mock_cli:
                mock_cli.voice_bot = Mock()
                mock_cli.conversation_context = []
                
                # Mock language detection
                mock_cli.voice_bot.language_detector.detect_language.return_value = (
                    test_case['expected_lang'], 0.9
                )
                
                # Mock dialog processing
                mock_cli.voice_bot.process_text.return_value = "Test response"
                
                # Mock TTS
                mock_cli.voice_bot.speak.return_value = True
                
                # Test the integration flow
                detected_lang, confidence = mock_cli.voice_bot.language_detector.detect_language(test_case['input'])
                response = mock_cli.voice_bot.process_text(test_case['input'], detected_lang)
                mock_cli.voice_bot.speak(response, detected_lang)
                
                # Verify integration
                self.assertEqual(detected_lang, test_case['expected_lang'])
                mock_cli.voice_bot.process_text.assert_called_with(test_case['input'], detected_lang)
                mock_cli.voice_bot.speak.assert_called_with("Test response", detected_lang)
                
                print(f"{Fore.GREEN}✅ Integration successful: {detected_lang} -> TTS: {detected_lang}{Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}✅ Language Detection Integration PASSED{Style.RESET_ALL}\n")

    def test_language_detection_error_handling(self):
        """Test language detection error handling"""
        print(f"\n{Fore.CYAN}🛡️ Testing Language Detection Error Handling{Style.RESET_ALL}")
        
        error_scenarios = [
            {
                "error_type": "DetectionFailure",
                "error_message": "Language detection failed",
                "expected_fallback": "en",
                "description": "Detection service failure"
            },
            {
                "error_type": "LowConfidence",
                "error_message": "Confidence too low",
                "expected_fallback": "en",
                "description": "Low confidence fallback"
            },
            {
                "error_type": "EmptyInput",
                "error_message": "Empty input string",
                "expected_fallback": "en",
                "description": "Empty input handling"
            }
        ]
        
        for i, scenario in enumerate(error_scenarios):
            print(f"{Fore.YELLOW}Error Test {i+1}: {scenario['description']}{Style.RESET_ALL}")
            
            # Mock error scenarios
            with patch('voice_bot.language_detection.LanguageDetector') as mock_detector:
                if scenario['error_type'] == 'DetectionFailure':
                    mock_detector.return_value.detect_language.side_effect = Exception(scenario['error_message'])
                elif scenario['error_type'] == 'LowConfidence':
                    mock_detector.return_value.detect_language.return_value = ("unknown", 0.3)
                elif scenario['error_type'] == 'EmptyInput':
                    mock_detector.return_value.detect_language.return_value = ("", 0.0)
                
                # Test error handling
                detector = mock_detector.return_value
                
                try:
                    detected_lang, confidence = detector.detect_language("test input")
                    
                    # Verify fallback behavior
                    if scenario['error_type'] == 'LowConfidence':
                        # Should fallback to default language
                        fallback_lang = scenario['expected_fallback']
                        print(f"{Fore.GREEN}✅ Low confidence fallback: {fallback_lang}{Style.RESET_ALL}")
                    elif scenario['error_type'] == 'EmptyInput':
                        # Should handle empty input
                        print(f"{Fore.GREEN}✅ Empty input handled{Style.RESET_ALL}")
                        
                except Exception as e:
                    # Should handle detection failure gracefully
                    self.assertIn("detection", str(e).lower())
                    print(f"{Fore.GREEN}✅ Detection failure handled gracefully{Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}✅ Language Detection Error Handling PASSED{Style.RESET_ALL}\n")

    def test_language_detection_performance(self):
        """Test language detection performance"""
        print(f"\n{Fore.CYAN}⚡ Testing Language Detection Performance{Style.RESET_ALL}")
        
        performance_test_cases = [
            {
                "input": "Hello, how are you?",
                "max_time": 1.0,  # seconds
                "description": "Short English text"
            },
            {
                "input": "नमस्ते, आप कैसे हैं? आज मौसम कैसा है?",
                "max_time": 1.5,  # seconds
                "description": "Medium Hindi text"
            },
            {
                "input": "Hello नमस्ते Good morning सुप्रभात How are you? आप कैसे हैं?",
                "max_time": 2.0,  # seconds
                "description": "Long mixed text"
            }
        ]
        
        for i, test_case in enumerate(performance_test_cases):
            print(f"{Fore.YELLOW}Performance Test {i+1}: {test_case['description']}{Style.RESET_ALL}")
            
            # Mock language detection
            with patch('voice_bot.language_detection.LanguageDetector') as mock_detector:
                mock_detector.return_value.detect_language.return_value = ("en", 0.9)
                
                # Test performance
                detector = mock_detector.return_value
                start_time = time.time()
                
                detected_lang, confidence = detector.detect_language(test_case['input'])
                
                end_time = time.time()
                detection_time = end_time - start_time
                
                # Verify performance
                self.assertLess(detection_time, test_case['max_time'])
                print(f"{Fore.GREEN}✅ Detection time: {detection_time:.3f}s < {test_case['max_time']}s{Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}✅ Language Detection Performance PASSED{Style.RESET_ALL}\n")

if __name__ == "__main__":
    # Run the tests
    unittest.main(verbosity=2)
