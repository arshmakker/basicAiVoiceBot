#!/usr/bin/env python3
"""
Simple Manual Voice Bot
A voice bot with manual start/stop recording control (no admin privileges needed)
"""

import sys
import os
import time
import signal
import threading
from pathlib import Path
from colorama import Fore, Style, init

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

init(autoreset=True)

class SimpleManualVoiceBot:
    """
    Simple Manual Voice Bot with input-based recording control
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
        
        print(f"{Fore.CYAN}🤖 Simple Manual Voice Bot Initialized{Style.RESET_ALL}")
        print(f"Terminal: {self.terminal} (iTerm: {self.is_iterm})")
        print(f"{Fore.YELLOW}💡 Controls: 's' = start, 't' = stop, 'q' = quit, 'h' = help{Style.RESET_ALL}")
    
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
            print(f"\n{Fore.WHITE}🔊 Speaking: '{text}'{Style.RESET_ALL}")
            subprocess.run(["say", text], check=True)
            print(f"{Fore.GREEN}✅ Speech completed{Style.RESET_ALL}")
        except Exception as e:
            print(f"\n{Fore.RED}❌ Speech failed: {e}{Style.RESET_ALL}")
    
    def start(self):
        """Start the simple manual voice bot"""
        if self.is_running:
            print(f"{Fore.YELLOW}⚠️  Voice bot is already running{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.GREEN}🚀 Starting Simple Manual Voice Bot{Style.RESET_ALL}")
        print(f"{Fore.CYAN}===================================={Style.RESET_ALL}")
        
        self.is_running = True
        
        # Startup announcement
        startup_message = "Hey, We ready to rumble! Simple manual recording activated. Press 's' to start recording."
        print(f"{Fore.MAGENTA}🔊 Startup: {startup_message}{Style.RESET_ALL}")
        self.speak(startup_message)
        
        # Start audio monitoring
        try:
            from voice_bot.audio_utils import AudioRecorder
            
            print(f"\n{Fore.YELLOW}🎤 Initializing simple manual audio recording...{Style.RESET_ALL}")
            self.recorder = AudioRecorder(sample_rate=16000, chunk_size=1024)
            
            # Start monitoring in a separate thread
            self.recording_thread = threading.Thread(target=self._monitoring_loop)
            self.recording_thread.daemon = True
            self.recording_thread.start()
            
            print(f"{Fore.GREEN}🎤 Simple manual audio recording ready{Style.RESET_ALL}")
            print(f"{Fore.WHITE}💡 Press 's' to start recording{Style.RESET_ALL}")
            print(f"{Fore.WHITE}💡 Press 't' to stop recording{Style.RESET_ALL}")
            print(f"{Fore.WHITE}💡 Press 'q' to quit{Style.RESET_ALL}")
            print(f"{Fore.WHITE}💡 Press 'h' for help{Style.RESET_ALL}")
            print(f"{Fore.WHITE}💡 Current status: 💤 Waiting for 's' command...{Style.RESET_ALL}")
            
        except Exception as e:
            print(f"\n{Fore.RED}❌ Audio setup failed: {e}{Style.RESET_ALL}")
            self.stop()
    
    def _monitoring_loop(self):
        """Simple manual audio monitoring loop"""
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
            
            print(f"\n{Fore.GREEN}✅ Audio stream opened for simple manual recording{Style.RESET_ALL}")
            
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
            stream.stop_stream()
            stream.close()
            audio.terminate()
            
        except Exception as e:
            print(f"\n{Fore.RED}❌ Monitoring setup failed: {e}{Style.RESET_ALL}")
    
    def start_recording(self):
        """Start recording"""
        if self.is_recording:
            print(f"{Fore.YELLOW}⚠️  Already recording{Style.RESET_ALL}")
            return
        
        self.is_recording = True
        self.recording_data = []
        
        print(f"\n{Fore.GREEN}🔴 RECORDING STARTED{Style.RESET_ALL}")
        print(f"{Fore.WHITE}💡 Press 't' to stop recording{Style.RESET_ALL}")
        
        # Announce recording start
        self.speak("Recording started")
    
    def stop_recording(self):
        """Stop recording and process response"""
        if not self.is_recording:
            print(f"{Fore.YELLOW}⚠️  Not currently recording{Style.RESET_ALL}")
            return
        
        self.is_recording = False
        
        print(f"\n{Fore.YELLOW}⏹️  RECORDING STOPPED{Style.RESET_ALL}")
        
        # Calculate recording duration
        recording_duration = len(self.recording_data) * (1024 / 16000)  # seconds
        
        print(f"{Fore.CYAN}📊 Recording stats:{Style.RESET_ALL}")
        print(f"  • Duration: {recording_duration:.1f} seconds")
        print(f"  • Audio chunks: {len(self.recording_data)}")
        print(f"  • Total size: {len(b''.join(self.recording_data))} bytes")
        
        # Process the recording and generate response
        self._process_recording_and_respond(recording_duration)
        
        # Clear recording data
        self.recording_data = []
        
        print(f"{Fore.GREEN}✅ Recording processing completed{Style.RESET_ALL}")
        print(f"{Fore.WHITE}💡 Press 's' to begin new recording{Style.RESET_ALL}")
        
        # Announce recording stop
        self.speak("Recording stopped")
    
    def _process_recording_and_respond(self, duration):
        """Process the recording and generate a response"""
        try:
            print(f"\n{Fore.CYAN}🔄 Processing recording and generating response...{Style.RESET_ALL}")
            
            # Simulate processing time
            time.sleep(1)
            
            # Generate response based on recording duration
            if duration < 1.0:
                response = "I heard a very short recording. Please speak a bit longer next time."
                print(f"{Fore.YELLOW}⚠️  Short recording detected ({duration:.1f}s){Style.RESET_ALL}")
            elif duration < 3.0:
                response = "I heard your message. That was a nice short recording!"
                print(f"{Fore.GREEN}✅ Short recording processed ({duration:.1f}s){Style.RESET_ALL}")
            elif duration < 10.0:
                response = "I heard your longer message. Thank you for the detailed input!"
                print(f"{Fore.GREEN}✅ Medium recording processed ({duration:.1f}s){Style.RESET_ALL}")
            else:
                response = "I heard your very long message. That was quite detailed!"
                print(f"{Fore.GREEN}✅ Long recording processed ({duration:.1f}s){Style.RESET_ALL}")
            
            # Display the response
            print(f"\n{Fore.MAGENTA}🤖 Bot Response:{Style.RESET_ALL}")
            print(f"{Fore.WHITE}{response}{Style.RESET_ALL}")
            
            # Speak the response
            print(f"\n{Fore.WHITE}🔊 Speaking response...{Style.RESET_ALL}")
            self.speak(response)
            
            # Add some additional feedback
            print(f"\n{Fore.GREEN}✅ Response processing completed{Style.RESET_ALL}")
            
        except Exception as e:
            print(f"\n{Fore.RED}❌ Error processing recording: {e}{Style.RESET_ALL}")
            # Fallback response
            fallback_response = "I heard your recording but had trouble processing it. Please try again."
            print(f"{Fore.WHITE}🤖 Fallback Response: {fallback_response}{Style.RESET_ALL}")
            self.speak(fallback_response)
    
    def stop(self):
        """Stop the simple manual voice bot"""
        if not self.is_running:
            return
        
        print(f"\n{Fore.YELLOW}🛑 Stopping Simple Manual Voice Bot{Style.RESET_ALL}")
        self.is_running = False
        
        # Stop any ongoing recording
        if self.is_recording:
            self.stop_recording()
        
        # Wait for monitoring thread to finish
        if self.recording_thread and self.recording_thread.is_alive():
            self.recording_thread.join(timeout=2)
        
        print(f"{Fore.GREEN}✅ Simple Manual Voice Bot stopped{Style.RESET_ALL}")
    
    def run_interactive(self):
        """Run in interactive mode with text commands"""
        try:
            self.start()
            
            # Interactive command loop
            while self.is_running:
                try:
                    command = input(f"\n{Fore.CYAN}Voice Bot> {Style.RESET_ALL}").strip().lower()
                    
                    if command in ['s', 'start']:
                        self.start_recording()
                    elif command in ['t', 'stop']:
                        self.stop_recording()
                    elif command in ['q', 'quit', 'exit']:
                        print(f"{Fore.YELLOW}👋 Exiting simple manual voice bot...{Style.RESET_ALL}")
                        break
                    elif command in ['status', 'stat']:
                        status = "🔴 RECORDING" if self.is_recording else "💤 IDLE"
                        print(f"{Fore.WHITE}Status: {status}{Style.RESET_ALL}")
                    elif command in ['h', 'help']:
                        print(f"{Fore.CYAN}Commands:{Style.RESET_ALL}")
                        print(f"  {Fore.WHITE}s / start{Style.RESET_ALL} - Begin recording")
                        print(f"  {Fore.WHITE}t / stop{Style.RESET_ALL}  - Stop recording")
                        print(f"  {Fore.WHITE}status{Style.RESET_ALL}    - Show current status")
                        print(f"  {Fore.WHITE}q / quit{Style.RESET_ALL}  - Exit the bot")
                        print(f"  {Fore.WHITE}h / help{Style.RESET_ALL}  - Show this help")
                    elif command == '':
                        continue
                    else:
                        print(f"{Fore.YELLOW}Unknown command: {command}{Style.RESET_ALL}")
                        print(f"{Fore.WHITE}Press 'h' for help{Style.RESET_ALL}")
                        
                except EOFError:
                    # Handle Ctrl+D
                    print(f"\n{Fore.YELLOW}👋 Exiting simple manual voice bot...{Style.RESET_ALL}")
                    break
                except KeyboardInterrupt:
                    print(f"\n{Fore.YELLOW}👋 Keyboard interrupt received{Style.RESET_ALL}")
                    break
                
        except Exception as e:
            print(f"\n{Fore.RED}❌ Error in interactive mode: {e}{Style.RESET_ALL}")
        finally:
            self.stop()

def main():
    """Main function"""
    print(f"{Fore.BLUE}🤖 Simple Manual Voice Bot{Style.RESET_ALL}")
    print(f"{Fore.BLUE}=========================={Style.RESET_ALL}")
    
    print(f"\n{Fore.YELLOW}💡 Features:{Style.RESET_ALL}")
    print(f"  • Text commands: 'start', 'stop', 'quit'")
    print(f"  • No admin privileges required")
    print(f"  • Startup announcements")
    print(f"  • Recording statistics")
    print(f"  • Clean shutdown")
    
    try:
        bot = SimpleManualVoiceBot()
        bot.run_interactive()
        
    except Exception as e:
        print(f"\n{Fore.RED}❌ Simple manual voice bot failed: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
