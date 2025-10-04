"""
Language Detection Module
Detects language of input text (English/Hindi)
"""

import re
import logging
from typing import Optional, Dict, List, Tuple
from collections import Counter

try:
    from langdetect import detect, detect_langs, DetectorFactory
    from langdetect.lang_detect_exception import LangDetectException
except ImportError:
    detect = None
    detect_langs = None
    DetectorFactory = None
    LangDetectException = Exception


class LanguageDetectionError(Exception):
    """Custom exception for language detection errors"""
    pass


class LanguageDetector:
    """
    Language detector for English and Hindi text
    """
    
    def __init__(self, confidence_threshold: float = 0.6):
        """
        Initialize language detector
        
        Args:
            confidence_threshold: Minimum confidence for language detection
        """
        self.confidence_threshold = confidence_threshold
        
        # Hindi character patterns
        self.hindi_patterns = [
            r'[\u0900-\u097F]',  # Devanagari script
            r'[\u0980-\u09FF]',  # Bengali script (sometimes used for Hindi)
        ]
        
        # English character patterns
        self.english_patterns = [
            r'[a-zA-Z]',  # Latin letters
        ]
        
        # Common Hindi words
        self.hindi_words = {
            'है', 'हैं', 'था', 'थे', 'था', 'थी', 'हो', 'होता', 'होती', 'होते',
            'मैं', 'तुम', 'आप', 'वह', 'यह', 'हम', 'उन्हें', 'इस', 'उस', 'क्या',
            'कैसे', 'कब', 'कहाँ', 'क्यों', 'कौन', 'कितना', 'कितनी', 'कितने',
            'अच्छा', 'बुरा', 'बड़ा', 'छोटा', 'नया', 'पुराना', 'सुंदर', 'अच्छी',
            'धन्यवाद', 'शुक्रिया', 'नमस्ते', 'नमस्कार', 'हैलो', 'अलविदा',
            'हाँ', 'नहीं', 'हो सकता', 'शायद', 'ज़रूर', 'बिल्कुल'
        }
        
        # Common English words
        self.english_words = {
            'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i',
            'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
            'this', 'but', 'his', 'by', 'from', 'they', 'she', 'or', 'an',
            'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what',
            'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go',
            'me', 'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him',
            'know', 'take', 'people', 'into', 'year', 'your', 'good', 'some',
            'could', 'them', 'see', 'other', 'than', 'then', 'now', 'look',
            'only', 'come', 'its', 'over', 'think', 'also', 'back', 'after',
            'use', 'two', 'how', 'our', 'work', 'first', 'well', 'way', 'even',
            'new', 'want', 'because', 'any', 'these', 'give', 'day', 'most',
            'us', 'is', 'was', 'are', 'were', 'been', 'being', 'have', 'has',
            'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
            'may', 'might', 'must', 'can', 'shall'
        }
        
        # Initialize langdetect if available
        if DetectorFactory:
            DetectorFactory.seed = 0  # For consistent results
    
    def detect_language(self, text: str) -> Tuple[str, float]:
        """
        Detect language of input text
        
        Args:
            text: Input text to analyze
            
        Returns:
            Tuple of (language_code, confidence)
        """
        if not text or not text.strip():
            return "en", 0.0
        
        text = text.strip()
        
        # Try langdetect first if available
        if detect:
            try:
                detected_lang = detect(text)
                confidence = self._get_langdetect_confidence(text)
                
                # Map langdetect results to our supported languages
                if detected_lang in ['hi', 'hi-Latn']:
                    return "hi", confidence
                elif detected_lang in ['en']:
                    return "en", confidence
                else:
                    # Fallback to pattern-based detection
                    return self._pattern_based_detection(text)
                    
            except LangDetectException:
                # Fallback to pattern-based detection
                return self._pattern_based_detection(text)
        else:
            # Use pattern-based detection
            return self._pattern_based_detection(text)
    
    def _get_langdetect_confidence(self, text: str) -> float:
        """Get confidence from langdetect"""
        if not detect_langs:
            return 0.5
        
        try:
            languages = detect_langs(text)
            if languages:
                return languages[0].prob
        except:
            pass
        
        return 0.5
    
    def _pattern_based_detection(self, text: str) -> Tuple[str, float]:
        """
        Pattern-based language detection using character analysis
        
        Args:
            text: Input text
            
        Returns:
            Tuple of (language_code, confidence)
        """
        # Count characters by script
        hindi_chars = 0
        english_chars = 0
        
        for char in text:
            if any(re.search(pattern, char) for pattern in self.hindi_patterns):
                hindi_chars += 1
            elif any(re.search(pattern, char) for pattern in self.english_patterns):
                english_chars += 1
        
        # Count words by language
        words = re.findall(r'\b\w+\b', text.lower())
        hindi_word_count = sum(1 for word in words if word in self.hindi_words)
        english_word_count = sum(1 for word in words if word in self.english_words)
        
        # Calculate scores
        total_chars = hindi_chars + english_chars
        total_words = hindi_word_count + english_word_count
        
        if total_chars == 0 and total_words == 0:
            return "en", 0.5  # Default to English
        
        # Character-based score
        char_score_hindi = hindi_chars / total_chars if total_chars > 0 else 0
        char_score_english = english_chars / total_chars if total_chars > 0 else 0
        
        # Word-based score
        word_score_hindi = hindi_word_count / total_words if total_words > 0 else 0
        word_score_english = english_word_count / total_words if total_words > 0 else 0
        
        # Combined score (weighted average)
        hindi_score = (char_score_hindi * 0.7) + (word_score_hindi * 0.3)
        english_score = (char_score_english * 0.7) + (word_score_english * 0.3)
        
        # Determine language
        if hindi_score > english_score:
            confidence = min(hindi_score, 0.95)  # Cap confidence
            return "hi", confidence
        else:
            confidence = min(english_score, 0.95)
            return "en", confidence
    
    def is_hindi(self, text: str) -> bool:
        """
        Check if text is in Hindi
        
        Args:
            text: Input text
            
        Returns:
            True if text is in Hindi
        """
        language, confidence = self.detect_language(text)
        return language == "hi" and confidence >= self.confidence_threshold
    
    def is_english(self, text: str) -> bool:
        """
        Check if text is in English
        
        Args:
            text: Input text
            
        Returns:
            True if text is in English
        """
        language, confidence = self.detect_language(text)
        return language == "en" and confidence >= self.confidence_threshold
    
    def get_language_with_confidence(self, text: str) -> Dict[str, float]:
        """
        Get language detection results with confidence scores
        
        Args:
            text: Input text
            
        Returns:
            Dictionary with language codes and confidence scores
        """
        detected_lang, confidence = self.detect_language(text)
        
        result = {
            "detected_language": detected_lang,
            "confidence": confidence,
            "is_hindi": detected_lang == "hi",
            "is_english": detected_lang == "en"
        }
        
        # Add individual language scores if using pattern-based detection
        if not detect:
            hindi_score = self._pattern_based_detection(text)[1] if detected_lang == "hi" else 0
            english_score = self._pattern_based_detection(text)[1] if detected_lang == "en" else 0
            
            result["hindi_score"] = hindi_score
            result["english_score"] = english_score
        
        return result
    
    def batch_detect(self, texts: List[str]) -> List[Tuple[str, float]]:
        """
        Detect language for multiple texts
        
        Args:
            texts: List of input texts
            
        Returns:
            List of (language_code, confidence) tuples
        """
        results = []
        for text in texts:
            result = self.detect_language(text)
            results.append(result)
        
        return results
    
    def set_confidence_threshold(self, threshold: float):
        """
        Set confidence threshold for language detection
        
        Args:
            threshold: New confidence threshold (0.0 to 1.0)
        """
        self.confidence_threshold = max(0.0, min(1.0, threshold))
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported languages"""
        return ["en", "hi"]
    
    def add_custom_words(self, language: str, words: List[str]):
        """
        Add custom words for better language detection
        
        Args:
            language: Language code ("en" or "hi")
            words: List of words to add
        """
        if language == "hi":
            self.hindi_words.update(words)
        elif language == "en":
            self.english_words.update(words)
        else:
            raise ValueError(f"Unsupported language: {language}")


class LanguageDetectorFactory:
    """Factory for creating language detectors"""
    
    @staticmethod
    def create_detector(confidence_threshold: float = 0.6) -> LanguageDetector:
        """
        Create a language detector instance
        
        Args:
            confidence_threshold: Minimum confidence for detection
            
        Returns:
            LanguageDetector instance
        """
        return LanguageDetector(confidence_threshold)
    
    @staticmethod
    def create_fast_detector() -> LanguageDetector:
        """
        Create a fast language detector with lower confidence threshold
        
        Returns:
            LanguageDetector instance optimized for speed
        """
        return LanguageDetector(confidence_threshold=0.4)
    
    @staticmethod
    def create_accurate_detector() -> LanguageDetector:
        """
        Create an accurate language detector with higher confidence threshold
        
        Returns:
            LanguageDetector instance optimized for accuracy
        """
        return LanguageDetector(confidence_threshold=0.8)
