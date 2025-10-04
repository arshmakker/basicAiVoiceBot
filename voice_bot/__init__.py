"""
Voice Bot Package
A complete voice bot implementation supporting English and Hindi
"""

__version__ = "1.0.0"
__author__ = "Voice Bot Team"
__description__ = "A multilingual voice bot with ASR, TTS, and dialog management"

from .asr import SpeechRecognizer, ContinuousSpeechRecognizer, SpeechRecognitionError
from .tts import TTSSynthesizer, TTSError
from .language_detection import LanguageDetector, LanguageDetectionError
from .dialog_system import DialogManager, DialogSystemError
from .voice_bot import VoiceBot, VoiceBotError

__all__ = [
    'VoiceBot',
    'VoiceBotError',
    'SpeechRecognizer',
    'ContinuousSpeechRecognizer', 
    'SpeechRecognitionError',
    'TTSSynthesizer',
    'TTSError',
    'LanguageDetector',
    'LanguageDetectionError',
    'DialogManager',
    'DialogSystemError'
]
