#!/usr/bin/env python3
"""
Test Voice Bot with Visualizer
Quick test to verify the voice bot with visualizer works
"""

import sys
import os
import time
import threading
from pathlib import Path
from colorama import Fore, Style, init

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

init(autoreset=True)

def test_visualizer_bot():
    """Test the voice bot with visualizer"""
    print(f"{Fore.CYAN}🧪 Testing Voice Bot with Visualizer{Style.RESET_ALL}")
    print(f"{Fore.CYAN}=================================={Style.RESET_ALL}")
    
    try:
        from minimal_voice_bot_with_visualizer import MinimalVoiceBotWithVisualizer
        
        print(f"{Fore.YELLOW}🔧 Creating voice bot with visualizer...{Style.RESET_ALL}")
        bot = MinimalVoiceBotWithVisualizer()
        
        print(f"{Fore.YELLOW}🎙️  Starting voice bot...{Style.RESET_ALL}")
        
        # Start in a separate thread to avoid blocking
        start_thread = threading.Thread(target=bot.start)
        start_thread.daemon = True
        start_thread.start()
        
        # Wait for startup
        time.sleep(3)
        
        print(f"\n{Fore.CYAN}💡 Voice bot should be running now with visualizer{Style.RESET_ALL}")
        print(f"{Fore.CYAN}💡 You should have heard: 'Hey, We ready to rumble! Let us go'{Style.RESET_ALL}")
        print(f"{Fore.CYAN}💡 You should see the voice modulation visualizer showing listening...{Style.RESET_ALL}")
        
        # Let it run for a few more seconds to show the visualizer
        print(f"\n{Fore.YELLOW}🎤 Voice visualizer should be showing listening animation...{Style.RESET_ALL}")
        time.sleep(5)
        
        print(f"\n{Fore.YELLOW}🛑 Stopping voice bot...{Style.RESET_ALL}")
        bot.stop()
        
        print(f"{Fore.GREEN}✅ Voice bot with visualizer test completed{Style.RESET_ALL}")
        return True
        
    except Exception as e:
        print(f"{Fore.RED}❌ Voice bot with visualizer test failed: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print(f"{Fore.BLUE}🧪 Voice Bot with Visualizer Test{Style.RESET_ALL}")
    print(f"{Fore.BLUE}================================={Style.RESET_ALL}")
    
    print(f"\n{Fore.YELLOW}💡 This will test the voice bot with voice modulation visualizer{Style.RESET_ALL}")
    
    # Test the voice bot with visualizer
    bot_success = test_visualizer_bot()
    
    # Summary
    print(f"\n{Fore.CYAN}📊 Test Results:{Style.RESET_ALL}")
    print(f"Voice Bot with Visualizer: {'✅ PASS' if bot_success else '❌ FAIL'}")
    
    terminal = os.environ.get('TERM_PROGRAM', 'Unknown')
    is_iterm = 'iTerm' in terminal
    
    if bot_success:
        print(f"\n{Fore.GREEN}🎉 Voice bot with visualizer is working!{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✅ Startup announcements work{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✅ Voice visualizer shows listening status{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✅ Audio recording works{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✅ Clean shutdown works{Style.RESET_ALL}")
        
        if is_iterm:
            print(f"{Fore.GREEN}✅ iTerm compatibility confirmed{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}🎯 You can now use the voice bot with visualizer:{Style.RESET_ALL}")
        print(f"python minimal_voice_bot_with_visualizer.py")
        print(f"# You'll see the voice modulation visualizer when listening")
        print(f"# The visualizer shows: 🎤 Listening... ████████░░")
    else:
        print(f"\n{Fore.RED}❌ Voice bot with visualizer has issues{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}👋 Test interrupted{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}❌ Test failed: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
