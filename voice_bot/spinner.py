"""
Spinner Utility Module
Provides visual feedback with animated spinners for different states
"""

import threading
import time
import sys
from typing import Optional
from enum import Enum


class SpinnerState(Enum):
    """Different states for the spinner"""
    INITIALIZING = "initializing"
    LISTENING = "listening"
    PROCESSING = "processing"
    SPEAKING = "speaking"
    WAITING = "waiting"
    ERROR = "error"


class Spinner:
    """Animated spinner with different states and messages"""
    
    def __init__(self):
        self.spinner_chars = {
            SpinnerState.INITIALIZING: "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏",
            SpinnerState.LISTENING: "🎤🎙️🎤🎙️",
            SpinnerState.PROCESSING: "⚡⚡⚡⚡",
            SpinnerState.SPEAKING: "🔊🔉🔊🔉",
            SpinnerState.WAITING: "⏳⏳⏳⏳",
            SpinnerState.ERROR: "❌❌❌❌"
        }
        
        self.messages = {
            SpinnerState.INITIALIZING: "Initializing Voice Bot",
            SpinnerState.LISTENING: "Listening for speech",
            SpinnerState.PROCESSING: "Processing your input",
            SpinnerState.SPEAKING: "Speaking response",
            SpinnerState.WAITING: "Waiting for input",
            SpinnerState.ERROR: "Error occurred"
        }
        
        self.is_running = False
        self.current_state = SpinnerState.WAITING
        self.current_message = ""
        self.spinner_thread = None
        self.lock = threading.Lock()
    
    def start(self, state: SpinnerState, message: Optional[str] = None):
        """Start the spinner with a specific state"""
        with self.lock:
            if self.is_running:
                self.stop()
            
            self.current_state = state
            self.current_message = message or self.messages[state]
            self.is_running = True
            
            self.spinner_thread = threading.Thread(target=self._animate, daemon=True)
            self.spinner_thread.start()
    
    def stop(self):
        """Stop the spinner"""
        with self.lock:
            self.is_running = False
            if self.spinner_thread and self.spinner_thread.is_alive():
                self.spinner_thread.join(timeout=0.1)
    
    def update_state(self, state: SpinnerState, message: Optional[str] = None):
        """Update the spinner state without stopping"""
        with self.lock:
            self.current_state = state
            self.current_message = message or self.messages[state]
    
    def _animate(self):
        """Animation loop"""
        chars = self.spinner_chars[self.current_state]
        char_index = 0
        
        while self.is_running:
            with self.lock:
                if not self.is_running:
                    break
                
                current_char = chars[char_index % len(chars)]
                display_message = f"{current_char} {self.current_message}"
                
                # Clear line and print spinner
                sys.stdout.write(f"\r{display_message}")
                sys.stdout.flush()
                
                char_index += 1
            
            time.sleep(0.1)
    
    def clear(self):
        """Clear the spinner line"""
        sys.stdout.write("\r" + " " * 50 + "\r")
        sys.stdout.flush()


class VoiceBotSpinner:
    """Specialized spinner for Voice Bot with predefined states"""
    
    def __init__(self):
        self.spinner = Spinner()
        self.is_active = False
    
    def start_initializing(self, component: str = ""):
        """Start initialization spinner"""
        message = f"Initializing Voice Bot{f' - {component}' if component else ''}"
        self.spinner.start(SpinnerState.INITIALIZING, message)
        self.is_active = True
    
    def start_listening(self):
        """Start listening spinner"""
        self.spinner.start(SpinnerState.LISTENING)
        self.is_active = True
    
    def start_processing(self, action: str = "input"):
        """Start processing spinner"""
        message = f"Processing {action}"
        self.spinner.start(SpinnerState.PROCESSING, message)
        self.is_active = True
    
    def start_speaking(self):
        """Start speaking spinner"""
        self.spinner.start(SpinnerState.SPEAKING)
        self.is_active = True
    
    def start_waiting(self):
        """Start waiting spinner"""
        self.spinner.start(SpinnerState.WAITING)
        self.is_active = True
    
    def show_error(self, error_message: str):
        """Show error state"""
        self.spinner.start(SpinnerState.ERROR, f"Error: {error_message}")
        self.is_active = True
    
    def stop(self):
        """Stop the spinner"""
        self.spinner.stop()
        self.spinner.clear()
        self.is_active = False
    
    def update_status(self, status: str):
        """Update status message"""
        if self.is_active:
            self.spinner.update_state(SpinnerState.PROCESSING, status)


# Global spinner instance
voice_bot_spinner = VoiceBotSpinner()

