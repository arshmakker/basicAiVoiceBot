#!/usr/bin/env python3
"""
Minimal Voice Bot
A production-ready minimal voice bot that works without heavy model loading
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

class MinimalVoiceBot:
    """
    A minimal voice bot that provides:
    - Startup announcements
    - Audio recording
    - Clean shutdown
    - iTerm compatibility
    - No heavy model loading
    """
    
    def __init__(self):
        self.is_running = False
        self.recorder = None
        self.recording_thread = None
        self.terminal = os.environ.get('TERM_PROGRAM', 'Unknown')
        self.is_iterm = 'iTerm' in self.terminal
        
        # Setup signal handlers for clean shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        print(f"{Fore.CYAN}🤖 Minimal Voice Bot Initialized{Style.RESET_ALL}")
        print(f"Terminal: {self.terminal} (iTerm: {self.is_iterm})")
    
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
            print(f"{Fore.BLUE}🔊 Speaking: '{text}'{Style.RESET_ALL}")
            subprocess.run(["say", text], check=True)
            print(f"{Fore.GREEN}✅ Speech completed{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}❌ Speech failed: {e}{Style.RESET_ALL}")
    
    def start(self):
        """Start the minimal voice bot"""
        if self.is_running:
            print(f"{Fore.YELLOW}⚠️  Voice bot is already running{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.GREEN}🚀 Starting Minimal Voice Bot{Style.RESET_ALL}")
        print(f"{Fore.CYAN}============================{Style.RESET_ALL}")
        
        self.is_running = True
        
        # Startup announcement
        startup_message = "Hey, We ready to rumble! Let us go"
        print(f"{Fore.MAGENTA}🔊 Startup: {startup_message}{Style.RESET_ALL}")
        self.speak(startup_message)
        
        # Start audio recording
        try:
            from voice_bot.audio_utils import AudioRecorder
            
            print(f"\n{Fore.YELLOW}🎤 Initializing audio recording...{Style.RESET_ALL}")
            self.recorder = AudioRecorder(sample_rate=16000, chunk_size=1024)
            
            # Start recording in a separate thread
            self.recording_thread = threading.Thread(target=self._recording_loop)
            self.recording_thread.daemon = True
            self.recording_thread.start()
            
            print(f"{Fore.GREEN}🎤 Audio recording started{Style.RESET_ALL}")
            print(f"{Fore.CYAN}💡 Speak naturally - audio will be recorded{Style.RESET_ALL}")
            print(f"{Fore.CYAN}💡 Press Ctrl+C to stop{Style.RESET_ALL}")
            
        except Exception as e:
            print(f"{Fore.RED}❌ Audio recording failed: {e}{Style.RESET_ALL}")
            self.stop()
    
    def _recording_loop(self):
        """Audio recording loop"""
        try:
            self.recorder.start_recording()
            
            # Keep recording while running
            while self.is_running:
                time.sleep(0.1)
                
        except Exception as e:
            print(f"{Fore.RED}❌ Recording loop error: {e}{Style.RESET_ALL}")
    
    def stop(self):
        """Stop the minimal voice bot"""
        if not self.is_running:
            return
        
        print(f"\n{Fore.YELLOW}🛑 Stopping Minimal Voice Bot{Style.RESET_ALL}")
        self.is_running = False
        
        # Stop recording
        if self.recorder:
            try:
                self.recorder.stop_recording()
                print(f"{Fore.GREEN}✅ Audio recording stopped{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}❌ Error stopping audio recording: {e}{Style.RESET_ALL}")
        
        # Wait for recording thread to finish
        if self.recording_thread and self.recording_thread.is_alive():
            self.recording_thread.join(timeout=2)
        
        print(f"{Fore.GREEN}✅ Minimal Voice Bot stopped{Style.RESET_ALL}")
    
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
    print(f"{Fore.BLUE}🤖 Minimal Voice Bot{Style.RESET_ALL}")
    print(f"{Fore.BLUE}=================={Style.RESET_ALL}")
    
    print(f"\n{Fore.YELLOW}💡 This is a lightweight voice bot that works reliably{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}💡 Features: Startup announcements, audio recording, clean shutdown{Style.RESET_ALL}")
    
    try:
        bot = MinimalVoiceBot()
        bot.run_interactive()
        
    except Exception as e:
        print(f"\n{Fore.RED}❌ Minimal voice bot failed: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
