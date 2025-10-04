#!/usr/bin/env python3
"""
Voice Input Debug Test
Comprehensive debugging for voice input issues in iTerm
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

def test_environment():
    """Test environment and terminal detection"""
    print(f"{Fore.CYAN}🔍 Environment and Terminal Detection{Style.RESET_ALL}")
    print(f"{Fore.CYAN}===================================={Style.RESET_ALL}")
    
    terminal = os.environ.get('TERM_PROGRAM', 'Unknown')
    is_iterm = 'iTerm' in terminal
    
    print(f"Terminal: {terminal}")
    print(f"iTerm Mode: {is_iterm}")
    print(f"TERM: {os.environ.get('TERM', 'Not set')}")
    print(f"TERM_SESSION_ID: {os.environ.get('TERM_SESSION_ID', 'Not set')}")
    print(f"Python: {sys.version}")
    print(f"Platform: {sys.platform}")
    
    return is_iterm

def test_voice_bot_creation():
    """Test VoiceBot creation with debug logging"""
    print(f"\n{Fore.CYAN}🤖 Testing VoiceBot Creation{Style.RESET_ALL}")
    print(f"{Fore.CYAN}==========================={Style.RESET_ALL}")
    
    try:
        from voice_bot import VoiceBot
        print(f"{Fore.GREEN}✅ VoiceBot imported successfully{Style.RESET_ALL}")
        
        print(f"\n{Fore.YELLOW}⏳ Creating VoiceBot instance (this may take time)...{Style.RESET_ALL}")
        print(f"{Fore.BLUE}💡 Debug logs will show what's happening{Style.RESET_ALL}")
        
        # This will trigger all the debug logs we added
        bot = VoiceBot(
            models_dir="models",
            vosk_en_model="vosk-model-en-us-0.22",
            vosk_hi_model="vosk-model-hi-0.22",
            tts_language="en"
        )
        
        print(f"{Fore.GREEN}✅ VoiceBot created successfully{Style.RESET_ALL}")
        return bot
        
    except Exception as e:
        print(f"{Fore.RED}❌ VoiceBot creation failed: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        return None

def test_voice_bot_start(bot):
    """Test VoiceBot start method"""
    print(f"\n{Fore.CYAN}🎤 Testing VoiceBot Start{Style.RESET_ALL}")
    print(f"{Fore.CYAN}========================{Style.RESET_ALL}")
    
    if not bot:
        print(f"{Fore.RED}❌ No bot to test{Style.RESET_ALL}")
        return False
    
    try:
        print(f"{Fore.YELLOW}⏳ Starting voice bot...{Style.RESET_ALL}")
        print(f"{Fore.BLUE}💡 This should start listening for voice input{Style.RESET_ALL}")
        
        bot.start()
        print(f"{Fore.GREEN}✅ VoiceBot started successfully{Style.RESET_ALL}")
        
        # Let it run for a few seconds to see if voice input works
        print(f"{Fore.YELLOW}🎙️  Testing voice input for 10 seconds...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}💡 Try speaking - you should see voice activity{Style.RESET_ALL}")
        
        time.sleep(10)
        
        bot.stop()
        print(f"{Fore.GREEN}✅ VoiceBot stopped successfully{Style.RESET_ALL}")
        return True
        
    except Exception as e:
        print(f"{Fore.RED}❌ VoiceBot start test failed: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        return False

def test_cli_voice_mode():
    """Test CLI voice mode with debug logging"""
    print(f"\n{Fore.CYAN}🖥️  Testing CLI Voice Mode{Style.RESET_ALL}")
    print(f"{Fore.CYAN}========================={Style.RESET_ALL}")
    
    try:
        from voice_bot_cli import VoiceBotCLI
        print(f"{Fore.GREEN}✅ VoiceBotCLI imported successfully{Style.RESET_ALL}")
        
        # Create CLI instance
        cli = VoiceBotCLI()
        print(f"{Fore.GREEN}✅ CLI created successfully{Style.RESET_ALL}")
        
        # Create mock args
        class MockArgs:
            models_dir = "models"
            vosk_en_model = "vosk-model-en-us-0.22"
            vosk_hi_model = "vosk-model-hi-0.22"
            tts_language = "en"
            use_gpu = False
            sample_rate = 16000
            chunk_size = 1024
            verbose = True
        
        args = MockArgs()
        
        print(f"\n{Fore.YELLOW}⏳ Initializing bot through CLI...{Style.RESET_ALL}")
        success = cli.initialize_bot(args)
        
        if success:
            print(f"{Fore.GREEN}✅ Bot initialized through CLI{Style.RESET_ALL}")
            
            print(f"\n{Fore.YELLOW}⏳ Starting voice mode...{Style.RESET_ALL}")
            cli.start()
            
            # Test voice mode for a few seconds
            print(f"{Fore.CYAN}💡 Voice mode active - try speaking{Style.RESET_ALL}")
            time.sleep(5)
            
            cli.stop()
            print(f"{Fore.GREEN}✅ CLI test completed{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.RED}❌ Bot initialization failed{Style.RESET_ALL}")
            return False
        
    except Exception as e:
        print(f"{Fore.RED}❌ CLI voice mode test failed: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        return False

def analyze_debug_logs():
    """Analyze the debug log files"""
    print(f"\n{Fore.CYAN}📋 Analyzing Debug Logs{Style.RESET_ALL}")
    print(f"{Fore.CYAN}========================{Style.RESET_ALL}")
    
    log_files = ['voice_bot_debug.log', 'audio_debug.log']
    
    for log_file in log_files:
        if os.path.exists(log_file):
            print(f"\n{Fore.YELLOW}📄 {log_file}:{Style.RESET_ALL}")
            try:
                with open(log_file, 'r') as f:
                    lines = f.readlines()
                    # Show last 10 lines
                    for line in lines[-10:]:
                        print(f"  {line.strip()}")
            except Exception as e:
                print(f"  Error reading {log_file}: {e}")
        else:
            print(f"\n{Fore.YELLOW}📄 {log_file}: Not found{Style.RESET_ALL}")

def main():
    """Main debug test"""
    print(f"{Fore.BLUE}🔍 Voice Input Debug Test{Style.RESET_ALL}")
    print(f"{Fore.BLUE}========================{Style.RESET_ALL}")
    
    print(f"\n{Fore.YELLOW}💡 This comprehensive test will help identify why voice input doesn't work in iTerm{Style.RESET_ALL}")
    
    # Test environment
    is_iterm = test_environment()
    
    # Test VoiceBot creation
    bot = test_voice_bot_creation()
    
    # Test VoiceBot start
    if bot:
        test_voice_bot_start(bot)
    
    # Test CLI voice mode
    test_cli_voice_mode()
    
    # Analyze debug logs
    analyze_debug_logs()
    
    print(f"\n{Fore.CYAN}📊 Debug Test Summary:{Style.RESET_ALL}")
    print(f"Terminal: {os.environ.get('TERM_PROGRAM', 'Unknown')}")
    print(f"iTerm Mode: {is_iterm}")
    
    if is_iterm:
        print(f"\n{Fore.GREEN}🎯 iTerm Detected:{Style.RESET_ALL}")
        print(f"• Enhanced signal handling should be active")
        print(f"• Debug logs should show iTerm-specific behavior")
        print(f"• Check debug logs for audio stream issues")
    else:
        print(f"\n{Fore.BLUE}🖥️  Standard Terminal:{Style.RESET_ALL}")
        print(f"• Standard signal handling")
        print(f"• Compare behavior with iTerm")
    
    print(f"\n{Fore.YELLOW}💡 Next Steps:{Style.RESET_ALL}")
    print(f"1. Check the debug log files for detailed information")
    print(f"2. Look for audio device detection issues")
    print(f"3. Check for stream creation problems")
    print(f"4. Verify microphone permissions")
    
    print(f"\n{Fore.GREEN}🎉 Debug test completed!{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}👋 Debug test interrupted by user{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}❌ Debug test failed: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
