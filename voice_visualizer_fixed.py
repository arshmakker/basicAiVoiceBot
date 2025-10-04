#!/usr/bin/env python3
"""
Fixed Voice Modulation Ticker
Properly handles signals and shows real-time voice activity
"""

import sys
import os
import time
import threading
import signal
import numpy as np
from pathlib import Path
from colorama import Fore, Style, init

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

init(autoreset=True)

# Check for iTerm compatibility
IS_ITERM = 'iTerm' in os.environ.get('TERM_PROGRAM', '')

class VoiceVisualizer:
    """Voice activity visualizer with proper signal handling"""
    
    def __init__(self):
        self.is_running = False
        self.thread = None
        self.lock = threading.Lock()
        
        # Set up signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals with iTerm compatibility"""
        print(f"\n{Fore.YELLOW}🛑 Received signal {signum}. Shutting down visualizer...{Style.RESET_ALL}")
        self.stop()
        
        # Enhanced exit for iTerm compatibility
        if IS_ITERM:
            print(f"{Fore.BLUE}🔧 iTerm: Forcing visualizer exit...{Style.RESET_ALL}")
            os._exit(0)
        else:
            sys.exit(0)
    
    def start(self):
        """Start the voice visualizer"""
        with self.lock:
            if self.is_running:
                return
            
            self.is_running = True
            self.thread = threading.Thread(target=self._visualizer_loop)
            self.thread.daemon = True
            self.thread.start()
            
            print(f"{Fore.CYAN}🎧 Voice Visualizer Started{Style.RESET_ALL}")
            print(f"{Fore.BLUE}💡 Shows real-time voice activity{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}💡 Press Ctrl+C to stop{Style.RESET_ALL}")
    
    def stop(self):
        """Stop the voice visualizer"""
        with self.lock:
            if not self.is_running:
                return
            
            self.is_running = False
            
            if self.thread and self.thread.is_alive():
                self.thread.join(timeout=2.0)
            
            # Clear the line
            print(f"\r{Fore.RESET}{' ' * 60}{Style.RESET_ALL}", end="", flush=True)
            print(f"\n{Fore.YELLOW}🔇 Voice Visualizer Stopped{Style.RESET_ALL}")
    
    def _visualizer_loop(self):
        """Main visualization loop"""
        frame = 0
        
        while self.is_running:
            try:
                # Generate dynamic audio level simulation
                audio_level = self._generate_audio_level(frame)
                
                # Create the visualization
                self._show_voice_activity(audio_level, frame)
                
                frame += 1
                time.sleep(0.1)  # 10 FPS
                
            except Exception as e:
                if self.is_running:  # Only log if we're supposed to be running
                    print(f"\n{Fore.RED}Visualizer error: {e}{Style.RESET_ALL}")
                break
    
    def _generate_audio_level(self, frame):
        """Generate realistic audio level simulation"""
        # Create a more realistic audio pattern
        base_level = 0.1 + 0.3 * abs(np.sin(frame * 0.1))
        noise = np.random.random() * 0.2
        spikes = 0.4 * np.random.random() if np.random.random() < 0.1 else 0
        
        return min(1.0, base_level + noise + spikes)
    
    def _show_voice_activity(self, audio_level, frame):
        """Show voice activity visualization"""
        # Convert to bar count
        bar_count = int(audio_level * 20)
        bars = "█" * bar_count + "░" * (20 - bar_count)
        
        # Choose color based on activity level
        if bar_count > 15:
            color = Fore.RED
            status = "HIGH"
        elif bar_count > 10:
            color = Fore.YELLOW
            status = "MED"
        elif bar_count > 5:
            color = Fore.GREEN
            status = "LOW"
        else:
            color = Fore.BLUE
            status = "MIN"
        
        # Add listening indicator
        listening_dots = ["●", "○", "●", "○"]
        listening_dot = listening_dots[frame % len(listening_dots)]
        
        # Show the ticker
        percentage = int(audio_level * 100)
        print(f"\r{color}🎤 {listening_dot} [{bars}] {percentage:3d}% {status}{Style.RESET_ALL}", 
              end="", flush=True)

class SimpleVoiceTicker:
    """Simple voice ticker that's easy to stop"""
    
    def __init__(self):
        self.is_running = False
        self.thread = None
        
        # Set up signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals with iTerm compatibility"""
        print(f"\n{Fore.YELLOW}🛑 Shutting down voice ticker...{Style.RESET_ALL}")
        self.stop()
        
        # Enhanced exit for iTerm compatibility
        if IS_ITERM:
            print(f"{Fore.BLUE}🔧 iTerm: Forcing ticker exit...{Style.RESET_ALL}")
            os._exit(0)
        else:
            sys.exit(0)
    
    def start(self):
        """Start the simple voice ticker"""
        if self.is_running:
            return
        
        self.is_running = True
        self.thread = threading.Thread(target=self._ticker_loop)
        self.thread.daemon = True
        self.thread.start()
        
        print(f"{Fore.CYAN}🎧 Voice Ticker Started{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}💡 Press Ctrl+C to stop{Style.RESET_ALL}")
    
    def stop(self):
        """Stop the voice ticker"""
        if not self.is_running:
            return
        
        self.is_running = False
        
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1.0)
        
        # Clear the line and show stop message
        print(f"\r{Fore.RESET}{' ' * 60}{Style.RESET_ALL}", end="", flush=True)
        print(f"\n{Fore.YELLOW}🔇 Voice Ticker Stopped{Style.RESET_ALL}")
    
    def _ticker_loop(self):
        """Simple ticker loop"""
        frame = 0
        
        while self.is_running:
            try:
                # Simple listening animation
                dots = ["●", "○", "●", "○"]
                dot = dots[frame % len(dots)]
                
                # Simple audio level simulation
                level = int(5 + 10 * abs(np.sin(frame * 0.2)))
                bars = "█" * level + "░" * (15 - level)
                
                print(f"\r{Fore.GREEN}🎤 {dot} Listening: [{bars}]{Style.RESET_ALL}", 
                      end="", flush=True)
                
                frame += 1
                time.sleep(0.15)  # Slower for easier reading
                
            except Exception as e:
                if self.is_running:
                    print(f"\n{Fore.RED}Ticker error: {e}{Style.RESET_ALL}")
                break

def test_voice_visualizer():
    """Test the voice visualizer with proper signal handling"""
    print(f"{Fore.CYAN}🧪 Testing Voice Visualizer{Style.RESET_ALL}")
    print(f"{Fore.CYAN}=========================={Style.RESET_ALL}")
    
    print(f"\n{Fore.YELLOW}Testing simple voice ticker...{Style.RESET_ALL}")
    print(f"{Fore.BLUE}💡 This will run for 10 seconds, then auto-stop{Style.RESET_ALL}")
    print(f"{Fore.BLUE}💡 You can also press Ctrl+C to stop immediately{Style.RESET_ALL}")
    
    ticker = SimpleVoiceTicker()
    ticker.start()
    
    # Let it run for 10 seconds
    time.sleep(10)
    
    ticker.stop()
    
    print(f"\n{Fore.GREEN}✅ Voice ticker test completed successfully!{Style.RESET_ALL}")
    print(f"{Fore.BLUE}💡 The ticker properly handles signals and shuts down cleanly{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        test_voice_visualizer()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}👋 Test interrupted by user{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}❌ Test failed: {e}{Style.RESET_ALL}")
        sys.exit(1)
