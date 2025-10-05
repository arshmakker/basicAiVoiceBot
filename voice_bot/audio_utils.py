"""
Audio Utilities Module
Handles audio recording, processing, and playback
"""

import pyaudio
import numpy as np
import threading
import queue
import time
import os
from typing import Optional, List
import logging

# Setup debug logging for audio troubleshooting
DEBUG_LOG = logging.getLogger('audio_debug')
DEBUG_LOG.setLevel(logging.DEBUG)

# Create debug log file
debug_handler = logging.FileHandler('audio_debug.log')
debug_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
debug_handler.setFormatter(debug_formatter)
DEBUG_LOG.addHandler(debug_handler)

def debug_log(message: str, level: str = "INFO"):
    """Enhanced debug logging with terminal info - silent console output"""
    terminal = os.environ.get('TERM_PROGRAM', 'Unknown')
    is_iterm = 'iTerm' in terminal
    full_message = f"[{terminal}|iTerm:{is_iterm}] {message}"
    
    # Only log to file, don't print to console for cleaner interface
    if level == "DEBUG":
        DEBUG_LOG.debug(full_message)
        # Removed console output: print(f"🔊 AUDIO DEBUG: {full_message}")
    elif level == "WARNING":
        DEBUG_LOG.warning(full_message)
        # Removed console output: print(f"🔊 AUDIO WARN: {full_message}")
    elif level == "ERROR":
        DEBUG_LOG.error(full_message)
        # Removed console output: print(f"🔊 AUDIO ERROR: {full_message}")
    else:
        DEBUG_LOG.info(full_message)
        # Removed console output: print(f"🔊 AUDIO INFO: {full_message}")


class AudioRecorder:
    """Handles audio recording from microphone"""
    
    def __init__(self, sample_rate: int = 16000, chunk_size: int = 1024):
        """
        Initialize audio recorder
        
        Args:
            sample_rate: Audio sample rate
            chunk_size: Size of audio chunks
        """
        debug_log("Initializing AudioRecorder", "DEBUG")
        debug_log(f"Sample rate: {sample_rate}, Chunk size: {chunk_size}", "DEBUG")
        
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.format = pyaudio.paFloat32
        self.channels = 1
        
        debug_log("Creating PyAudio instance", "DEBUG")
        self.audio = pyaudio.PyAudio()
        debug_log("PyAudio instance created", "DEBUG")
        
        self.stream = None
        self.is_recording = False
        self.audio_queue = queue.Queue()
        
        # Find default input device
        debug_log("Finding input device", "DEBUG")
        self.input_device = self._find_input_device()
        debug_log(f"Selected input device: {self.input_device}", "DEBUG")
        
    def _find_input_device(self) -> Optional[int]:
        """Find default input device with fallback"""
        debug_log("Starting input device search", "DEBUG")
        try:
            device_count = self.audio.get_device_count()
            debug_log(f"Found {device_count} audio devices", "DEBUG")
            available_devices = []
            
            # First pass: collect all available input devices
            for i in range(device_count):
                device_info = self.audio.get_device_info_by_index(i)
                if device_info['maxInputChannels'] > 0:
                    available_devices.append((i, device_info['name']))
                    debug_log(f"Input device {i}: {device_info['name']}", "DEBUG")
            
            if not available_devices:
                logging.error("No input devices found")
                return None
            
            # Prefer MacBook Air Microphone over iPhone
            for device_id, device_name in available_devices:
                if "MacBook Air Microphone" in device_name:
                    logging.info(f"Using MacBook Air Microphone (Device {device_id})")
                    return device_id
            
            # Fallback to first available device
            device_id, device_name = available_devices[0]
            logging.info(f"Using fallback microphone: {device_name} (Device {device_id})")
            return device_id
            
        except Exception as e:
            logging.warning(f"Error finding input device: {e}")
            return None
    
    def start_recording(self):
        """Start audio recording with device fallback"""
        debug_log("start_recording() called", "DEBUG")
        
        if self.is_recording:
            debug_log("Already recording, skipping start", "DEBUG")
            return
        
        debug_log(f"Starting recording with device {self.input_device}", "DEBUG")
        
        # Try to start recording with current device
        try:
            # Try without callback first (simpler approach)
            debug_log("Opening audio stream", "DEBUG")
            self.stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                input_device_index=self.input_device,
                frames_per_buffer=self.chunk_size
            )
            
            self.is_recording = True
            logging.info("Audio recording started")
            logging.debug(f"Stream opened successfully: {self.stream}")
            
        except Exception as e:
            logging.warning(f"Failed to start recording with device {self.input_device}: {e}")
            
            # Try to find a working device
            self.input_device = self._find_input_device()
            if self.input_device is None:
                logging.error("No working input devices found")
                raise Exception("No working microphone found. Please check your audio devices.")
            
            # Try again with fallback device
            try:
                logging.debug(f"Trying fallback device {self.input_device}")
                self.stream = self.audio.open(
                    format=self.format,
                    channels=self.channels,
                    rate=self.sample_rate,
                    input=True,
                    input_device_index=self.input_device,
                    frames_per_buffer=self.chunk_size
                )
                
                self.is_recording = True
                logging.info(f"Audio recording started with fallback device {self.input_device}")
                logging.debug(f"Fallback stream opened successfully: {self.stream}")
                
            except Exception as e2:
                logging.error(f"Failed to start recording with fallback device: {e2}")
                raise Exception(f"Could not start audio recording. Please check your microphone connection. Error: {e2}")
    
    def stop_recording(self):
        """Stop audio recording"""
        if not self.is_recording:
            return
        
        self.is_recording = False
        
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
        
        logging.info("Audio recording stopped")
    
    def _audio_callback(self, in_data, frame_count, time_info, status):
        """Audio callback for real-time processing"""
        if self.is_recording:
            # Convert bytes to numpy array
            audio_data = np.frombuffer(in_data, dtype=np.float32)
            
            # Debug: Log audio chunk info
            rms = np.sqrt(np.mean(audio_data**2))
            logging.debug(f"Audio chunk received: {len(audio_data)} samples, "
                         f"RMS: {rms:.4f}, Status: {status}")
            
            self.audio_queue.put(audio_data)
        
        return (in_data, pyaudio.paContinue)
    
    def get_audio_chunk(self) -> Optional[np.ndarray]:
        """Get next audio chunk"""
        if not self.is_recording or not self.stream:
            return None
        
        try:
            # Read audio data directly from stream
            data = self.stream.read(self.chunk_size, exception_on_overflow=False)
            audio_data = np.frombuffer(data, dtype=np.float32)
            
            # Debug: Log audio chunk info
            rms = np.sqrt(np.mean(audio_data**2))
            logging.debug(f"Audio chunk received: {len(audio_data)} samples, "
                         f"RMS: {rms:.4f}")
            
            return audio_data
            
        except Exception as e:
            logging.error(f"Error reading audio chunk: {e}")
            return None
    
    def __del__(self):
        """Cleanup"""
        self.stop_recording()
        if hasattr(self, 'audio'):
            self.audio.terminate()


class AudioProcessor:
    """Handles audio processing and analysis"""
    
    def __init__(self, sample_rate: int = 16000):
        """
        Initialize audio processor
        
        Args:
            sample_rate: Audio sample rate
        """
        self.sample_rate = sample_rate
    
    def normalize_audio(self, audio_data: np.ndarray) -> np.ndarray:
        """
        Normalize audio data
        
        Args:
            audio_data: Input audio data
            
        Returns:
            Normalized audio data
        """
        if len(audio_data) == 0:
            return audio_data
        
        # Remove DC offset
        audio_data = audio_data - np.mean(audio_data)
        
        # Normalize to [-1, 1]
        max_val = np.max(np.abs(audio_data))
        if max_val > 0:
            audio_data = audio_data / max_val
        
        return audio_data
    
    def is_speech(self, audio_data: np.ndarray, threshold: float = 0.01) -> bool:
        """
        Detect if audio contains speech
        
        Args:
            audio_data: Audio data to analyze
            threshold: Energy threshold for speech detection
            
        Returns:
            True if speech is detected
        """
        if len(audio_data) == 0:
            return False
        
        # Calculate RMS energy
        rms = np.sqrt(np.mean(audio_data ** 2))
        
        return rms > threshold
    
    def detect_silence(self, audio_data: np.ndarray, threshold: float = 0.01) -> bool:
        """
        Detect silence in audio
        
        Args:
            audio_data: Audio data to analyze
            threshold: Energy threshold for silence detection
            
        Returns:
            True if silence is detected
        """
        return not self.is_speech(audio_data, threshold)
    
    def trim_silence(self, audio_data: np.ndarray, 
                    silence_threshold: float = 0.01,
                    frame_length: int = 1024) -> np.ndarray:
        """
        Trim silence from beginning and end of audio
        
        Args:
            audio_data: Input audio data
            silence_threshold: Threshold for silence detection
            frame_length: Frame length for analysis
            
        Returns:
            Trimmed audio data
        """
        if len(audio_data) == 0:
            return audio_data
        
        # Find start of speech
        start_idx = 0
        for i in range(0, len(audio_data) - frame_length, frame_length):
            frame = audio_data[i:i + frame_length]
            if self.is_speech(frame, silence_threshold):
                start_idx = i
                break
        
        # Find end of speech
        end_idx = len(audio_data)
        for i in range(len(audio_data) - frame_length, 0, -frame_length):
            frame = audio_data[i:i + frame_length]
            if self.is_speech(frame, silence_threshold):
                end_idx = i + frame_length
                break
        
        return audio_data[start_idx:end_idx]
    
    def apply_preemphasis(self, audio_data: np.ndarray, alpha: float = 0.97) -> np.ndarray:
        """
        Apply preemphasis filter
        
        Args:
            audio_data: Input audio data
            alpha: Preemphasis coefficient
            
        Returns:
            Preemphasized audio data
        """
        if len(audio_data) <= 1:
            return audio_data
        
        # Apply preemphasis: y[n] = x[n] - alpha * x[n-1]
        preemphasized = np.zeros_like(audio_data)
        preemphasized[0] = audio_data[0]
        
        for i in range(1, len(audio_data)):
            preemphasized[i] = audio_data[i] - alpha * audio_data[i - 1]
        
        return preemphasized


class AudioPlayer:
    """Handles audio playback"""
    
    def __init__(self, sample_rate: int = 22050):
        """
        Initialize audio player
        
        Args:
            sample_rate: Audio sample rate
        """
        self.sample_rate = sample_rate
        self.format = pyaudio.paFloat32
        self.channels = 1
        
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.is_playing = False
        
        # Find default output device
        self.output_device = self._find_output_device()
    
    def _find_output_device(self) -> Optional[int]:
        """Find default output device"""
        try:
            device_count = self.audio.get_device_count()
            for i in range(device_count):
                device_info = self.audio.get_device_info_by_index(i)
                if device_info['maxOutputChannels'] > 0:
                    return i
            return None
        except Exception as e:
            logging.warning(f"Error finding output device: {e}")
            return None
    
    def play_audio(self, audio_data: np.ndarray, blocking: bool = True):
        """
        Play audio data
        
        Args:
            audio_data: Audio data to play
            blocking: Whether to block until playback is complete
        """
        if len(audio_data) == 0:
            return
        
        try:
            # Ensure audio data is float32
            if audio_data.dtype != np.float32:
                audio_data = audio_data.astype(np.float32)
            
            # Open audio stream
            self.stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.sample_rate,
                output=True,
                output_device_index=self.output_device
            )
            
            self.is_playing = True
            
            # Play audio
            audio_bytes = audio_data.tobytes()
            self.stream.write(audio_bytes)
            
            if blocking:
                # Wait for playback to complete
                time.sleep(len(audio_data) / self.sample_rate)
            
            self.stop_playing()
            
        except Exception as e:
            logging.error(f"Audio playback error: {e}")
            self.stop_playing()
            raise
    
    def stop_playing(self):
        """Stop audio playback"""
        if not self.is_playing:
            return
        
        self.is_playing = False
        
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
    
    def __del__(self):
        """Cleanup"""
        self.stop_playing()
        if hasattr(self, 'audio'):
            self.audio.terminate()


class AudioTranscriber:
    """Audio transcription using Vosk models"""
    
    def __init__(self, models_dir: str = "models"):
        """
        Initialize transcriber
        
        Args:
            models_dir: Directory containing Vosk models
        """
        self.models_dir = models_dir
        self.en_model_path = os.path.join(models_dir, "vosk-model-en-us-0.22")
        self.hi_model_path = os.path.join(models_dir, "vosk-model-hi-0.22")
        
        # Initialize models once to avoid reloading
        self.en_model = None
        self.hi_model = None
        self._models_loaded = False
        
    def _load_models_safely(self):
        """Load Vosk models safely with error handling"""
        if self._models_loaded:
            return True
            
        try:
            import vosk
            
            # Try to load English model
            if os.path.exists(self.en_model_path):
                debug_log("Loading English Vosk model", "DEBUG")
                self.en_model = vosk.Model(self.en_model_path)
                debug_log("English model loaded successfully", "DEBUG")
            
            # Try to load Hindi model
            if os.path.exists(self.hi_model_path):
                debug_log("Loading Hindi Vosk model", "DEBUG")
                self.hi_model = vosk.Model(self.hi_model_path)
                debug_log("Hindi model loaded successfully", "DEBUG")
            
            self._models_loaded = True
            return True
            
        except Exception as e:
            debug_log(f"Failed to load Vosk models: {e}", "ERROR")
            return False
    
    def transcribe_audio(self, audio_data: bytes, sample_rate: int = 16000) -> str:
        """
        Transcribe audio data using pre-loaded models
        
        Args:
            audio_data: Raw audio data
            sample_rate: Audio sample rate
            
        Returns:
            Transcribed text
        """
        try:
            # Load models if not already loaded
            if not self._load_models_safely():
                return "Transcription unavailable - models not loaded"
            
            import vosk
            import json
            import sys
            from io import StringIO
            
            # Suppress Vosk logging output
            old_stderr = sys.stderr
            sys.stderr = StringIO()
            
            transcripts = {}
            
            try:
                # Try English model if available
                if self.en_model:
                    try:
                        debug_log("Trying English model for transcription", "DEBUG")
                        recognizer = vosk.KaldiRecognizer(self.en_model, sample_rate)
                        
                        if recognizer.AcceptWaveform(audio_data):
                            result = json.loads(recognizer.Result())
                            en_transcript = result.get('text', '').strip()
                        else:
                            result = json.loads(recognizer.PartialResult())
                            en_transcript = result.get('partial', '').strip()
                        
                        if en_transcript:
                            transcripts['English'] = en_transcript
                            debug_log(f"English transcription: '{en_transcript}'", "DEBUG")
                            
                    except Exception as e:
                        debug_log(f"English model failed: {e}", "WARNING")
                
                # Try Hindi model if available
                if self.hi_model:
                    try:
                        debug_log("Trying Hindi model for transcription", "DEBUG")
                        recognizer = vosk.KaldiRecognizer(self.hi_model, sample_rate)
                        
                        if recognizer.AcceptWaveform(audio_data):
                            result = json.loads(recognizer.Result())
                            hi_transcript = result.get('text', '').strip()
                        else:
                            result = json.loads(recognizer.PartialResult())
                            hi_transcript = result.get('partial', '').strip()
                        
                        if hi_transcript:
                            transcripts['Hindi'] = hi_transcript
                            debug_log(f"Hindi transcription: '{hi_transcript}'", "DEBUG")
                            
                    except Exception as e:
                        debug_log(f"Hindi model failed: {e}", "WARNING")
                
            finally:
                # Restore stderr
                sys.stderr = old_stderr
            
            # Choose the best result
            if len(transcripts) == 1:
                language, transcript = list(transcripts.items())[0]
                debug_log(f"Using {language} transcription", "DEBUG")
                return transcript
            elif len(transcripts) == 2:
                # Both models worked, choose the longer/more confident one
                en_text = transcripts.get('English', '')
                hi_text = transcripts.get('Hindi', '')
                
                if len(hi_text) > len(en_text):
                    debug_log("Using Hindi transcription (longer)", "DEBUG")
                    return hi_text
                else:
                    debug_log("Using English transcription (longer)", "DEBUG")
                    return en_text
            else:
                debug_log("No speech detected in recording", "WARNING")
                return "No speech detected"
                
        except ImportError:
            debug_log("Vosk not available, cannot transcribe", "WARNING")
            return "Transcription unavailable - Vosk not installed"
        except Exception as e:
            debug_log(f"Transcription error: {e}", "ERROR")
            return f"Transcription error: {str(e)}"
    
    def transcribe_audio_file(self, audio_file_path: str, sample_rate: int = 16000) -> str:
        """
        Transcribe audio from file
        
        Args:
            audio_file_path: Path to audio file
            sample_rate: Audio sample rate
            
        Returns:
            Transcribed text
        """
        try:
            with open(audio_file_path, 'rb') as audio_file:
                audio_data = audio_file.read()
            return self.transcribe_audio(audio_data, sample_rate)
        except Exception as e:
            debug_log(f"Failed to read audio file: {e}", "ERROR")
            return f"Failed to read audio file: {str(e)}"
    
    def cleanup(self):
        """Clean up Vosk models to prevent memory leaks"""
        try:
            if self.en_model:
                del self.en_model
                self.en_model = None
            if self.hi_model:
                del self.hi_model
                self.hi_model = None
            self._models_loaded = False
            debug_log("Vosk models cleaned up", "DEBUG")
        except Exception as e:
            debug_log(f"Error cleaning up models: {e}", "WARNING")
    
    def __del__(self):
        """Destructor to ensure cleanup"""
        self.cleanup()
