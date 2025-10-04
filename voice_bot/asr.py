"""
Speech Recognition Module
Handles speech-to-text conversion using Vosk and Whisper
"""

import os
import json
import pyaudio
import numpy as np
import threading
import time
from pathlib import Path
from typing import Optional, Callable, Dict, Any
import logging

try:
    import vosk
except ImportError:
    vosk = None

try:
    import whisper
except ImportError:
    whisper = None

from .audio_utils import AudioRecorder, AudioProcessor


class SpeechRecognitionError(Exception):
    """Custom exception for speech recognition errors"""
    pass


class VoskRecognizer:
    """Vosk-based speech recognizer"""
    
    def __init__(self, model_path: str, sample_rate: int = 16000):
        """
        Initialize Vosk recognizer
        
        Args:
            model_path: Path to Vosk model directory
            sample_rate: Audio sample rate (default: 16000)
        """
        if vosk is None:
            raise ImportError("Vosk not installed. Install with: pip install vosk")
        
        self.sample_rate = sample_rate
        self.model_path = Path(model_path)
        
        if not self.model_path.exists():
            raise FileNotFoundError(f"Vosk model not found at {model_path}")
        
        # Initialize Vosk model
        try:
            self.model = vosk.Model(str(self.model_path))
            self.recognizer = vosk.KaldiRecognizer(self.model, sample_rate)
            logging.info(f"Vosk model loaded from {model_path}")
        except Exception as e:
            raise SpeechRecognitionError(f"Failed to load Vosk model: {e}")
    
    def recognize_audio(self, audio_data: np.ndarray) -> Optional[str]:
        """
        Recognize speech from audio data
        
        Args:
            audio_data: Audio data as numpy array
            
        Returns:
            Recognized text or None if no speech detected
        """
        try:
            # Convert to bytes
            audio_bytes = (audio_data * 32767).astype(np.int16).tobytes()
            
            # Debug logging
            logging.debug(f"Vosk recognition - Audio length: {len(audio_data)} samples, "
                         f"RMS: {np.sqrt(np.mean(audio_data**2)):.4f}")
            
            # Process audio
            if self.recognizer.AcceptWaveform(audio_bytes):
                result = json.loads(self.recognizer.Result())
                text = result.get('text', '').strip()
                if text:
                    logging.debug(f"Vosk final result: '{text}'")
                return text
            else:
                # Partial result
                partial = json.loads(self.recognizer.PartialResult())
                partial_text = partial.get('partial', '').strip()
                if partial_text:
                    logging.debug(f"Vosk partial result: '{partial_text}'")
                return None
                
        except Exception as e:
            logging.error(f"Vosk recognition error: {e}")
            return None
    
    def reset(self):
        """Reset recognizer state"""
        self.recognizer = vosk.KaldiRecognizer(self.model, self.sample_rate)


class WhisperRecognizer:
    """Whisper-based speech recognizer"""
    
    def __init__(self, model_name: str = "medium"):
        """
        Initialize Whisper recognizer
        
        Args:
            model_name: Whisper model name (tiny, base, small, medium, large)
        """
        if whisper is None:
            raise ImportError("Whisper not installed. Install with: pip install openai-whisper")
        
        self.model_name = model_name
        
        try:
            # Suppress FP16 warnings by setting environment variable
            import warnings
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")
                self.model = whisper.load_model(model_name)
            logging.info(f"Whisper model '{model_name}' loaded")
        except Exception as e:
            raise SpeechRecognitionError(f"Failed to load Whisper model: {e}")
    
    def recognize_audio(self, audio_data: np.ndarray, sample_rate: int = 16000) -> Optional[str]:
        """
        Recognize speech from audio data
        
        Args:
            audio_data: Audio data as numpy array
            sample_rate: Audio sample rate
            
        Returns:
            Recognized text or None if no speech detected
        """
        try:
            # Whisper expects float32 audio
            if audio_data.dtype != np.float32:
                audio_data = audio_data.astype(np.float32)
            
            # Debug logging
            logging.debug(f"Whisper recognition - Audio length: {len(audio_data)} samples, "
                         f"duration: {len(audio_data)/sample_rate:.2f}s, "
                         f"RMS: {np.sqrt(np.mean(audio_data**2)):.4f}")
            
            # Transcribe audio with explicit FP32 setting to avoid warnings
            import warnings
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")
                result = self.model.transcribe(
                    audio_data, 
                    language=None,  # Auto-detect language
                    fp16=False      # Explicitly use FP32 to avoid CPU warnings
                )
            text = result.get('text', '').strip()
            
            if text:
                logging.debug(f"Whisper result: '{text}'")
            else:
                logging.debug("Whisper returned empty result")
            
            return text if text else None
            
        except Exception as e:
            logging.error(f"Whisper recognition error: {e}")
            return None


class SpeechRecognizer:
    """
    Main speech recognition class that supports both Vosk and Whisper
    """
    
    def __init__(self, 
                 vosk_en_model_path: Optional[str] = None,
                 vosk_hi_model_path: Optional[str] = None,
                 preferred_engine: str = "vosk"):
        """
        Initialize speech recognizer
        
        Args:
            vosk_en_model_path: Path to English Vosk model
            vosk_hi_model_path: Path to Hindi Vosk model  
            preferred_engine: Preferred engine (currently only "vosk" supported)
        """
        self.preferred_engine = preferred_engine
        self.recognizers = {}
        
        # Initialize Vosk recognizers if models are provided
        if vosk_en_model_path and Path(vosk_en_model_path).exists():
            try:
                self.recognizers['vosk_en'] = VoskRecognizer(vosk_en_model_path)
                logging.info("English Vosk recognizer initialized")
            except Exception as e:
                logging.warning(f"Failed to initialize English Vosk: {e}")
        
        if vosk_hi_model_path and Path(vosk_hi_model_path).exists():
            try:
                self.recognizers['vosk_hi'] = VoskRecognizer(vosk_hi_model_path)
                logging.info("Hindi Vosk recognizer initialized")
            except Exception as e:
                logging.warning(f"Failed to initialize Hindi Vosk: {e}")
        
        # Note: Whisper support has been removed - using Vosk only
        
        if not self.recognizers:
            raise SpeechRecognitionError("No Vosk models available. Please ensure at least one Vosk model is properly installed.")
    
    def recognize_speech(self, 
                       audio_data: np.ndarray, 
                       language: Optional[str] = None,
                       sample_rate: int = 16000) -> Optional[str]:
        """
        Recognize speech from audio data
        
        Args:
            audio_data: Audio data as numpy array
            language: Expected language ("en" or "hi") for Vosk
            sample_rate: Audio sample rate
            
        Returns:
            Recognized text or None
        """
        logging.debug(f"Speech recognition attempt - Language: {language}, "
                     f"Audio length: {len(audio_data)} samples")
        
        # Try preferred engine first
        if self.preferred_engine == "vosk" and language:
            vosk_key = f"vosk_{language}"
            if vosk_key in self.recognizers:
                logging.debug(f"Trying Vosk {language} recognizer")
                result = self.recognizers[vosk_key].recognize_audio(audio_data)
                if result:
                    logging.info(f"✅ Vosk {language} recognized: '{result}'")
                    return result
                else:
                    logging.debug(f"Vosk {language} returned no result")
        
        # Note: Whisper fallback removed - using Vosk only
        
        # Try other Vosk models
        for key, recognizer in self.recognizers.items():
            if key.startswith('vosk_') and key != f"vosk_{language}":
                logging.debug(f"Trying {key} recognizer")
                result = recognizer.recognize_audio(audio_data)
                if result:
                    logging.info(f"✅ {key} recognized: '{result}'")
                    return result
        
        logging.debug("No speech recognition engine returned a result")
        return None
    
    def reset_vosk(self):
        """Reset all Vosk recognizers"""
        for key, recognizer in self.recognizers.items():
            if key.startswith('vosk_'):
                recognizer.reset()
    
    def get_available_engines(self) -> list:
        """Get list of available recognition engines"""
        return list(self.recognizers.keys())


class ContinuousSpeechRecognizer:
    """
    Continuous speech recognition with real-time audio processing
    """
    
    def __init__(self, 
                 speech_recognizer: SpeechRecognizer,
                 sample_rate: int = 16000,
                 chunk_size: int = 1024,
                 silence_threshold: float = 0.005,  # Lower threshold for better sensitivity
                 silence_duration: float = 0.5):   # Shorter silence duration
        """
        Initialize continuous speech recognizer
        
        Args:
            speech_recognizer: SpeechRecognizer instance
            sample_rate: Audio sample rate
            chunk_size: Audio chunk size
            silence_threshold: Silence detection threshold
            silence_duration: Duration of silence before processing
        """
        self.speech_recognizer = speech_recognizer
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.silence_threshold = silence_threshold
        self.silence_duration = silence_duration
        
        self.audio_recorder = AudioRecorder(sample_rate, chunk_size)
        self.audio_processor = AudioProcessor(sample_rate)
        
        self.is_listening = False
        self.audio_buffer = []
        self.last_speech_time = 0
        
        # Callbacks
        self.on_speech_detected: Optional[Callable[[str], None]] = None
        self.on_silence_detected: Optional[Callable[[], None]] = None
        self.on_error: Optional[Callable[[Exception], None]] = None
    
    def start_listening(self):
        """Start continuous speech recognition"""
        if self.is_listening:
            logging.debug("Already listening, skipping start")
            return
        
        logging.debug("Setting is_listening to True")
        self.is_listening = True
        self.audio_buffer = []
        self.last_speech_time = time.time()
        
        # Start audio recording in separate thread
        logging.debug("Starting recording thread")
        self.recording_thread = threading.Thread(target=self._recording_loop)
        self.recording_thread.daemon = False  # Don't terminate when main thread exits
        self.recording_thread.start()
        
        logging.info("Started continuous speech recognition")
    
    def stop_listening(self):
        """Stop continuous speech recognition"""
        logging.debug("Setting is_listening to False")
        self.is_listening = False
        if hasattr(self, 'recording_thread'):
            logging.debug("Joining recording thread")
            self.recording_thread.join(timeout=1.0)
        
        logging.info("Stopped continuous speech recognition")
    
    def _recording_loop(self):
        """Main recording loop"""
        try:
            logging.debug("Attempting to start audio recording...")
            self.audio_recorder.start_recording()
            logging.debug("Recording loop started")
            
            chunk_count = 0
            while self.is_listening:
                try:
                    # Get audio chunk
                    audio_chunk = self.audio_recorder.get_audio_chunk()
                    if audio_chunk is None:
                        continue
                    
                    chunk_count += 1
                    if chunk_count % 100 == 0:  # Log every 100 chunks
                        logging.debug(f"Received {chunk_count} audio chunks")
                    
                    # Check for speech activity
                    is_speech = self.audio_processor.is_speech(audio_chunk, self.silence_threshold)
                    
                    if is_speech:
                        logging.debug(f"Speech detected in chunk {chunk_count}")
                        self.audio_buffer.extend(audio_chunk)
                        self.last_speech_time = time.time()
                    else:
                        # Check if we've had enough silence
                        silence_duration = time.time() - self.last_speech_time
                        if silence_duration >= self.silence_duration and self.audio_buffer:
                            logging.debug(f"Processing audio buffer after {silence_duration:.2f}s silence")
                            # Process accumulated audio
                            self._process_audio_buffer()
                            self.audio_buffer = []
                            
                except Exception as chunk_error:
                    logging.error(f"Error in recording loop iteration: {chunk_error}")
                    logging.error(f"Chunk error type: {type(chunk_error)}")
                    import traceback
                    logging.error(f"Chunk error traceback: {traceback.format_exc()}")
                    break
                
        except Exception as e:
            logging.error(f"Recording loop error: {e}")
            logging.error(f"Recording loop error type: {type(e)}")
            import traceback
            logging.error(f"Recording loop traceback: {traceback.format_exc()}")
            if self.on_error:
                self.on_error(e)
        finally:
            logging.debug("Stopping audio recording...")
            self.audio_recorder.stop_recording()
            logging.debug("Recording loop ended")
    
    def _process_audio_buffer(self):
        """Process accumulated audio buffer"""
        if not self.audio_buffer:
            return
        
        try:
            # Convert to numpy array
            audio_data = np.array(self.audio_buffer, dtype=np.float32)
            
            # Debug: Log audio statistics
            logging.debug(f"Processing audio buffer: {len(audio_data)} samples, "
                         f"duration: {len(audio_data)/self.sample_rate:.2f}s, "
                         f"RMS: {np.sqrt(np.mean(audio_data**2)):.4f}")
            
            # Normalize audio
            audio_data = self.audio_processor.normalize_audio(audio_data)
            
            # Debug: Log normalized audio stats
            logging.debug(f"Normalized audio - RMS: {np.sqrt(np.mean(audio_data**2)):.4f}, "
                         f"Max: {np.max(np.abs(audio_data)):.4f}")
            
            # Recognize speech
            logging.debug("Attempting speech recognition...")
            text = self.speech_recognizer.recognize_speech(audio_data)
            
            if text:
                logging.info(f"🎤 Speech recognized: '{text}'")
                if self.on_speech_detected:
                    self.on_speech_detected(text)
            else:
                logging.debug("No speech detected in audio buffer")
            
            if self.on_silence_detected:
                self.on_silence_detected()
                
        except Exception as e:
            logging.error(f"Audio processing error: {e}")
            if self.on_error:
                self.on_error(e)
