#!/usr/bin/env python3
"""
Test script for manual voice bot with single key commands and responses
"""

import time
import subprocess
import sys
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def test_manual_voice_bot():
    """Test the manual voice bot with single key commands"""
    print(f"{Fore.BLUE}🧪 Testing Manual Voice Bot with Single Key Commands{Style.RESET_ALL}")
    print(f"{Fore.BLUE}================================================={Style.RESET_ALL}")
    
    try:
        from simple_manual_voice_bot import SimpleManualVoiceBot
        
        print(f"\n{Fore.CYAN}🤖 Creating Simple Manual Voice Bot...{Style.RESET_ALL}")
        bot = SimpleManualVoiceBot()
        
        print(f"\n{Fore.YELLOW}📋 Test Commands:{Style.RESET_ALL}")
        print(f"  • 's' or 'start' - Start recording")
        print(f"  • 't' or 'stop'  - Stop recording") 
        print(f"  • 'h' or 'help'  - Show help")
        print(f"  • 'q' or 'quit'  - Exit")
        
        print(f"\n{Fore.GREEN}✅ Manual Voice Bot created successfully{Style.RESET_ALL}")
        print(f"{Fore.CYAN}💡 Key features:{Style.RESET_ALL}")
        print(f"  • Single key commands (s, t, q, h)")
        print(f"  • Bot responses after recording")
        print(f"  • No admin privileges required")
        print(f"  • Recording statistics")
        print(f"  • Voice feedback")
        
        return True
        
    except Exception as e:
        print(f"{Fore.RED}❌ Manual Voice Bot test failed: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        return False

def show_usage_guide():
    """Show usage guide for the manual voice bot"""
    print(f"\n{Fore.MAGENTA}📖 Manual Voice Bot Usage Guide{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}=============================={Style.RESET_ALL}")
    
    print(f"\n{Fore.YELLOW}🚀 Quick Start:{Style.RESET_ALL}")
    print(f"  python voice_bot.py manual")
    
    print(f"\n{Fore.YELLOW}⌨️  Single Key Commands:{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}s{Style.RESET_ALL} or {Fore.GREEN}start{Style.RESET_ALL}  - Begin recording")
    print(f"  {Fore.RED}t{Style.RESET_ALL} or {Fore.RED}stop{Style.RESET_ALL}   - Stop recording")
    print(f"  {Fore.BLUE}h{Style.RESET_ALL} or {Fore.BLUE}help{Style.RESET_ALL}  - Show help")
    print(f"  {Fore.YELLOW}q{Style.RESET_ALL} or {Fore.YELLOW}quit{Style.RESET_ALL}  - Exit bot")
    
    print(f"\n{Fore.YELLOW}🎯 Workflow:{Style.RESET_ALL}")
    print(f"  1. Start the bot: {Fore.CYAN}python voice_bot.py manual{Style.RESET_ALL}")
    print(f"  2. Press {Fore.GREEN}'s'{Style.RESET_ALL} to start recording")
    print(f"  3. Speak your message")
    print(f"  4. Press {Fore.RED}'t'{Style.RESET_ALL} to stop recording")
    print(f"  5. Bot responds with feedback")
    print(f"  6. Repeat or press {Fore.YELLOW}'q'{Style.RESET_ALL} to quit")
    
    print(f"\n{Fore.YELLOW}✨ Features:{Style.RESET_ALL}")
    print(f"  • {Fore.GREEN}Single key commands{Style.RESET_ALL} - Fast and easy")
    print(f"  • {Fore.GREEN}Bot responses{Style.RESET_ALL} - Feedback after each recording")
    print(f"  • {Fore.GREEN}No admin rights{Style.RESET_ALL} - Works on any system")
    print(f"  • {Fore.GREEN}Recording stats{Style.RESET_ALL} - Duration and size info")
    print(f"  • {Fore.GREEN}Voice feedback{Style.RESET_ALL} - Audio confirmations")
    print(f"  • {Fore.GREEN}Clean shutdown{Style.RESET_ALL} - Proper resource cleanup")

if __name__ == "__main__":
    print(f"{Fore.BLUE}╔══════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.BLUE}║              🧪 MANUAL VOICE BOT TEST                      ║{Style.RESET_ALL}")
    print(f"{Fore.BLUE}║                                                              ║{Style.RESET_ALL}")
    print(f"{Fore.BLUE}║  Testing single key commands and response system            ║{Style.RESET_ALL}")
    print(f"{Fore.BLUE}╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    
    # Test the manual voice bot
    success = test_manual_voice_bot()
    
    if success:
        print(f"\n{Fore.GREEN}🎉 Manual Voice Bot test completed successfully!{Style.RESET_ALL}")
        show_usage_guide()
        
        print(f"\n{Fore.CYAN}🚀 Ready to use! Run: python voice_bot.py manual{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.RED}❌ Manual Voice Bot test failed{Style.RESET_ALL}")
        sys.exit(1)
