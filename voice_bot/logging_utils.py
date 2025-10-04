"""
Logging utilities for single-line output
"""

import sys
import logging
import threading
from typing import Optional

class SingleLineFormatter(logging.Formatter):
    """Custom formatter for single-line logging"""
    
    def format(self, record):
        # Get the formatted message
        msg = super().format(record)
        
        # Add color based on level
        if record.levelno >= logging.ERROR:
            color = '\033[91m'  # Red
        elif record.levelno >= logging.WARNING:
            color = '\033[93m'  # Yellow
        elif record.levelno >= logging.INFO:
            color = '\033[92m'  # Green
        else:
            color = '\033[96m'  # Cyan (DEBUG)
        
        reset = '\033[0m'
        return f"{color}{msg}{reset}"

class SingleLineHandler(logging.Handler):
    """Custom logging handler that updates a single line"""
    
    def __init__(self):
        super().__init__()
        self.lock = threading.Lock()
        self.current_line_length = 0
        
    def emit(self, record):
        try:
            with self.lock:
                msg = self.format(record)
                
                # Clear current line and write new message
                sys.stdout.write('\r' + ' ' * self.current_line_length + '\r')
                sys.stdout.write(msg)
                sys.stdout.flush()
                
                # Update line length (account for ANSI color codes)
                self.current_line_length = len(msg)
                
        except Exception:
            self.handleError(record)
    
    def clear_line(self):
        """Clear the current line"""
        with self.lock:
            sys.stdout.write('\r' + ' ' * self.current_line_length + '\r')
            sys.stdout.flush()
            self.current_line_length = 0

def setup_single_line_logging(level: int = logging.INFO, verbose: bool = False):
    """Setup single-line logging configuration"""
    
    # Remove existing handlers
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Create single-line handler
    handler = SingleLineHandler()
    handler.setFormatter(SingleLineFormatter('%(levelname)s: %(message)s'))
    
    # Set level
    handler.setLevel(logging.DEBUG if verbose else logging.INFO)
    
    # Add handler to root logger
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    
    return handler

def log_and_clear(handler: SingleLineHandler, message: str, level: int = logging.INFO):
    """Log a message and then clear the line"""
    logger = logging.getLogger()
    logger.log(level, message)
    handler.clear_line()



