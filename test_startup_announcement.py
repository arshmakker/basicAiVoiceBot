#!/usr/bin/env python3
"""
Test Startup Announcement
Tests the "Hey, We ready to rumble! Let us go" startup message
"""

import sys
import time
from pathlib import Path
from colorama import Fore, Style, init

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from voice_bot import VoiceBot
from voice_bot.logging_utils import setup_single_line_logging

init(autoreset=True)

def test_startup_announcement():
    """Test the startup announcement"""
    print(f"{Fore.CYAN}🎤 Testing Startup Announcement{Style.RESET_ALL}")
    print(f"{Fore.CYAN}=============================={Style.RESET_ALL}")
    
    # Setup minimal logging
    setup_single_line_logging(verbose=False)
    
    try:
        print(f"\n{Fore.YELLOW}⏳ Creating Voice Bot...{Style.RESET_ALL}")
        
        # Create voice bot
        voice_bot = VoiceBot(
            models_dir="models",
            vosk_en_model="vosk-model-en-us-0.22",
            vosk_hi_model="vosk-model-hi-0.22",
            tts_language="en",
            use_gpu=False
        )
        
        print(f"{Fore.GREEN}✅ Voice Bot created successfully!{Style.RESET_ALL}")
        
        print(f"\n{Fore.YELLOW}🎤 Starting Voice Bot (should announce startup message)...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}💡 Listen for: 'Hey, We ready to rumble! Let us go'{Style.RESET_ALL}")
        
        # Start voice bot - this should trigger the startup announcement
        voice_bot.start()
        
        print(f"{Fore.GREEN}✅ Voice Bot started!{Style.RESET_ALL}")
        print(f"{Fore.BLUE}📊 Status:{Style.RESET_ALL}")
        status = voice_bot.get_status()
        print(f"   Running: {status['is_running']}")
        print(f"   Listening: {status['is_listening']}")
        
        # Keep it running for a few seconds
        print(f"\n{Fore.CYAN}Keeping voice bot active for 5 seconds...{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}💡 The bot should have spoken the startup message by now{Style.RESET_ALL}")
        time.sleep(5)
        
        # Stop the voice bot
        print(f"\n{Fore.YELLOW}Stopping voice bot...{Style.RESET_ALL}")
        voice_bot.stop()
        
        print(f"{Fore.GREEN}✅ Voice Bot stopped successfully!{Style.RESET_ALL}")
        print(f"\n{Fore.GREEN}🎉 Startup Announcement Test Completed!{Style.RESET_ALL}")
        print(f"{Fore.BLUE}The voice bot should have spoken: 'Hey, We ready to rumble! Let us go'{Style.RESET_ALL}")
        
        return True
        
    except Exception as e:
        print(f"{Fore.RED}❌ Test failed: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_startup_announcement()
    sys.exit(0 if success else 1)

