"""
Main Voice Bot Class
Orchestrates all components for complete voice interaction
"""

import logging
import threading
import time
from typing import Optional, Callable, Dict, Any
from pathlib import Path

from .asr import SpeechRecognizer, ContinuousSpeechRecognizer
from .tts import TTSSynthesizer
from .language_detection import LanguageDetector
from .dialog_system import DialogManager
from .spinner import voice_bot_spinner


class VoiceBotError(Exception):
    """Custom exception for voice bot errors"""
    pass


class VoiceBot:
    """
    Main Voice Bot class that orchestrates all components
    """
    
    def __init__(self, 
                 models_dir: str = "models",
                 vosk_en_model: Optional[str] = None,
                 vosk_hi_model: Optional[str] = None,
                 tts_language: str = "en",
                 use_gpu: bool = False,
                 sample_rate: int = 16000,
                 chunk_size: int = 1024):
        """
        Initialize Voice Bot
        
        Args:
            models_dir: Directory containing model files
            vosk_en_model: Path to English Vosk model
            vosk_hi_model: Path to Hindi Vosk model
            tts_language: Default TTS language
            use_gpu: Whether to use GPU acceleration
            sample_rate: Audio sample rate
            chunk_size: Audio chunk size
        """
        self.models_dir = Path(models_dir)
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.use_gpu = use_gpu
        
        # Initialize components
        self.speech_recognizer = None
        self.tts_synthesizer = None
        self.language_detector = None
        self.dialog_manager = None
        self.continuous_recognizer = None
        
        # State management
        self.is_running = False
        self.is_listening = False
        self.current_language = tts_language
        
        # Callbacks
        self.on_speech_detected: Optional[Callable[[str], None]] = None
        self.on_response_generated: Optional[Callable[[str], None]] = None
        self.on_error: Optional[Callable[[Exception], None]] = None
        self.on_language_detected: Optional[Callable[[str], None]] = None
        
        # Initialize all components
        self._initialize_components(vosk_en_model, vosk_hi_model, tts_language)
    
    def _initialize_components(self, 
                            vosk_en_model: Optional[str],
                            vosk_hi_model: Optional[str], 
                            tts_language: str):
        """Initialize all voice bot components"""
        try:
            logging.info("Initializing Voice Bot components...")
            # Don't use spinner during initialization - let logging handle it
            
            # Initialize speech recognition
            logging.info("Loading Speech Recognition Models")
            self._initialize_speech_recognition(vosk_en_model, vosk_hi_model)
            
            # Initialize TTS
            logging.info("Loading Text-to-Speech Engine")
            self._initialize_tts(tts_language)
            
            # Initialize language detection
            logging.info("Initializing Language Detection")
            self._initialize_language_detection()
            
            # Initialize dialog system
            logging.info("Loading Dialog System")
            self._initialize_dialog_system()
            
            # Initialize continuous recognition
            logging.info("Setting up Continuous Recognition")
            self._initialize_continuous_recognition()
            
            logging.info("Voice Bot components initialized successfully")
            
        except Exception as e:
            logging.error(f"Failed to initialize Voice Bot: {e}")
            raise VoiceBotError(f"Initialization failed: {e}")
    
    def _initialize_speech_recognition(self, 
                                     vosk_en_model: Optional[str],
                                     vosk_hi_model: Optional[str]):
        """Initialize speech recognition components"""
        try:
            # Set default model paths if not provided
            if not vosk_en_model:
                vosk_en_model = str(self.models_dir / "vosk-model-en-us-0.22")
            else:
                # If relative path provided, make it relative to models_dir
                vosk_en_model = str(self.models_dir / vosk_en_model)
                
            if not vosk_hi_model:
                vosk_hi_model = str(self.models_dir / "vosk-model-hi-0.22")
            else:
                # If relative path provided, make it relative to models_dir
                vosk_hi_model = str(self.models_dir / vosk_hi_model)
            
            # Check if models exist
            if not Path(vosk_en_model).exists():
                logging.warning(f"English Vosk model not found at {vosk_en_model}")
                vosk_en_model = None
            
            if not Path(vosk_hi_model).exists():
                logging.warning(f"Hindi Vosk model not found at {vosk_hi_model}")
                vosk_hi_model = None
            
            # Initialize speech recognizer with Vosk models only
            try:
                self.speech_recognizer = SpeechRecognizer(
                    vosk_en_model_path=vosk_en_model,
                    vosk_hi_model_path=vosk_hi_model,
                    preferred_engine="vosk"
                )
                logging.info("Speech recognition initialized with Vosk")
            except Exception as e:
                logging.error(f"Failed to initialize Vosk speech recognition: {e}")
                raise VoiceBotError(f"Failed to initialize speech recognition: {e}")
            
        except Exception as e:
            logging.error(f"Failed to initialize speech recognition: {e}")
            raise
    
    def _initialize_tts(self, tts_language: str):
        """Initialize TTS components"""
        try:
            # Try to initialize TTS with multilingual support
            try:
                self.tts_synthesizer = TTSSynthesizer(
                    language=tts_language,
                    use_gpu=self.use_gpu,
                    multilingual=True
                )
                logging.info("TTS initialized with multilingual support")
            except Exception as e:
                logging.warning(f"Failed to initialize multilingual TTS, trying single language: {e}")
                # Fallback to single language TTS
                try:
                    self.tts_synthesizer = TTSSynthesizer(
                        language=tts_language,
                        use_gpu=self.use_gpu,
                        multilingual=False
                    )
                    logging.info("TTS initialized with single language support")
                except Exception as fallback_error:
                    logging.error(f"Failed to initialize TTS: {fallback_error}")
                    raise VoiceBotError(f"Failed to initialize TTS: {fallback_error}")
            
        except Exception as e:
            logging.error(f"Failed to initialize TTS: {e}")
            raise
    
    def _initialize_language_detection(self):
        """Initialize language detection"""
        try:
            self.language_detector = LanguageDetector(confidence_threshold=0.6)
            
            logging.info("Language detection initialized")
            
        except Exception as e:
            logging.error(f"Failed to initialize language detection: {e}")
            raise
    
    def _initialize_dialog_system(self):
        """Initialize dialog system"""
        try:
            self.dialog_manager = DialogManager()
            
            logging.info("Dialog system initialized")
            
        except Exception as e:
            logging.error(f"Failed to initialize dialog system: {e}")
            raise
    
    def _initialize_continuous_recognition(self):
        """Initialize continuous speech recognition"""
        try:
            if self.speech_recognizer:
                self.continuous_recognizer = ContinuousSpeechRecognizer(
                    speech_recognizer=self.speech_recognizer,
                    sample_rate=self.sample_rate,
                    chunk_size=self.chunk_size,
                    silence_threshold=0.01,
                    silence_duration=1.0
                )
                
                # Set up callbacks
                self.continuous_recognizer.on_speech_detected = self._handle_speech_detected
                self.continuous_recognizer.on_error = self._handle_recognition_error
                
                logging.info("Continuous recognition initialized")
            
        except Exception as e:
            logging.error(f"Failed to initialize continuous recognition: {e}")
            raise
    
    def start(self):
        """Start the voice bot"""
        if self.is_running:
            logging.warning("Voice bot is already running")
            return
        
        try:
            self.is_running = True
            logging.info("Voice Bot started")
            
            # Start continuous recognition
            if self.continuous_recognizer:
                self.continuous_recognizer.start_listening()
                self.is_listening = True
                voice_bot_spinner.start_listening()
                logging.info("Started listening for speech")
                
                # Startup announcement
                startup_message = "Hey, We ready to rumble! Let us go"
                logging.info(f"Startup announcement: {startup_message}")
                try:
                    self.speak(startup_message, blocking=False)
                except Exception as e:
                    logging.warning(f"Failed to speak startup message: {e}")
            
        except Exception as e:
            self.is_running = False
            logging.error(f"Failed to start voice bot: {e}")
            if self.on_error:
                self.on_error(e)
            raise VoiceBotError(f"Failed to start: {e}")
    
    def stop(self):
        """Stop the voice bot"""
        if not self.is_running:
            logging.warning("Voice bot is not running")
            return
        
        try:
            self.is_running = False
            
            # Stop continuous recognition
            if self.continuous_recognizer and self.is_listening:
                self.continuous_recognizer.stop_listening()
                self.is_listening = False
                voice_bot_spinner.stop()
                logging.info("Stopped listening for speech")
            
            logging.info("Voice Bot stopped")
            
        except Exception as e:
            logging.error(f"Error stopping voice bot: {e}")
            if self.on_error:
                self.on_error(e)
    
    def _handle_speech_detected(self, text: str):
        """Handle detected speech"""
        try:
            logging.info(f"Speech detected: {text}")
            voice_bot_spinner.start_processing("speech input")
            
            # Call user callback
            if self.on_speech_detected:
                self.on_speech_detected(text)
            
            # Detect language with error handling
            try:
                detected_language, confidence = self.language_detector.detect_language(text)
                logging.info(f"Language detected: {detected_language} (confidence: {confidence:.2f})")
                
                # Call language detection callback
                if self.on_language_detected:
                    self.on_language_detected(detected_language)
            except Exception as e:
                logging.warning(f"Language detection failed: {e}, using default language")
                detected_language = self.current_language
            
            # Process input through dialog system with error handling
            try:
                voice_bot_spinner.update_status("Generating response")
                response = self.dialog_manager.process_input(text, detected_language)
                logging.info(f"Generated response: {response}")
            except Exception as e:
                logging.error(f"Dialog processing failed: {e}")
                response = "I'm sorry, I had trouble understanding that. Could you please try again?"
            
            # Speak response with error handling
            try:
                voice_bot_spinner.start_speaking()
                self.speak(response, detected_language)
                voice_bot_spinner.stop()
                voice_bot_spinner.start_listening()  # Resume listening
            except Exception as e:
                logging.error(f"TTS failed: {e}")
                voice_bot_spinner.stop()
                # Try fallback language
                try:
                    fallback_lang = "en" if detected_language == "hi" else "hi"
                    voice_bot_spinner.start_speaking()
                    self.speak(response, fallback_lang)
                    voice_bot_spinner.stop()
                    voice_bot_spinner.start_listening()  # Resume listening
                except Exception as fallback_error:
                    logging.error(f"Fallback TTS also failed: {fallback_error}")
                    voice_bot_spinner.show_error("Speech synthesis failed")
                    time.sleep(2)
                    voice_bot_spinner.stop()
                    voice_bot_spinner.start_listening()  # Resume listening
                    if self.on_error:
                        self.on_error(fallback_error)
            
            # Call response callback
            if self.on_response_generated:
                self.on_response_generated(response)
            
        except Exception as e:
            logging.error(f"Error handling speech: {e}")
            voice_bot_spinner.show_error("Processing failed")
            time.sleep(2)
            voice_bot_spinner.stop()
            voice_bot_spinner.start_listening()  # Resume listening
            if self.on_error:
                self.on_error(e)
    
    def _handle_recognition_error(self, error: Exception):
        """Handle speech recognition errors"""
        logging.error(f"Speech recognition error: {error}")
        if self.on_error:
            self.on_error(error)
    
    def speak(self, text: str, language: Optional[str] = None, blocking: bool = True):
        """
        Speak text using TTS
        
        Args:
            text: Text to speak
            language: Language code (if None, uses detected language)
            blocking: Whether to block until speech is complete
        """
        if not self.tts_synthesizer:
            logging.error("TTS not initialized")
            return
        
        try:
            target_language = language or self.current_language
            self.tts_synthesizer.speak(text, target_language, blocking)
            logging.info(f"Spoke: {text}")
            
        except Exception as e:
            logging.error(f"TTS error: {e}")
            # Fallback to system TTS
            try:
                import subprocess
                subprocess.run(["say", text], check=True)
                logging.info("Fallback TTS (system) succeeded")
            except Exception as e2:
                logging.error(f"Fallback TTS also failed: {e2}")
                if self.on_error:
                    self.on_error(e)
    
    def speak_async(self, text: str, language: Optional[str] = None):
        """
        Speak text asynchronously
        
        Args:
            text: Text to speak
            language: Language code (if None, uses detected language)
        """
        if not self.tts_synthesizer:
            logging.error("TTS not initialized")
            return
        
        try:
            target_language = language or self.current_language
            thread = self.tts_synthesizer.speak_async(text, target_language)
            logging.info(f"Started speaking asynchronously: {text}")
            return thread
            
        except Exception as e:
            logging.error(f"Async TTS error: {e}")
            if self.on_error:
                self.on_error(e)
    
    def process_text(self, text: str, language: Optional[str] = None) -> str:
        """
        Process text input and return response
        
        Args:
            text: Input text
            language: Language code (if None, auto-detect)
            
        Returns:
            Generated response
        """
        try:
            # Detect language if not provided
            if not language:
                language, _ = self.language_detector.detect_language(text)
            
            # Process through dialog system
            response = self.dialog_manager.process_input(text, language)
            
            return response
            
        except Exception as e:
            logging.error(f"Text processing error: {e}")
            if self.on_error:
                self.on_error(e)
            return "I'm sorry, I encountered an error processing your request."
    
    def set_language(self, language: str):
        """
        Set default language
        
        Args:
            language: Language code ("en" or "hi")
        """
        if language not in ["en", "hi"]:
            raise ValueError(f"Unsupported language: {language}")
        
        self.current_language = language
        
        # Update TTS language
        if self.tts_synthesizer:
            self.tts_synthesizer.set_language(language)
        
        logging.info(f"Language set to: {language}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current bot status"""
        return {
            "is_running": self.is_running,
            "is_listening": self.is_listening,
            "current_language": self.current_language,
            "available_engines": self.speech_recognizer.get_available_engines() if self.speech_recognizer else [],
            "available_languages": self.tts_synthesizer.get_available_languages() if self.tts_synthesizer else [],
            "supported_intents": self.dialog_manager.get_supported_intents() if self.dialog_manager else []
        }
    
    def get_conversation_history(self) -> list:
        """Get conversation history"""
        if self.dialog_manager:
            return self.dialog_manager.get_conversation_history()
        return []
    
    def clear_conversation_history(self):
        """Clear conversation history"""
        if self.dialog_manager:
            self.dialog_manager.clear_history()
    
    def reset_speech_recognition(self):
        """Reset speech recognition state"""
        if self.speech_recognizer:
            self.speech_recognizer.reset_vosk()
    
    def __enter__(self):
        """Context manager entry"""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.stop()
    
    def __del__(self):
        """Cleanup on destruction"""
        self.stop()
