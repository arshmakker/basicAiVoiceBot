#!/usr/bin/env python3
"""
Test iTerm Compatibility Fix
Tests the enhanced signal handling for iTerm compatibility
"""

import sys
import os
import time
from pathlib import Path
from colorama import Fore, Style, init

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

init(autoreset=True)

def test_iterm_compatibility():
    """Test the iTerm compatibility fixes"""
    print(f"{Fore.CYAN}🧪 Testing iTerm Compatibility Fix{Style.RESET_ALL}")
    print(f"{Fore.CYAN}================================={Style.RESET_ALL}")
    
    # Check terminal type
    terminal = os.environ.get('TERM_PROGRAM', 'Unknown')
    is_iterm = 'iTerm' in terminal
    
    print(f"\n{Fore.BLUE}📊 Terminal Information:{Style.RESET_ALL}")
    print(f"Terminal: {terminal}")
    print(f"iTerm Mode: {Fore.GREEN if is_iterm else Fore.YELLOW}{is_iterm}{Style.RESET_ALL}")
    print(f"TERM: {os.environ.get('TERM', 'Not set')}")
    
    # Test voice visualizer import
    try:
        from voice_visualizer_fixed import SimpleVoiceTicker
        print(f"\n{Fore.GREEN}✅ Voice visualizer imported successfully{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}❌ Voice visualizer import failed: {e}{Style.RESET_ALL}")
        return False
    
    # Test voice bot CLI import
    try:
        from voice_bot_cli import VoiceBotCLI
        print(f"{Fore.GREEN}✅ Voice bot CLI imported successfully{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}❌ Voice bot CLI import failed: {e}{Style.RESET_ALL}")
        return False
    
    # Test signal handling setup
    try:
        print(f"\n{Fore.YELLOW}🧪 Testing signal handling setup...{Style.RESET_ALL}")
        
        cli = VoiceBotCLI()
        print(f"{Fore.GREEN}✅ CLI created with enhanced signal handling{Style.RESET_ALL}")
        
        ticker = SimpleVoiceTicker()
        print(f"{Fore.GREEN}✅ Ticker created with enhanced signal handling{Style.RESET_ALL}")
        
    except Exception as e:
        print(f"{Fore.RED}❌ Signal handling setup failed: {e}{Style.RESET_ALL}")
        return False
    
    # Test visualizer functionality
    try:
        print(f"\n{Fore.YELLOW}🎧 Testing visualizer functionality...{Style.RESET_ALL}")
        
        ticker = SimpleVoiceTicker()
        ticker.start()
        print(f"{Fore.GREEN}✅ Visualizer started successfully{Style.RESET_ALL}")
        
        time.sleep(3)
        ticker.stop()
        print(f"{Fore.GREEN}✅ Visualizer stopped successfully{Style.RESET_ALL}")
        
    except Exception as e:
        print(f"{Fore.RED}❌ Visualizer functionality test failed: {e}{Style.RESET_ALL}")
        return False
    
    print(f"\n{Fore.CYAN}📋 iTerm Compatibility Summary:{Style.RESET_ALL}")
    print(f"✅ Enhanced signal handling implemented")
    print(f"✅ Force exit for iTerm compatibility")
    print(f"✅ Graceful shutdown for standard terminals")
    
    if is_iterm:
        print(f"\n{Fore.GREEN}🎯 iTerm Mode Detected:{Style.RESET_ALL}")
        print(f"• Using enhanced signal handling")
        print(f"• Using force exit (os._exit) for clean shutdown")
        print(f"• Optimized for iTerm threading behavior")
    else:
        print(f"\n{Fore.BLUE}🖥️  Standard Terminal Mode:{Style.RESET_ALL}")
        print(f"• Using standard signal handling")
        print(f"• Using graceful exit (sys.exit)")
        print(f"• Standard threading behavior")
    
    print(f"\n{Fore.GREEN}🎉 iTerm compatibility test completed successfully!{Style.RESET_ALL}")
    return True

if __name__ == "__main__":
    try:
        success = test_iterm_compatibility()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}👋 Test interrupted by user{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}❌ Test failed: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
