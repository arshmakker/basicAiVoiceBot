#!/usr/bin/env python3
"""
Test Voice Visualizer Integration
Tests the voice visualizer with the voice bot CLI
"""

import sys
import time
from pathlib import Path
from colorama import Fore, Style, init

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

init(autoreset=True)

def test_voice_visualizer_integration():
    """Test voice visualizer integration with voice bot"""
    print(f"{Fore.CYAN}🧪 Testing Voice Visualizer Integration{Style.RESET_ALL}")
    print(f"{Fore.CYAN}======================================{Style.RESET_ALL}")
    
    try:
        print(f"\n{Fore.YELLOW}⏳ Testing voice visualizer import...{Style.RESET_ALL}")
        
        # Test import
        from voice_visualizer_fixed import SimpleVoiceTicker
        print(f"{Fore.GREEN}✅ Voice visualizer imported successfully{Style.RESET_ALL}")
        
        print(f"\n{Fore.YELLOW}🧪 Testing voice visualizer functionality...{Style.RESET_ALL}")
        
        # Test voice ticker
        ticker = SimpleVoiceTicker()
        print(f"{Fore.GREEN}✅ Voice ticker created successfully{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}🎧 Starting voice ticker for 5 seconds...{Style.RESET_ALL}")
        print(f"{Fore.BLUE}💡 You should see voice activity visualization below{Style.RESET_ALL}")
        
        ticker.start()
        time.sleep(5)
        ticker.stop()
        
        print(f"\n{Fore.GREEN}✅ Voice ticker test completed successfully!{Style.RESET_ALL}")
        
        # Test CLI integration
        print(f"\n{Fore.YELLOW}🧪 Testing CLI integration...{Style.RESET_ALL}")
        
        from voice_bot_cli import VoiceBotCLI
        cli = VoiceBotCLI()
        print(f"{Fore.GREEN}✅ CLI with voice visualizer imported successfully{Style.RESET_ALL}")
        
        print(f"\n{Fore.GREEN}🎉 All voice visualizer integration tests passed!{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}🚀 Ready to test with voice bot!{Style.RESET_ALL}")
        print(f"Commands to try:")
        print(f"1. {Fore.YELLOW}python voice_bot_cli.py --mode interactive{Style.RESET_ALL}")
        print(f"   Then type: {Fore.YELLOW}text Hello{Style.RESET_ALL}")
        print(f"   You'll see voice visualizer during processing")
        
        print(f"\n2. {Fore.YELLOW}python voice_bot_cli.py{Style.RESET_ALL}")
        print(f"   Full voice mode with continuous voice visualizer")
        
        return True
        
    except Exception as e:
        print(f"{Fore.RED}❌ Integration test failed: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_voice_visualizer_integration()
    sys.exit(0 if success else 1)
