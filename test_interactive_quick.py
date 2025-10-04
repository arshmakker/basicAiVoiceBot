#!/usr/bin/env python3
"""
Quick Interactive Test
Tests the interactive mode quickly
"""

import sys
import time
from pathlib import Path
from colorama import Fore, Style, init

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from voice_bot_cli import VoiceBotCLI
from voice_bot.logging_utils import setup_single_line_logging

init(autoreset=True)

def test_interactive_mode():
    """Test interactive mode quickly"""
    print(f"{Fore.CYAN}🧪 Testing Interactive Mode{Style.RESET_ALL}")
    print(f"{Fore.CYAN}==========================={Style.RESET_ALL}")
    
    # Setup minimal logging
    setup_single_line_logging(verbose=False)
    
    try:
        print(f"\n{Fore.YELLOW}⏳ Creating CLI instance...{Style.RESET_ALL}")
        
        # Create CLI
        cli = VoiceBotCLI()
        cli.setup_logging(verbose=False)
        
        print(f"{Fore.YELLOW}⏳ Initializing voice bot...{Style.RESET_ALL}")
        
        # Create a simple args object
        class Args:
            models_dir = "models"
            vosk_en_model = "vosk-model-en-us-0.22"
            vosk_hi_model = "vosk-model-hi-0.22"
            tts_language = "en"
            use_gpu = False
            verbose = False
            sample_rate = 16000
            chunk_size = 1024
        
        args = Args()
        
        # Initialize bot
        if not cli.initialize_bot(args):
            print(f"{Fore.RED}❌ Failed to initialize bot{Style.RESET_ALL}")
            return False
        
        print(f"{Fore.GREEN}✅ Voice bot initialized successfully!{Style.RESET_ALL}")
        
        # Test interactive commands
        print(f"\n{Fore.YELLOW}🧪 Testing interactive commands...{Style.RESET_ALL}")
        
        # Test text processing
        print(f"{Fore.CYAN}Testing 'text Hello' command...{Style.RESET_ALL}")
        response = cli.voice_bot.process_text("Hello")
        print(f"{Fore.GREEN}Response: '{response}'{Style.RESET_ALL}")
        
        # Test status
        print(f"\n{Fore.CYAN}Testing 'status' command...{Style.RESET_ALL}")
        status = cli.voice_bot.get_status()
        print(f"{Fore.BLUE}Status: {status['available_engines']} engines, {len(status['supported_intents'])} intents{Style.RESET_ALL}")
        
        # Test history
        print(f"\n{Fore.CYAN}Testing conversation history...{Style.RESET_ALL}")
        history = cli.voice_bot.get_conversation_history()
        print(f"{Fore.BLUE}History entries: {len(history)}{Style.RESET_ALL}")
        
        print(f"\n{Fore.GREEN}✅ Interactive mode test completed successfully!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}💡 The interactive mode should now work without hanging{Style.RESET_ALL}")
        
        return True
        
    except Exception as e:
        print(f"{Fore.RED}❌ Test failed: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_interactive_mode()
    sys.exit(0 if success else 1)
