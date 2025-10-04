#!/usr/bin/env python3
"""
Command Line Interface for Voice Bot
Main entry point for running the voice bot
"""

import sys
import os
import argparse
import logging
import signal
import time
from pathlib import Path
from typing import Optional

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

from voice_bot import VoiceBot, VoiceBotError
from voice_bot.logging_utils import setup_single_line_logging, log_and_clear
from colorama import init, Fore, Style

# Setup debug logging for iTerm troubleshooting
DEBUG_LOG = logging.getLogger('voice_bot_debug')
DEBUG_LOG.setLevel(logging.DEBUG)

# Create debug log file
debug_handler = logging.FileHandler('voice_bot_debug.log')
debug_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
debug_handler.setFormatter(debug_formatter)
DEBUG_LOG.addHandler(debug_handler)

def debug_log(message: str, level: str = "INFO"):
    """Enhanced debug logging with terminal info"""
    terminal = os.environ.get('TERM_PROGRAM', 'Unknown')
    is_iterm = 'iTerm' in terminal
    full_message = f"[{terminal}|iTerm:{is_iterm}] {message}"
    
    if level == "DEBUG":
        DEBUG_LOG.debug(full_message)
        print(f"{Fore.BLUE}🐛 DEBUG: {full_message}{Style.RESET_ALL}")
    elif level == "WARNING":
        DEBUG_LOG.warning(full_message)
        print(f"{Fore.YELLOW}⚠️  WARN: {full_message}{Style.RESET_ALL}")
    elif level == "ERROR":
        DEBUG_LOG.error(full_message)
        print(f"{Fore.RED}❌ ERROR: {full_message}{Style.RESET_ALL}")
    else:
        DEBUG_LOG.info(full_message)
        print(f"{Fore.GREEN}ℹ️  INFO: {full_message}{Style.RESET_ALL}")

# Initialize colorama for cross-platform colored output
init(autoreset=True)

# Check for iTerm compatibility
IS_ITERM = 'iTerm' in os.environ.get('TERM_PROGRAM', '')


class VoiceBotCLI:
    """Command Line Interface for Voice Bot"""
    
    def __init__(self):
        """Initialize CLI"""
        debug_log("Initializing VoiceBotCLI", "DEBUG")
        self.voice_bot: Optional[VoiceBot] = None
        self.running = False
        
        # Set up signal handlers for graceful shutdown
        debug_log("Setting up signal handlers", "DEBUG")
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        debug_log("Signal handlers configured", "DEBUG")
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals with iTerm compatibility"""
        debug_log(f"Signal handler called with signal {signum}", "DEBUG")
        print(f"\n{Fore.YELLOW}Received signal {signum}. Shutting down gracefully...{Style.RESET_ALL}")
        self.stop()
        
        # Enhanced exit for iTerm compatibility
        if IS_ITERM:
            debug_log("Using iTerm-compatible exit (os._exit)", "DEBUG")
            print(f"{Fore.BLUE}🔧 iTerm: Performing enhanced shutdown...{Style.RESET_ALL}")
            # Force exit for iTerm to prevent hanging
            os._exit(0)
        else:
            debug_log("Using standard exit (sys.exit)", "DEBUG")
            sys.exit(0)
    
    def setup_logging(self, verbose: bool = False):
        """Setup logging configuration"""
        self.log_handler = setup_single_line_logging(verbose=verbose)
    
    def print_banner(self):
        """Print welcome banner"""
        banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗
║                    Voice Bot CLI v1.0.0                    ║
║              Multilingual Voice Assistant                  ║
║              Supporting English & Hindi                     ║
╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}

{Fore.GREEN}🎤 Ready to start voice conversation!{Style.RESET_ALL}
{Fore.YELLOW}💡 Tips:{Style.RESET_ALL}
   • Speak naturally in English or Hindi
   • Say 'help' to see what I can do
   • Say 'goodbye' to end the conversation
   • Press Ctrl+C to exit

{Fore.BLUE}🔊 Starting voice bot...{Style.RESET_ALL}
"""
        print(banner)
    
    def print_status(self, status: dict):
        """Print bot status information"""
        print(f"\n{Fore.CYAN}📊 Bot Status:{Style.RESET_ALL}")
        print(f"   Running: {Fore.GREEN if status['is_running'] else Fore.RED}{status['is_running']}{Style.RESET_ALL}")
        print(f"   Listening: {Fore.GREEN if status['is_listening'] else Fore.RED}{status['is_listening']}{Style.RESET_ALL}")
        print(f"   Language: {Fore.BLUE}{status['current_language']}{Style.RESET_ALL}")
        print(f"   ASR Engines: {Fore.BLUE}{', '.join(status['available_engines'])}{Style.RESET_ALL}")
        print(f"   TTS Languages: {Fore.BLUE}{', '.join(status['available_languages'])}{Style.RESET_ALL}")
        print(f"   Supported Intents: {Fore.BLUE}{len(status['supported_intents'])}{Style.RESET_ALL}")
    
    def print_help(self):
        """Print help information"""
        help_text = f"""
{Fore.CYAN}🤖 Voice Bot Commands:{Style.RESET_ALL}

{Fore.GREEN}Voice Commands:{Style.RESET_ALL}
   • "Hello" / "नमस्ते" - Greet the bot
   • "How are you?" / "आप कैसे हैं?" - Small talk
   • "What can you do?" / "आप क्या कर सकते हैं?" - Get help
   • "What is a voice bot?" / "वॉयस बॉट क्या है?" - Learn about voice bots
   • "Goodbye" / "अलविदा" - End conversation

{Fore.GREEN}Keyboard Commands:{Style.RESET_ALL}
   • Ctrl+C - Exit the program
   • 'status' - Show bot status
   • 'history' - Show conversation history
   • 'clear' - Clear conversation history
   • 'help' - Show this help
   • 'quit' - Exit the program

{Fore.GREEN}Supported Languages:{Style.RESET_ALL}
   • English (en)
   • Hindi (hi)

{Fore.GREEN}Features:{Style.RESET_ALL}
   • Automatic language detection
   • Real-time speech recognition
   • Natural language understanding
   • Multilingual text-to-speech
   • Conversation history
"""
        print(help_text)
    
    def initialize_bot(self, args) -> bool:
        """Initialize voice bot with given arguments"""
        debug_log("Initializing voice bot with arguments", "DEBUG")
        debug_log(f"Models dir: {args.models_dir}", "DEBUG")
        debug_log(f"Vosk EN model: {args.vosk_en_model}", "DEBUG")
        debug_log(f"Vosk HI model: {args.vosk_hi_model}", "DEBUG")
        debug_log(f"TTS language: {args.tts_language}", "DEBUG")
        
        try:
            # Check if models directory exists
            models_dir = Path(args.models_dir)
            debug_log(f"Checking models directory: {models_dir}", "DEBUG")
            if not models_dir.exists():
                debug_log(f"Models directory not found: {models_dir}", "ERROR")
                print(f"{Fore.YELLOW}⚠️  Models directory not found: {models_dir}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}   Run: python download_models.py --all{Style.RESET_ALL}")
                return False
            
            # Show loading progress
            print(f"{Fore.BLUE}💡 Loading models - this may take 10-20 seconds{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}⏳ Progress will be shown below:{Style.RESET_ALL}")
            
            # Start progress bar
            from progress_bar import LoadingProgress
            progress = LoadingProgress(total_time=20)
            progress.start()
            
            # Initialize voice bot (this is where the "hanging" happens)
            debug_log("Creating VoiceBot instance", "DEBUG")
            debug_log("This is where model loading happens - may take time", "INFO")
            self.voice_bot = VoiceBot(
                models_dir=args.models_dir,
                vosk_en_model=args.vosk_en_model,
                vosk_hi_model=args.vosk_hi_model,
                tts_language=args.tts_language,
                use_gpu=args.use_gpu,
                sample_rate=args.sample_rate,
                chunk_size=args.chunk_size
            )
            
            # Stop progress bar
            progress.stop()
            
            # Set up callbacks
            self.voice_bot.on_speech_detected = self._on_speech_detected
            self.voice_bot.on_response_generated = self._on_response_generated
            self.voice_bot.on_language_detected = self._on_language_detected
            self.voice_bot.on_error = self._on_error
            
            print(f"\n{Fore.GREEN}✅ Voice Bot initialized successfully!{Style.RESET_ALL}")
            # Clear the logging line
            if hasattr(self, 'log_handler'):
                self.log_handler.clear_line()
            return True
            
        except VoiceBotError as e:
            print(f"{Fore.RED}❌ Failed to initialize Voice Bot: {e}{Style.RESET_ALL}")
            return False
        except Exception as e:
            print(f"{Fore.RED}❌ Unexpected error: {e}{Style.RESET_ALL}")
            return False
    
    def start(self):
        """Start the voice bot"""
        debug_log("Starting voice bot", "DEBUG")
        
        if not self.voice_bot:
            debug_log("Voice bot not initialized", "ERROR")
            print(f"{Fore.RED}❌ Voice Bot not initialized{Style.RESET_ALL}")
            return False
        
        try:
            debug_log("Calling voice_bot.start()", "DEBUG")
            self.voice_bot.start()
            self.running = True
            debug_log("Voice bot started successfully", "INFO")
            print(f"{Fore.GREEN}🎤 Voice Bot is now listening...{Style.RESET_ALL}")
            print(f"{Fore.CYAN}💡 Speak naturally in English or Hindi{Style.RESET_ALL}")
            
            # Startup announcement
            startup_message = "Hey, We ready to rumble! Let us go"
            print(f"{Fore.MAGENTA}🔊 Startup: {startup_message}{Style.RESET_ALL}")
            self.voice_bot.speak(startup_message)
            
            # Clear the logging line
            if hasattr(self, 'log_handler'):
                self.log_handler.clear_line()
            return True
            
        except Exception as e:
            print(f"{Fore.RED}❌ Failed to start Voice Bot: {e}{Style.RESET_ALL}")
            return False
    
    def stop(self):
        """Stop the voice bot"""
        if self.voice_bot and self.running:
            try:
                self.voice_bot.stop()
                self.running = False
                print(f"{Fore.YELLOW}🛑 Voice Bot stopped{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}❌ Error stopping Voice Bot: {e}{Style.RESET_ALL}")
    
    def run_interactive_mode(self):
        """Run interactive command mode"""
        print(f"\n{Fore.CYAN}💬 Interactive Mode - Type commands or press Ctrl+C to exit{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✅ Voice Bot ready for text processing!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}💡 Try: 'text Hello' to test the bot{Style.RESET_ALL}")
        print(f"{Fore.BLUE}💡 Voice visualizer will show when processing{Style.RESET_ALL}")
        
        # Set running to True for interactive mode
        self.running = True
        
        while self.running:
            try:
                command = input(f"\n{Fore.BLUE}voice-bot> {Style.RESET_ALL}").strip().lower()
                
                if not command:
                    continue
                
                if command in ['quit', 'exit', 'q']:
                    break
                elif command == 'help':
                    self.print_help()
                elif command == 'status':
                    if self.voice_bot:
                        status = self.voice_bot.get_status()
                        self.print_status(status)
                elif command == 'history':
                    if self.voice_bot:
                        history = self.voice_bot.get_conversation_history()
                        self._print_history(history)
                elif command == 'clear':
                    if self.voice_bot:
                        self.voice_bot.clear_conversation_history()
                        print(f"{Fore.GREEN}✅ Conversation history cleared{Style.RESET_ALL}")
                elif command.startswith('speak '):
                    text = command[6:]  # Remove 'speak ' prefix
                    if self.voice_bot:
                        print(f"{Fore.MAGENTA}🔊 Speaking: '{text}'{Style.RESET_ALL}")
                        self.voice_bot.speak(text)
                    else:
                        print(f"{Fore.RED}❌ Voice bot not initialized{Style.RESET_ALL}")
                elif command.startswith('text '):
                    text = command[5:]  # Remove 'text ' prefix
                    if self.voice_bot:
                        # Show processing visualizer
                        from voice_visualizer_fixed import SimpleVoiceTicker
                        ticker = SimpleVoiceTicker()
                        ticker.start()
                        
                        try:
                            response = self.voice_bot.process_text(text)
                            print(f"\n{Fore.GREEN}Bot: {response}{Style.RESET_ALL}")
                            self.voice_bot.speak(response)
                        finally:
                            ticker.stop()
                else:
                    print(f"{Fore.YELLOW}Unknown command: {command}{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}Type 'help' for available commands{Style.RESET_ALL}")
                
            except KeyboardInterrupt:
                break
            except EOFError:
                break
            except Exception as e:
                print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")
    
    def run_voice_mode(self):
        """Run voice-only mode with voice visualizer"""
        debug_log("Starting voice mode", "DEBUG")
        print(f"\n{Fore.CYAN}🎤 Voice Mode - Speak naturally or press Ctrl+C to exit{Style.RESET_ALL}")
        
        # Start voice visualizer
        debug_log("Importing SimpleVoiceTicker", "DEBUG")
        from voice_visualizer_fixed import SimpleVoiceTicker
        debug_log("Creating voice ticker", "DEBUG")
        voice_ticker = SimpleVoiceTicker()
        debug_log("Starting voice ticker", "DEBUG")
        voice_ticker.start()
        debug_log("Voice ticker started", "INFO")
        
        try:
            debug_log("Entering voice mode main loop", "DEBUG")
            while self.running:
                time.sleep(0.1)  # Small delay to prevent high CPU usage
        except KeyboardInterrupt:
            debug_log("KeyboardInterrupt received in voice mode", "DEBUG")
            pass
        finally:
            # Stop voice visualizer
            debug_log("Stopping voice ticker", "DEBUG")
            voice_ticker.stop()
            debug_log("Voice ticker stopped", "DEBUG")
    
    def _on_speech_detected(self, text: str):
        """Callback for detected speech"""
        print(f"\n{Fore.GREEN}👤 You: {text}{Style.RESET_ALL}")
    
    def _on_response_generated(self, response: str):
        """Callback for generated response"""
        print(f"{Fore.BLUE}🤖 Bot: {response}{Style.RESET_ALL}")
    
    def _on_language_detected(self, language: str):
        """Callback for language detection"""
        lang_name = "English" if language == "en" else "Hindi"
        print(f"{Fore.MAGENTA}🌐 Language: {lang_name}{Style.RESET_ALL}")
    
    def _on_error(self, error: Exception):
        """Callback for errors"""
        print(f"{Fore.RED}❌ Error: {error}{Style.RESET_ALL}")
    
    def _print_history(self, history: list):
        """Print conversation history"""
        if not history:
            print(f"{Fore.YELLOW}No conversation history{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}📜 Conversation History:{Style.RESET_ALL}")
        for i, exchange in enumerate(history[-10:], 1):  # Show last 10 exchanges
            print(f"\n{Fore.BLUE}{i}. {exchange['timestamp']}{Style.RESET_ALL}")
            print(f"   {Fore.GREEN}👤 You: {exchange['user_input']}{Style.RESET_ALL}")
            print(f"   {Fore.BLUE}🤖 Bot: {exchange['bot_response']}{Style.RESET_ALL}")
            print(f"   {Fore.MAGENTA}🎯 Intent: {exchange['intent']}{Style.RESET_ALL}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Voice Bot - Multilingual Voice Assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python voice_bot_cli.py                    # Run with default settings
  python voice_bot_cli.py --mode interactive  # Run in interactive mode
  python voice_bot_cli.py --models-dir ./models --use-gpu  # Custom settings
  python voice_bot_cli.py --verbose           # Enable verbose logging
        """
    )
    
    # Model configuration
    parser.add_argument('--models-dir', default='models',
                       help='Directory containing model files (default: models)')
    parser.add_argument('--vosk-en-model', 
                       help='Path to English Vosk model')
    parser.add_argument('--vosk-hi-model',
                       help='Path to Hindi Vosk model')
    
    # TTS configuration
    parser.add_argument('--tts-language', default='en',
                       choices=['en', 'hi'],
                       help='Default TTS language (default: en)')
    parser.add_argument('--use-gpu', action='store_true',
                       help='Use GPU acceleration (if available)')
    
    # Audio configuration
    parser.add_argument('--sample-rate', type=int, default=16000,
                       help='Audio sample rate (default: 16000)')
    parser.add_argument('--chunk-size', type=int, default=1024,
                       help='Audio chunk size (default: 1024)')
    
    # Runtime configuration
    parser.add_argument('--mode', default='voice',
                       choices=['voice', 'interactive'],
                       help='Run mode: voice-only or interactive (default: voice)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Create CLI instance
    cli = VoiceBotCLI()
    
    # Setup logging
    cli.setup_logging(args.verbose)
    
    try:
        # Print banner
        cli.print_banner()
        
        # Initialize voice bot
        if not cli.initialize_bot(args):
            sys.exit(1)
        
        # Run in selected mode
        if args.mode == 'interactive':
            # For interactive mode, don't start the voice bot, just run interactive commands
            cli.run_interactive_mode()
        else:
            # For voice mode, start the voice bot first
            if not cli.start():
                sys.exit(1)
            cli.run_voice_mode()
    
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}👋 Goodbye!{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}❌ Fatal error: {e}{Style.RESET_ALL}")
        sys.exit(1)
    finally:
        cli.stop()


if __name__ == "__main__":
    main()
