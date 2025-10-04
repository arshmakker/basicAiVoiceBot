#!/usr/bin/env python3
"""
Voice Bot - Single Entry Point
Clean, organized voice bot with multiple modes
"""

import sys
import os
import argparse
import time
import threading
from pathlib import Path
from colorama import Fore, Style, init

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

init(autoreset=True)

def show_banner():
    """Show the voice bot banner"""
    print(f"{Fore.BLUE}╔══════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.BLUE}║                    🤖 VOICE BOT                            ║{Style.RESET_ALL}")
    print(f"{Fore.BLUE}║                                                              ║{Style.RESET_ALL}")
    print(f"{Fore.BLUE}║  Multiple modes available:                                    ║{Style.RESET_ALL}")
    print(f"{Fore.BLUE}║  • simple    - Basic voice bot with startup announcement    ║{Style.RESET_ALL}")
    print(f"{Fore.BLUE}║  • smart     - Auto start/stop recording (recommended)     ║{Style.RESET_ALL}")
    print(f"{Fore.BLUE}║  • manual    - Manual start/stop with single key commands ║{Style.RESET_ALL}")
    print(f"{Fore.BLUE}║  • full      - Complete voice bot (may hang)               ║{Style.RESET_ALL}")
    print(f"{Fore.BLUE}║  • test      - Run tests                                   ║{Style.RESET_ALL}")
    print(f"{Fore.BLUE}╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")

def run_simple_mode():
    """Run simple voice bot mode"""
    print(f"\n{Fore.CYAN}🎤 Starting Simple Voice Bot Mode{Style.RESET_ALL}")
    print(f"{Fore.CYAN}================================={Style.RESET_ALL}")
    
    try:
        from minimal_voice_bot import MinimalVoiceBot
        
        bot = MinimalVoiceBot()
        bot.run_interactive()
        
    except Exception as e:
        print(f"{Fore.RED}❌ Simple mode failed: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()

def run_smart_mode():
    """Run smart voice bot mode (recommended)"""
    print(f"\n{Fore.CYAN}🧠 Starting Smart Voice Bot Mode (Recommended){Style.RESET_ALL}")
    print(f"{Fore.CYAN}=============================================={Style.RESET_ALL}")
    
    try:
        from smart_voice_bot import SmartVoiceBot
        
        bot = SmartVoiceBot()
        bot.run_interactive()
        
    except Exception as e:
        print(f"{Fore.RED}❌ Smart mode failed: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()

def run_manual_mode():
    """Run manual voice bot mode with integrated transcription"""
    print(f"\n{Fore.CYAN}🎮 Starting Manual Voice Bot Mode{Style.RESET_ALL}")
    print(f"{Fore.CYAN}=================================={Style.RESET_ALL}")
    
    try:
        from voice_bot_cli import VoiceBotCLI
        
        cli = VoiceBotCLI()
        
        # Create mock args for manual mode
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
        
        # Initialize bot (lightweight for manual mode)
        print(f"{Fore.YELLOW}⏳ Initializing manual mode...{Style.RESET_ALL}")
        success = cli.initialize_bot(args)
        
        if success:
            print(f"{Fore.GREEN}✅ Manual mode initialized{Style.RESET_ALL}")
            cli.run_manual_mode()
        else:
            print(f"{Fore.RED}❌ Manual mode initialization failed{Style.RESET_ALL}")
            
    except Exception as e:
        print(f"{Fore.RED}❌ Manual mode failed: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()

def run_full_mode():
    """Run full voice bot mode (may hang)"""
    print(f"\n{Fore.YELLOW}⚠️  Starting Full Voice Bot Mode (May Hang){Style.RESET_ALL}")
    print(f"{Fore.YELLOW}============================================{Style.RESET_ALL}")
    print(f"{Fore.RED}⚠️  WARNING: This mode may hang due to memory issues{Style.RESET_ALL}")
    print(f"{Fore.RED}⚠️  Use 'smart' mode instead for reliable operation{Style.RESET_ALL}")
    
    try:
        from voice_bot_cli import VoiceBotCLI
        
        cli = VoiceBotCLI()
        
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
        
        print(f"{Fore.YELLOW}⏳ Initializing full voice bot (this may take 30+ seconds)...{Style.RESET_ALL}")
        success = cli.initialize_bot(args)
        
        if success:
            print(f"{Fore.GREEN}✅ Full voice bot initialized{Style.RESET_ALL}")
            cli.run_interactive()
        else:
            print(f"{Fore.RED}❌ Full voice bot initialization failed{Style.RESET_ALL}")
            
    except Exception as e:
        print(f"{Fore.RED}❌ Full mode failed: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()

def run_test_mode():
    """Run test mode"""
    print(f"\n{Fore.CYAN}🧪 Running Voice Bot Tests{Style.RESET_ALL}")
    print(f"{Fore.CYAN}=========================={Style.RESET_ALL}")
    
    try:
        # Test 1: System TTS
        print(f"\n{Fore.YELLOW}🔊 Testing System TTS...{Style.RESET_ALL}")
        import subprocess
        subprocess.run(["say", "Voice bot test successful"], check=True)
        print(f"{Fore.GREEN}✅ System TTS works{Style.RESET_ALL}")
        
        # Test 2: Audio Detection
        print(f"\n{Fore.YELLOW}🎤 Testing Audio Detection...{Style.RESET_ALL}")
        import pyaudio
        
        audio = pyaudio.PyAudio()
        device_count = audio.get_device_count()
        
        input_devices = []
        for i in range(device_count):
            device_info = audio.get_device_info_by_index(i)
            if device_info['maxInputChannels'] > 0:
                input_devices.append((i, device_info['name']))
        
        if input_devices:
            print(f"{Fore.GREEN}✅ Found {len(input_devices)} input devices{Style.RESET_ALL}")
            for i, name in input_devices[:3]:
                print(f"  • {name}")
        else:
            print(f"{Fore.RED}❌ No input devices found{Style.RESET_ALL}")
            return False
        
        audio.terminate()
        
        # Test 3: Voice Activity Detection
        print(f"\n{Fore.YELLOW}🎯 Testing Voice Activity Detection...{Style.RESET_ALL}")
        from smart_voice_bot import VoiceActivityDetector
        import numpy as np
        
        vad = VoiceActivityDetector()
        
        # Test silence
        silence_data = np.zeros(1024, dtype=np.int16).tobytes()
        result = vad.process_audio_chunk(silence_data)
        print(f"  Silence test: is_speaking={result['is_speaking']} ✅")
        
        # Test speech
        speech_data = (np.random.randn(1024) * 10000).astype(np.int16).tobytes()
        result = vad.process_audio_chunk(speech_data)
        print(f"  Speech test: is_speaking={result['is_speaking']} ✅")
        
        print(f"\n{Fore.GREEN}🎉 All tests passed!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}💡 You can now use any voice bot mode{Style.RESET_ALL}")
        
        return True
        
    except Exception as e:
        print(f"{Fore.RED}❌ Test mode failed: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        return False

def show_help():
    """Show help information"""
    print(f"\n{Fore.CYAN}📖 Voice Bot Help{Style.RESET_ALL}")
    print(f"{Fore.CYAN}================{Style.RESET_ALL}")
    
    print(f"\n{Fore.YELLOW}Available Modes:{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}simple{Style.RESET_ALL}  - Basic voice bot with startup announcement")
    print(f"  {Fore.GREEN}smart{Style.RESET_ALL}   - Auto start/stop recording (recommended)")
    print(f"  {Fore.GREEN}manual{Style.RESET_ALL}  - Manual start/stop with single key commands")
    print(f"  {Fore.GREEN}full{Style.RESET_ALL}    - Complete voice bot (may hang)")
    print(f"  {Fore.GREEN}test{Style.RESET_ALL}    - Run tests")
    
    print(f"\n{Fore.YELLOW}Usage Examples:{Style.RESET_ALL}")
    print(f"  python voice_bot.py smart          # Recommended mode")
    print(f"  python voice_bot.py manual         # Manual control mode")
    print(f"  python voice_bot.py simple         # Basic mode")
    print(f"  python voice_bot.py test           # Run tests")
    print(f"  python voice_bot.py --help         # Show this help")
    
    print(f"\n{Fore.YELLOW}Features by Mode:{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}Simple Mode:{Style.RESET_ALL}")
    print(f"    • Startup announcement")
    print(f"    • Audio recording")
    print(f"    • Clean shutdown")
    print(f"    • Low memory usage")
    
    print(f"  {Fore.GREEN}Smart Mode:{Style.RESET_ALL}")
    print(f"    • All simple mode features")
    print(f"    • Auto start recording when you speak")
    print(f"    • Auto stop after 3 seconds of silence")
    print(f"    • Real-time visualizer")
    print(f"    • Recording statistics")
    
    print(f"  {Fore.GREEN}Manual Mode:{Style.RESET_ALL}")
    print(f"    • All simple mode features")
    print(f"    • Single key commands: 's', 't', 'q'")
    print(f"    • Bot responses after recording")
    print(f"    • No admin privileges required")
    print(f"    • Full manual control")
    print(f"    • Recording statistics")
    
    print(f"  {Fore.GREEN}Full Mode:{Style.RESET_ALL}")
    print(f"    • Complete voice bot with AI models")
    print(f"    • Speech recognition")
    print(f"    • Dialog system")
    print(f"    • ⚠️  May hang due to memory issues")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Voice Bot - Multiple modes available",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python voice_bot.py smart          # Recommended: Auto start/stop recording
  python voice_bot.py simple         # Basic: Startup announcement + recording
  python voice_bot.py test           # Run tests
  python voice_bot.py --help         # Show detailed help
        """
    )
    
    parser.add_argument(
        'mode',
        nargs='?',
        choices=['simple', 'smart', 'manual', 'full', 'test'],
        default='smart',
        help='Voice bot mode (default: smart)'
    )
    
    parser.add_argument(
        '--help-mode',
        action='store_true',
        help='Show detailed help for all modes'
    )
    
    args = parser.parse_args()
    
    # Show banner
    show_banner()
    
    # Handle help mode
    if args.help_mode:
        show_help()
        return
    
    # Show terminal info
    terminal = os.environ.get('TERM_PROGRAM', 'Unknown')
    is_iterm = 'iTerm' in terminal
    print(f"\n{Fore.CYAN}Terminal: {terminal} (iTerm: {is_iterm}){Style.RESET_ALL}")
    
    # Run selected mode
    print(f"\n{Fore.YELLOW}🎯 Selected Mode: {args.mode.upper()}{Style.RESET_ALL}")
    
    try:
        if args.mode == 'simple':
            run_simple_mode()
        elif args.mode == 'smart':
            run_smart_mode()
        elif args.mode == 'manual':
            run_manual_mode()
        elif args.mode == 'full':
            run_full_mode()
        elif args.mode == 'test':
            run_test_mode()
        else:
            print(f"{Fore.RED}❌ Unknown mode: {args.mode}{Style.RESET_ALL}")
            show_help()
            
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}👋 Voice bot stopped by user{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}❌ Voice bot failed: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
