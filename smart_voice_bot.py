#!/usr/bin/env python3
"""
Smart Voice Bot with Voice Activity Detection
A voice bot that automatically starts/stops recording based on voice activity
"""

import sys
import os
import time
import signal
import threading
import numpy as np
from pathlib import Path
from colorama import Fore, Style, init

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

init(autoreset=True)

class VoiceActivityDetector:
    """
    Voice Activity Detector that detects when user is speaking
    """
    
    def __init__(self, sample_rate=16000, chunk_size=1024, silence_threshold=0.01, silence_duration=3.0):
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.silence_threshold = silence_threshold
        self.silence_duration = silence_duration
        
        # State tracking
        self.is_speaking = False
        self.last_speech_time = 0
        self.silence_start_time = 0
        
        # Audio buffer
        self.audio_buffer = []
        
    def process_audio_chunk(self, audio_data):
        """
        Process audio chunk and detect voice activity
        
        Args:
            audio_data: Raw audio data bytes
            
        Returns:
            dict: {
                'is_speaking': bool,
                'silence_duration': float,
                'should_stop_recording': bool
            }
        """
        try:
            # Convert bytes to numpy array
            audio_array = np.frombuffer(audio_data, dtype=np.int16)
            
            # Calculate RMS (Root Mean Square) for volume detection
            rms = np.sqrt(np.mean(audio_array.astype(np.float32) ** 2))
            
            current_time = time.time()
            
            # Voice activity detection
            if rms > self.silence_threshold:
                # Speech detected
                if not self.is_speaking:
                    self.is_speaking = True
                    print(f"\n{Fore.GREEN}🎤 Speech detected! Starting recording...{Style.RESET_ALL}")
                
                self.last_speech_time = current_time
                self.silence_start_time = 0
                
            else:
                # Silence detected
                if self.is_speaking:
                    if self.silence_start_time == 0:
                        self.silence_start_time = current_time
                    
                    silence_duration = current_time - self.silence_start_time
                    
                    if silence_duration >= self.silence_duration:
                        # Stop recording after silence
                        self.is_speaking = False
                        self.silence_start_time = 0
                        print(f"\n{Fore.YELLOW}⏹️  {self.silence_duration:.1f}s of silence detected. Stopping recording...{Style.RESET_ALL}")
                        
                        return {
                            'is_speaking': False,
                            'silence_duration': silence_duration,
                            'should_stop_recording': True,
                            'volume': rms
                        }
                    else:
                        # Still in silence period
                        remaining = self.silence_duration - silence_duration
                        print(f"\r{Fore.YELLOW}⏸️  Silence: {silence_duration:.1f}s (stop in {remaining:.1f}s){Style.RESET_ALL}", end="", flush=True)
            
            return {
                'is_speaking': self.is_speaking,
                'silence_duration': current_time - (self.silence_start_time if self.silence_start_time else self.last_speech_time),
                'should_stop_recording': False,
                'volume': rms
            }
            
        except Exception as e:
            print(f"\n{Fore.RED}❌ Voice activity detection error: {e}{Style.RESET_ALL}")
            return {
                'is_speaking': False,
                'silence_duration': 0,
                'should_stop_recording': False,
                'volume': 0
            }

class SmartVoiceVisualizer:
    """
    Smart voice visualizer that shows different states
    """
    
    def __init__(self):
        self.is_running = False
        self.visualizer_thread = None
        self.current_state = "idle"  # idle, listening, recording, processing
        
    def set_state(self, state):
        """Set the current state"""
        self.current_state = state
    
    def start(self):
        """Start the visualizer"""
        if self.is_running:
            return
        
        self.is_running = True
        self.visualizer_thread = threading.Thread(target=self._visualizer_loop)
        self.visualizer_thread.daemon = True
        self.visualizer_thread.start()
    
    def stop(self):
        """Stop the visualizer"""
        if not self.is_running:
            return
        
        self.is_running = False
        
        if self.visualizer_thread and self.visualizer_thread.is_alive():
            self.visualizer_thread.join(timeout=1)
        
        # Clear the visualizer line
        print(f"\r{Fore.RESET}{' ' * 60}\r", end="", flush=True)
    
    def _visualizer_loop(self):
        """Visualizer animation loop"""
        while self.is_running:
            try:
                if self.current_state == "idle":
                    frames = [
                        "💤 Waiting for speech... ░░░░░░░░░░",
                        "💤 Waiting for speech... █░░░░░░░░░",
                        "💤 Waiting for speech... ██░░░░░░░░",
                        "💤 Waiting for speech... ███░░░░░░░",
                        "💤 Waiting for speech... ████░░░░░░",
                        "💤 Waiting for speech... █████░░░░░",
                        "💤 Waiting for speech... ██████░░░░",
                        "💤 Waiting for speech... ███████░░░",
                        "💤 Waiting for speech... ████████░░",
                        "💤 Waiting for speech... █████████░",
                    ]
                elif self.current_state == "listening":
                    frames = [
                        "🎤 Listening... ░░░░░░░░░░",
                        "🎤 Listening... █░░░░░░░░░",
                        "🎤 Listening... ██░░░░░░░░",
                        "🎤 Listening... ███░░░░░░░",
                        "🎤 Listening... ████░░░░░░",
                        "🎤 Listening... █████░░░░░",
                        "🎤 Listening... ██████░░░░",
                        "🎤 Listening... ███████░░░",
                        "🎤 Listening... ████████░░",
                        "🎤 Listening... █████████░",
                        "🎤 Listening... ██████████",
                    ]
                elif self.current_state == "recording":
                    frames = [
                        "🔴 RECORDING ██████████",
                        "🔴 RECORDING █████████░",
                        "🔴 RECORDING ████████░░",
                        "🔴 RECORDING ███████░░░",
                        "🔴 RECORDING ██████░░░░",
                        "🔴 RECORDING █████░░░░░",
                        "🔴 RECORDING ████░░░░░░",
                        "🔴 RECORDING ███░░░░░░░",
                        "🔴 RECORDING ██░░░░░░░░",
                        "🔴 RECORDING █░░░░░░░░░",
                    ]
                else:
                    frames = ["⏳ Processing..."]
                
                for frame in frames:
                    if not self.is_running:
                        break
                    
                    # Choose color based on state
                    if self.current_state == "idle":
                        color = Fore.BLUE
                    elif self.current_state == "listening":
                        color = Fore.CYAN
                    elif self.current_state == "recording":
                        color = Fore.RED
                    else:
                        color = Fore.YELLOW
                    
                    print(f"\r{color}{frame}{Style.RESET_ALL}", end="", flush=True)
                    time.sleep(0.2)
                
            except Exception:
                break

class SmartVoiceBot:
    """
    Smart Voice Bot with automatic voice activity detection
    """
    
    def __init__(self):
        self.is_running = False
        self.recorder = None
        self.recording_thread = None
        self.visualizer = SmartVoiceVisualizer()
        self.vad = VoiceActivityDetector()
        self.terminal = os.environ.get('TERM_PROGRAM', 'Unknown')
        self.is_iterm = 'iTerm' in self.terminal
        
        # Recording state
        self.is_recording = False
        self.recording_data = []
        
        # Setup signal handlers for clean shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        print(f"{Fore.CYAN}🤖 Smart Voice Bot Initialized{Style.RESET_ALL}")
        print(f"Terminal: {self.terminal} (iTerm: {self.is_iterm})")
        print(f"{Fore.YELLOW}💡 Features: Auto start/stop recording, 3s silence detection{Style.RESET_ALL}")
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print(f"\n{Fore.YELLOW}🛑 Received signal {signum}, shutting down...{Style.RESET_ALL}")
        self.stop()
        
        if self.is_iterm:
            print(f"{Fore.BLUE}🔧 iTerm: Using forced exit{Style.RESET_ALL}")
            os._exit(0)
        else:
            sys.exit(0)
    
    def speak(self, text):
        """Speak text using system TTS"""
        if not text.strip():
            return
        
        try:
            import subprocess
            print(f"\n{Fore.BLUE}🔊 Speaking: '{text}'{Style.RESET_ALL}")
            subprocess.run(["say", text], check=True)
            print(f"{Fore.GREEN}✅ Speech completed{Style.RESET_ALL}")
        except Exception as e:
            print(f"\n{Fore.RED}❌ Speech failed: {e}{Style.RESET_ALL}")
    
    def start(self):
        """Start the smart voice bot"""
        if self.is_running:
            print(f"{Fore.YELLOW}⚠️  Voice bot is already running{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.GREEN}🚀 Starting Smart Voice Bot{Style.RESET_ALL}")
        print(f"{Fore.CYAN}==========================={Style.RESET_ALL}")
        
        self.is_running = True
        
        # Startup announcement
        startup_message = "Hey, We ready to rumble! Smart recording activated"
        print(f"{Fore.MAGENTA}🔊 Startup: {startup_message}{Style.RESET_ALL}")
        self.speak(startup_message)
        
        # Start voice visualizer
        print(f"\n{Fore.YELLOW}🎤 Starting smart visualizer...{Style.RESET_ALL}")
        self.visualizer.start()
        self.visualizer.set_state("idle")
        
        # Start audio monitoring
        try:
            from voice_bot.audio_utils import AudioRecorder
            
            print(f"\n{Fore.YELLOW}🎤 Initializing smart audio monitoring...{Style.RESET_ALL}")
            self.recorder = AudioRecorder(sample_rate=16000, chunk_size=1024)
            
            # Start monitoring in a separate thread
            self.recording_thread = threading.Thread(target=self._monitoring_loop)
            self.recording_thread.daemon = True
            self.recording_thread.start()
            
            print(f"{Fore.GREEN}🎤 Smart audio monitoring started{Style.RESET_ALL}")
            print(f"{Fore.CYAN}💡 Start speaking - recording will begin automatically{Style.RESET_ALL}")
            print(f"{Fore.CYAN}💡 Stop speaking for 3 seconds - recording will stop automatically{Style.RESET_ALL}")
            print(f"{Fore.CYAN}💡 Press Ctrl+C to stop{Style.RESET_ALL}")
            
        except Exception as e:
            print(f"\n{Fore.RED}❌ Audio monitoring failed: {e}{Style.RESET_ALL}")
            self.stop()
    
    def _monitoring_loop(self):
        """Smart audio monitoring loop with VAD"""
        try:
            import pyaudio
            
            # Create a custom audio stream for monitoring
            audio = pyaudio.PyAudio()
            stream = audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                input_device_index=self.recorder.input_device,
                frames_per_buffer=1024
            )
            
            print(f"\n{Fore.GREEN}✅ Audio stream opened for monitoring{Style.RESET_ALL}")
            
            while self.is_running:
                try:
                    # Read audio chunk
                    audio_chunk = stream.read(1024, exception_on_overflow=False)
                    
                    # Process with VAD
                    vad_result = self.vad.process_audio_chunk(audio_chunk)
                    
                    # Update visualizer state
                    if vad_result['is_speaking']:
                        if not self.is_recording:
                            self.visualizer.set_state("recording")
                            self.is_recording = True
                            self.recording_data = []
                            print(f"\n{Fore.GREEN}🔴 Started recording{Style.RESET_ALL}")
                        
                        # Store recording data
                        self.recording_data.append(audio_chunk)
                    else:
                        if self.is_recording:
                            self.visualizer.set_state("listening")
                        else:
                            self.visualizer.set_state("idle")
                    
                    # Check if we should stop recording
                    if vad_result['should_stop_recording'] and self.is_recording:
                        self._stop_recording()
                    
                    # Small delay to prevent CPU overload
                    time.sleep(0.01)
                    
                except Exception as e:
                    print(f"\n{Fore.RED}❌ Monitoring loop error: {e}{Style.RESET_ALL}")
                    break
            
            # Cleanup
            stream.stop_stream()
            stream.close()
            audio.terminate()
            
        except Exception as e:
            print(f"\n{Fore.RED}❌ Monitoring setup failed: {e}{Style.RESET_ALL}")
    
    def _stop_recording(self):
        """Stop recording and process the audio"""
        if not self.is_recording:
            return
        
        self.is_recording = False
        self.visualizer.set_state("processing")
        
        print(f"\n{Fore.YELLOW}⏹️  Recording stopped. Processing audio...{Style.RESET_ALL}")
        
        # Calculate recording duration
        recording_duration = len(self.recording_data) * (1024 / 16000)  # seconds
        
        print(f"{Fore.CYAN}📊 Recording stats:{Style.RESET_ALL}")
        print(f"  • Duration: {recording_duration:.1f} seconds")
        print(f"  • Audio chunks: {len(self.recording_data)}")
        print(f"  • Total size: {len(b''.join(self.recording_data))} bytes")
        
        # Clear recording data
        self.recording_data = []
        
        # Reset visualizer to idle
        self.visualizer.set_state("idle")
        
        print(f"{Fore.GREEN}✅ Audio processing completed{Style.RESET_ALL}")
    
    def stop(self):
        """Stop the smart voice bot"""
        if not self.is_running:
            return
        
        print(f"\n{Fore.YELLOW}🛑 Stopping Smart Voice Bot{Style.RESET_ALL}")
        self.is_running = False
        
        # Stop any ongoing recording
        if self.is_recording:
            self._stop_recording()
        
        # Stop visualizer
        self.visualizer.stop()
        
        # Wait for monitoring thread to finish
        if self.recording_thread and self.recording_thread.is_alive():
            self.recording_thread.join(timeout=2)
        
        print(f"{Fore.GREEN}✅ Smart Voice Bot stopped{Style.RESET_ALL}")
    
    def run_interactive(self):
        """Run in interactive mode"""
        try:
            self.start()
            
            # Keep running until interrupted
            while self.is_running:
                time.sleep(1)
                
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}👋 Keyboard interrupt received{Style.RESET_ALL}")
        except Exception as e:
            print(f"\n{Fore.RED}❌ Error in interactive mode: {e}{Style.RESET_ALL}")
        finally:
            self.stop()

def main():
    """Main function"""
    print(f"{Fore.BLUE}🤖 Smart Voice Bot{Style.RESET_ALL}")
    print(f"{Fore.BLUE}================{Style.RESET_ALL}")
    
    print(f"\n{Fore.YELLOW}💡 Features:{Style.RESET_ALL}")
    print(f"  • Auto start recording when you speak")
    print(f"  • Auto stop recording after 3 seconds of silence")
    print(f"  • Real-time voice activity detection")
    print(f"  • Smart visualizer showing current state")
    print(f"  • Startup announcements")
    print(f"  • Clean shutdown")
    
    try:
        bot = SmartVoiceBot()
        bot.run_interactive()
        
    except Exception as e:
        print(f"\n{Fore.RED}❌ Smart voice bot failed: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
