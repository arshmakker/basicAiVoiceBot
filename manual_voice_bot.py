#!/usr/bin/env python3
"""
Manual Voice Bot
A voice bot with manual start/stop recording control
"""

import sys
import os
import time
import signal
import threading
import keyboard
from pathlib import Path
from colorama import Fore, Style, init

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

init(autoreset=True)

class ManualVoiceBot:
    """
    Manual Voice Bot with keyboard-controlled recording
    """
    
    def __init__(self):
        self.is_running = False
        self.recorder = None
        self.recording_thread = None
        self.is_recording = False
        self.recording_data = []
        self.terminal = os.environ.get('TERM_PROGRAM', 'Unknown')
        self.is_iterm = 'iTerm' in self.terminal
        
        # Setup signal handlers for clean shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        print(f"{Fore.CYAN}🤖 Manual Voice Bot Initialized{Style.RESET_ALL}")
        print(f"Terminal: {self.terminal} (iTerm: {self.is_iterm})")
        print(f"{Fore.YELLOW}💡 Controls: SPACE = Start/Stop recording, ESC = Exit{Style.RESET_ALL}")
    
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
        """Start the manual voice bot"""
        if self.is_running:
            print(f"{Fore.YELLOW}⚠️  Voice bot is already running{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.GREEN}🚀 Starting Manual Voice Bot{Style.RESET_ALL}")
        print(f"{Fore.CYAN}============================{Style.RESET_ALL}")
        
        self.is_running = True
        
        # Startup announcement
        startup_message = "Hey, We ready to rumble! Manual recording activated. Press Space to start recording."
        print(f"{Fore.MAGENTA}🔊 Startup: {startup_message}{Style.RESET_ALL}")
        self.speak(startup_message)
        
        # Start audio monitoring
        try:
            from voice_bot.audio_utils import AudioRecorder
            
            print(f"\n{Fore.YELLOW}🎤 Initializing manual audio recording...{Style.RESET_ALL}")
            self.recorder = AudioRecorder(sample_rate=16000, chunk_size=1024)
            
            # Start monitoring in a separate thread
            self.recording_thread = threading.Thread(target=self._monitoring_loop)
            self.recording_thread.daemon = True
            self.recording_thread.start()
            
            print(f"{Fore.GREEN}🎤 Manual audio recording ready{Style.RESET_ALL}")
            print(f"{Fore.CYAN}💡 Press SPACE to start/stop recording{Style.RESET_ALL}")
            print(f"{Fore.CYAN}💡 Press ESC to exit{Style.RESET_ALL}")
            print(f"{Fore.CYAN}💡 Current status: 💤 Waiting for SPACE key...{Style.RESET_ALL}")
            
        except Exception as e:
            print(f"\n{Fore.RED}❌ Audio setup failed: {e}{Style.RESET_ALL}")
            self.stop()
    
    def _monitoring_loop(self):
        """Manual audio monitoring loop"""
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
            
            print(f"\n{Fore.GREEN}✅ Audio stream opened for manual recording{Style.RESET_ALL}")
            
            # Setup keyboard listeners
            keyboard.add_hotkey('space', self._toggle_recording)
            keyboard.add_hotkey('esc', self._exit_bot)
            
            while self.is_running:
                try:
                    # Read audio chunk
                    audio_chunk = stream.read(1024, exception_on_overflow=False)
                    
                    # If recording, store the data
                    if self.is_recording:
                        self.recording_data.append(audio_chunk)
                    
                    # Small delay to prevent CPU overload
                    time.sleep(0.01)
                    
                except Exception as e:
                    print(f"\n{Fore.RED}❌ Monitoring loop error: {e}{Style.RESET_ALL}")
                    break
            
            # Cleanup
            keyboard.unhook_all()
            stream.stop_stream()
            stream.close()
            audio.terminate()
            
        except Exception as e:
            print(f"\n{Fore.RED}❌ Monitoring setup failed: {e}{Style.RESET_ALL}")
    
    def _toggle_recording(self):
        """Toggle recording state"""
        if not self.is_running:
            return
        
        if self.is_recording:
            self._stop_recording()
        else:
            self._start_recording()
    
    def _start_recording(self):
        """Start recording"""
        if self.is_recording:
            return
        
        self.is_recording = True
        self.recording_data = []
        
        print(f"\n{Fore.GREEN}🔴 RECORDING STARTED{Style.RESET_ALL}")
        print(f"{Fore.CYAN}💡 Press SPACE again to stop recording{Style.RESET_ALL}")
        
        # Announce recording start
        self.speak("Recording started")
    
    def _stop_recording(self):
        """Stop recording"""
        if not self.is_recording:
            return
        
        self.is_recording = False
        
        print(f"\n{Fore.YELLOW}⏹️  RECORDING STOPPED{Style.RESET_ALL}")
        
        # Calculate recording duration
        recording_duration = len(self.recording_data) * (1024 / 16000)  # seconds
        
        print(f"{Fore.CYAN}📊 Recording stats:{Style.RESET_ALL}")
        print(f"  • Duration: {recording_duration:.1f} seconds")
        print(f"  • Audio chunks: {len(self.recording_data)}")
        print(f"  • Total size: {len(b''.join(self.recording_data))} bytes")
        
        # Clear recording data
        self.recording_data = []
        
        print(f"{Fore.GREEN}✅ Recording processing completed{Style.RESET_ALL}")
        print(f"{Fore.CYAN}💡 Press SPACE to start new recording{Style.RESET_ALL}")
        
        # Announce recording stop
        self.speak("Recording stopped")
    
    def _exit_bot(self):
        """Exit the bot"""
        print(f"\n{Fore.YELLOW}👋 Exiting manual voice bot...{Style.RESET_ALL}")
        self.stop()
    
    def stop(self):
        """Stop the manual voice bot"""
        if not self.is_running:
            return
        
        print(f"\n{Fore.YELLOW}🛑 Stopping Manual Voice Bot{Style.RESET_ALL}")
        self.is_running = False
        
        # Stop any ongoing recording
        if self.is_recording:
            self._stop_recording()
        
        # Wait for monitoring thread to finish
        if self.recording_thread and self.recording_thread.is_alive():
            self.recording_thread.join(timeout=2)
        
        print(f"{Fore.GREEN}✅ Manual Voice Bot stopped{Style.RESET_ALL}")
    
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
    print(f"{Fore.BLUE}🤖 Manual Voice Bot{Style.RESET_ALL}")
    print(f"{Fore.BLUE}=================={Style.RESET_ALL}")
    
    print(f"\n{Fore.YELLOW}💡 Features:{Style.RESET_ALL}")
    print(f"  • Manual start/stop recording with SPACE key")
    print(f"  • ESC key to exit")
    print(f"  • Startup announcements")
    print(f"  • Recording statistics")
    print(f"  • Clean shutdown")
    
    try:
        bot = ManualVoiceBot()
        bot.run_interactive()
        
    except Exception as e:
        print(f"\n{Fore.RED}❌ Manual voice bot failed: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
