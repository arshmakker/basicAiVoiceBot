#!/usr/bin/env python3
"""
Progress Bar and Timer for Voice Bot Loading
Shows loading progress with visual indicators and timer
"""

import sys
import time
import threading
from pathlib import Path
from colorama import Fore, Style, init

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

init(autoreset=True)

class LoadingProgress:
    """Progress bar and timer for voice bot loading"""
    
    def __init__(self, total_time=20):
        self.total_time = total_time
        self.start_time = None
        self.is_running = False
        self.current_step = 0
        self.steps = [
            "Initializing components...",
            "Loading English Vosk model...",
            "Loading Hindi Vosk model...",
            "Initializing TTS engine...",
            "Setting up audio pipeline...",
            "Preparing speech recognition...",
            "Configuring voice synthesis...",
            "Finalizing voice bot setup...",
            "Starting continuous recognition...",
            "Voice bot ready!"
        ]
    
    def start(self):
        """Start the progress display"""
        self.start_time = time.time()
        self.is_running = True
        
        print(f"\n{Fore.CYAN}🚀 Voice Bot Loading Progress{Style.RESET_ALL}")
        print(f"{Fore.CYAN}============================{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}⏳ Loading models and components...{Style.RESET_ALL}")
        print(f"{Fore.BLUE}💡 This normally takes 10-20 seconds{Style.RESET_ALL}")
        print(f"{Fore.BLUE}📊 Progress will be shown below:{Style.RESET_ALL}")
        
        # Start timer and progress in separate thread
        self.timer_thread = threading.Thread(target=self._run_timer)
        self.timer_thread.daemon = True
        self.timer_thread.start()
    
    def _run_timer(self):
        """Run the timer and progress display"""
        step_duration = self.total_time / len(self.steps)
        
        for i, step in enumerate(self.steps):
            if not self.is_running:
                break
                
            self.current_step = i
            elapsed = time.time() - self.start_time
            
            # Show progress
            progress = (i + 1) / len(self.steps) * 100
            bar_length = 40
            filled_length = int(bar_length * progress / 100)
            bar = "█" * filled_length + "░" * (bar_length - filled_length)
            
            print(f"\r{Fore.GREEN}[{bar}] {progress:.1f}% - {step}{Style.RESET_ALL}", end="", flush=True)
            
            # Wait for step duration
            time.sleep(step_duration)
        
        if self.is_running:
            print(f"\n{Fore.GREEN}🎉 Voice Bot Loading Complete!{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}🔊 Startup: 'Hey, We ready to rumble! Let us go'{Style.RESET_ALL}")
    
    def stop(self):
        """Stop the progress display"""
        self.is_running = False
        if hasattr(self, 'timer_thread'):
            self.timer_thread.join(timeout=1.0)

def test_progress_bar():
    """Test the progress bar"""
    print(f"{Fore.CYAN}🧪 Testing Progress Bar{Style.RESET_ALL}")
    print(f"{Fore.CYAN}====================={Style.RESET_ALL}")
    
    progress = LoadingProgress(total_time=10)  # 10 seconds for testing
    progress.start()
    
    # Wait for completion
    time.sleep(12)
    progress.stop()
    
    print(f"\n{Fore.GREEN}✅ Progress bar test completed!{Style.RESET_ALL}")

if __name__ == "__main__":
    test_progress_bar()
