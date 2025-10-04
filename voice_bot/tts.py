"""
Text-to-Speech Module
Handles text-to-speech conversion using Coqui TTS
"""

import os
import numpy as np
import threading
import time
from pathlib import Path
from typing import Optional, Dict, Any, List
import logging

try:
    from TTS.api import TTS
    from TTS.utils.manage import ModelManager
except ImportError:
    TTS = None
    ModelManager = None

try:
    import pyttsx3
except ImportError:
    pyttsx3 = None

from .audio_utils import AudioPlayer


class TTSError(Exception):
    """Custom exception for TTS errors"""
    pass


class PyTTSX3TTS:
    """Fallback TTS implementation using pyttsx3"""
    
    def __init__(self, language: str = "en"):
        """
        Initialize pyttsx3 TTS
        
        Args:
            language: Language code (en, hi)
        """
        if pyttsx3 is None:
            raise ImportError("pyttsx3 not installed. Install with: pip install pyttsx3")
        
        self.language = language
        self.engine = None
        self._initialize_engine()
    
    def _initialize_engine(self):
        """Initialize pyttsx3 engine"""
        try:
            self.engine = pyttsx3.init()
            
            # Set properties
            voices = self.engine.getProperty('voices')
            if voices:
                # Try to find a voice that matches the language
                if self.language == "hi":
                    # For Hindi, we'll use the default voice as pyttsx3 has limited Hindi support
                    logging.info("Using default voice for Hindi (limited support)")
                else:
                    # For English, try to find an English voice
                    for voice in voices:
                        if 'english' in voice.name.lower() or 'en' in voice.id.lower():
                            self.engine.setProperty('voice', voice.id)
                            break
            
            # Set speech rate and volume
            self.engine.setProperty('rate', 150)  # Speed of speech
            self.engine.setProperty('volume', 0.9)  # Volume level (0.0 to 1.0)
            
            logging.info("pyttsx3 TTS engine initialized successfully")
            
        except Exception as e:
            logging.error(f"Failed to initialize pyttsx3 engine: {e}")
            raise TTSError(f"Failed to initialize pyttsx3: {e}")
    
    def speak(self, text: str, blocking: bool = True):
        """
        Speak text using pyttsx3
        
        Args:
            text: Text to speak
            blocking: Whether to block until speech is complete
        """
        if not self.engine:
            raise TTSError("pyttsx3 engine not initialized")
        
        if not text.strip():
            return
        
        try:
            self.engine.say(text)
            if blocking:
                self.engine.runAndWait()
            else:
                # For non-blocking, we can't easily implement this with pyttsx3
                # So we'll just run it in a thread
                import threading
                thread = threading.Thread(target=self.engine.runAndWait)
                thread.daemon = True
                thread.start()
                return thread
            
        except Exception as e:
            logging.error(f"pyttsx3 speak error: {e}")
            raise TTSError(f"Failed to speak with pyttsx3: {e}")
    
    def get_available_languages(self) -> List[str]:
        """Get available languages (pyttsx3 has limited language support)"""
        return ["en"]  # pyttsx3 primarily supports English
    
    def set_language(self, language: str):
        """Set language (limited support in pyttsx3)"""
        self.language = language
        logging.info(f"Language set to {language} (limited support in pyttsx3)")


class CoquiTTS:
    """Coqui TTS implementation"""
    
    def __init__(self, 
                 model_name: Optional[str] = None,
                 language: str = "en",
                 use_gpu: bool = False):
        """
        Initialize Coqui TTS
        
        Args:
            model_name: Specific TTS model name
            language: Language code (en, hi)
            use_gpu: Whether to use GPU acceleration
        """
        if TTS is None:
            raise ImportError("Coqui TTS not installed. Install with: pip install TTS")
        
        self.language = language
        self.use_gpu = use_gpu
        self.model_name = model_name
        
        # Available models for different languages
        self.available_models = {
            "en": [
                "tts_models/en/ljspeech/tacotron2-DDC",
                "tts_models/en/ljspeech/fast_pitch",
                "tts_models/en/vctk/vits",
                "tts_models/en/sam/tacotron-DDC"
            ],
            "hi": [
                "tts_models/hi/cv/vits",  # Hindi model
                "tts_models/multilingual/multi-dataset/xtts_v2"  # Multilingual
            ]
        }
        
        self.tts = None
        self.audio_player = AudioPlayer()
        
        # Initialize TTS model
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize TTS model"""
        try:
            if self.model_name:
                # Use specific model
                model_name = self.model_name
            else:
                # Use default model for language
                available = self.available_models.get(self.language, self.available_models["en"])
                model_name = available[0]  # Use first available model
            
            logging.info(f"Loading TTS model: {model_name}")
            
            # Initialize TTS
            self.tts = TTS(model_name, gpu=self.use_gpu)
            
            logging.info(f"TTS model loaded successfully: {model_name}")
            
        except Exception as e:
            logging.error(f"Failed to load TTS model: {e}")
            # Try fallback model
            try:
                fallback_model = "tts_models/en/ljspeech/tacotron2-DDC"
                logging.info(f"Trying fallback model: {fallback_model}")
                self.tts = TTS(fallback_model, gpu=self.use_gpu)
                logging.info("Fallback TTS model loaded successfully")
            except Exception as fallback_error:
                raise TTSError(f"Failed to load any TTS model: {e}, {fallback_error}")
    
    def synthesize(self, text: str, speaker: Optional[str] = None) -> np.ndarray:
        """
        Synthesize speech from text
        
        Args:
            text: Text to synthesize
            speaker: Speaker name (for multi-speaker models)
            
        Returns:
            Audio data as numpy array
        """
        if not self.tts:
            raise TTSError("TTS model not initialized")
        
        if not text.strip():
            return np.array([], dtype=np.float32)
        
        try:
            # Synthesize speech
            if speaker and hasattr(self.tts, 'speakers') and speaker in self.tts.speakers:
                audio_data = self.tts.tts(text, speaker=speaker)
            else:
                audio_data = self.tts.tts(text)
            
            # Convert to numpy array if needed
            if not isinstance(audio_data, np.ndarray):
                audio_data = np.array(audio_data, dtype=np.float32)
            
            return audio_data
            
        except Exception as e:
            logging.error(f"TTS synthesis error: {e}")
            raise TTSError(f"Failed to synthesize speech: {e}")
    
    def synthesize_to_file(self, text: str, output_path: str, speaker: Optional[str] = None):
        """
        Synthesize speech and save to file
        
        Args:
            text: Text to synthesize
            output_path: Output file path
            speaker: Speaker name (for multi-speaker models)
        """
        if not self.tts:
            raise TTSError("TTS model not initialized")
        
        try:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Synthesize and save
            if speaker and hasattr(self.tts, 'speakers') and speaker in self.tts.speakers:
                self.tts.tts_to_file(text, speaker=speaker, file_path=str(output_path))
            else:
                self.tts.tts_to_file(text, file_path=str(output_path))
            
            logging.info(f"Speech saved to: {output_path}")
            
        except Exception as e:
            logging.error(f"TTS file synthesis error: {e}")
            raise TTSError(f"Failed to synthesize speech to file: {e}")
    
    def get_available_speakers(self) -> List[str]:
        """Get list of available speakers"""
        if not self.tts or not hasattr(self.tts, 'speakers'):
            return []
        return list(self.tts.speakers)
    
    def get_available_models(self) -> Dict[str, List[str]]:
        """Get available models for each language"""
        return self.available_models.copy()


class MultilingualTTS:
    """Multilingual TTS manager"""
    
    def __init__(self, use_gpu: bool = False):
        """
        Initialize multilingual TTS
        
        Args:
            use_gpu: Whether to use GPU acceleration
        """
        self.use_gpu = use_gpu
        self.tts_engines = {}
        self.current_language = "en"
        
        # Initialize English TTS by default
        self._initialize_language("en")
    
    def _initialize_language(self, language: str):
        """Initialize TTS for specific language"""
        if language in self.tts_engines:
            return
        
        try:
            if language == "en":
                # Use high-quality English model
                model_name = "tts_models/en/ljspeech/tacotron2-DDC"
            elif language == "hi":
                # Use Hindi model or multilingual model
                model_name = "tts_models/multilingual/multi-dataset/xtts_v2"
            else:
                # Fallback to English
                model_name = "tts_models/en/ljspeech/tacotron2-DDC"
                language = "en"
            
            logging.info(f"Initializing TTS for language: {language}")
            tts = TTS(model_name, gpu=self.use_gpu)
            self.tts_engines[language] = tts
            
            logging.info(f"TTS initialized for {language}")
            
        except Exception as e:
            logging.error(f"Failed to initialize TTS for {language}: {e}")
            # Fallback to English
            if language != "en":
                self._initialize_language("en")
    
    def synthesize(self, text: str, language: str = "en") -> np.ndarray:
        """
        Synthesize speech in specified language
        
        Args:
            text: Text to synthesize
            language: Language code (en, hi)
            
        Returns:
            Audio data as numpy array
        """
        # Initialize language if needed
        if language not in self.tts_engines:
            self._initialize_language(language)
        
        # Use fallback language if requested language failed
        if language not in self.tts_engines:
            language = "en"
        
        try:
            tts = self.tts_engines[language]
            
            # For multilingual models, specify language
            if hasattr(tts, 'language') and language in tts.languages:
                audio_data = tts.tts(text, language=language)
            else:
                audio_data = tts.tts(text)
            
            # Convert to numpy array if needed
            if not isinstance(audio_data, np.ndarray):
                audio_data = np.array(audio_data, dtype=np.float32)
            
            return audio_data
            
        except Exception as e:
            logging.error(f"TTS synthesis error for {language}: {e}")
            raise TTSError(f"Failed to synthesize speech in {language}: {e}")
    
    def get_available_languages(self) -> List[str]:
        """Get list of available languages"""
        return list(self.tts_engines.keys())
    
    def switch_language(self, language: str):
        """Switch to different language"""
        self.current_language = language
        self._initialize_language(language)


class TTSSynthesizer:
    """
    Main TTS synthesizer class that handles text-to-speech conversion
    """
    
    def __init__(self, 
                 language: str = "en",
                 use_gpu: bool = False,
                 multilingual: bool = True):
        """
        Initialize TTS synthesizer
        
        Args:
            language: Default language
            use_gpu: Whether to use GPU acceleration
            multilingual: Whether to use multilingual TTS
        """
        self.language = language
        self.use_gpu = use_gpu
        self.multilingual = multilingual
        
        self.audio_player = AudioPlayer()
        self.tts = None
        
        # Try to initialize TTS with fallback support
        self._initialize_tts()
    
    def _initialize_tts(self):
        """Initialize TTS with fallback support"""
        # Check if Coqui TTS is available first
        if TTS is None:
            logging.info("Coqui TTS not available, using pyttsx3 fallback")
            try:
                self.tts = PyTTSX3TTS(language=self.language)
                logging.info("TTS initialized with pyttsx3 fallback")
                return
            except Exception as pyttsx3_error:
                logging.error(f"pyttsx3 TTS failed: {pyttsx3_error}")
                raise TTSError(f"pyttsx3 TTS failed: {pyttsx3_error}")
        
        try:
            # First try Coqui TTS
            if self.multilingual:
                self.tts = MultilingualTTS(use_gpu=self.use_gpu)
                logging.info("TTS initialized with Coqui MultilingualTTS")
            else:
                self.tts = CoquiTTS(language=self.language, use_gpu=self.use_gpu)
                logging.info("TTS initialized with Coqui TTS")
        except Exception as coqui_error:
            logging.warning(f"Coqui TTS failed: {coqui_error}")
            
            # Fallback to pyttsx3
            try:
                self.tts = PyTTSX3TTS(language=self.language)
                logging.info("TTS initialized with pyttsx3 fallback")
            except Exception as pyttsx3_error:
                logging.error(f"pyttsx3 TTS also failed: {pyttsx3_error}")
                raise TTSError(f"All TTS engines failed: Coqui: {coqui_error}, pyttsx3: {pyttsx3_error}")
    
    def speak(self, text: str, language: Optional[str] = None, blocking: bool = True):
        """
        Convert text to speech and play it
        
        Args:
            text: Text to speak
            language: Language code (if None, uses default)
            blocking: Whether to block until speech is complete
        """
        if not text.strip():
            return
        
        try:
            # Use specified language or default
            target_language = language or self.language
            
            # Check if we're using pyttsx3 fallback
            if isinstance(self.tts, PyTTSX3TTS):
                # pyttsx3 handles both synthesis and playback
                self.tts.speak(text, blocking=blocking)
            else:
                # Coqui TTS - synthesize then play
                audio_data = self.tts.synthesize(text, target_language)
                
                if len(audio_data) > 0:
                    # Play audio
                    self.audio_player.play_audio(audio_data, blocking=blocking)
            
        except Exception as e:
            logging.error(f"TTS speak error: {e}")
            raise TTSError(f"Failed to speak text: {e}")
    
    def speak_async(self, text: str, language: Optional[str] = None):
        """
        Convert text to speech and play it asynchronously
        
        Args:
            text: Text to speak
            language: Language code (if None, uses default)
        """
        def _speak_thread():
            try:
                self.speak(text, language, blocking=True)
            except Exception as e:
                logging.error(f"Async TTS speak error: {e}")
        
        thread = threading.Thread(target=_speak_thread)
        thread.daemon = True
        thread.start()
        return thread
    
    def synthesize_to_file(self, text: str, output_path: str, language: Optional[str] = None):
        """
        Synthesize speech and save to file
        
        Args:
            text: Text to synthesize
            output_path: Output file path
            language: Language code (if None, uses default)
        """
        if not text.strip():
            return
        
        try:
            target_language = language or self.language
            audio_data = self.tts.synthesize(text, target_language)
            
            if len(audio_data) > 0:
                # Save audio data
                output_path = Path(output_path)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Convert to appropriate format and save
                import soundfile as sf
                sf.write(str(output_path), audio_data, 22050)
                
                logging.info(f"Speech saved to: {output_path}")
            
        except Exception as e:
            logging.error(f"TTS file synthesis error: {e}")
            raise TTSError(f"Failed to synthesize speech to file: {e}")
    
    def get_available_languages(self) -> List[str]:
        """Get available languages"""
        if isinstance(self.tts, PyTTSX3TTS):
            return self.tts.get_available_languages()
        elif hasattr(self.tts, 'get_available_languages'):
            return self.tts.get_available_languages()
        return [self.language]
    
    def set_language(self, language: str):
        """Set default language"""
        self.language = language
        if isinstance(self.tts, PyTTSX3TTS):
            self.tts.set_language(language)
        elif hasattr(self.tts, 'switch_language'):
            self.tts.switch_language(language)
