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
    # Import everything needed at the top
    from voice_bot.audio_utils import AudioRecorder, AudioTranscriber
    import signal
    import time
    import threading
    from colorama import Fore, Style
    
    print(f"\n{Fore.CYAN}🎮 Starting Manual Voice Bot Mode{Style.RESET_ALL}")
    print(f"{Fore.CYAN}=================================={Style.RESET_ALL}")
    
    try:
        
        # Initialize audio recorder and transcriber
        print(f"{Fore.YELLOW}⏳ Initializing audio components...{Style.RESET_ALL}")
        recorder = AudioRecorder()
        
        # Initialize transcriber with error handling
        transcriber = None
        try:
            transcriber = AudioTranscriber(models_dir="models")
            print(f"{Fore.GREEN}✅ Audio transcriber ready{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.YELLOW}⚠️  Transcriber initialization failed: {e}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}   Transcription will be disabled{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}   You can still record audio{Style.RESET_ALL}")
        
        is_recording = False
        recording_data = []
        running = True
        
        def signal_handler(signum, frame):
            nonlocal running
            print(f"\n{Fore.YELLOW}🛑 Received signal {signum}, shutting down...{Style.RESET_ALL}")
            running = False
            
            # Force cleanup for external terminals
            try:
                if 'recorder' in locals():
                    recorder.stop_recording()
                if 'transcriber' in locals() and transcriber:
                    transcriber.cleanup()
                print(f"{Fore.GREEN}✅ Cleanup completed{Style.RESET_ALL}")
            except:
                pass
            
            # Force exit for external terminals
            import os
            import sys
            os._exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        print(f"{Fore.GREEN}✅ Manual mode initialized{Style.RESET_ALL}")
        
        # Startup announcement
        startup_message = "Hey, We ready to rumble! Manual recording activated. Type 's' and press Enter to start recording."
        print(f"{Fore.MAGENTA}🔊 Startup: {startup_message}{Style.RESET_ALL}")
        
        # Try system TTS first (most reliable)
        try:
            import subprocess
            subprocess.run(["say", startup_message], check=True)
            print(f"{Fore.GREEN}✅ Startup announcement played via system TTS{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.YELLOW}⚠️  Startup TTS failed: {e}{Style.RESET_ALL}")
        
        print(f"{Fore.CYAN}🎤 Manual Mode - Press 's' + Enter to record, 't' + Enter to stop{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}💡 Controls: 's' + Enter = start, 't' + Enter = stop, 'q' + Enter = quit, 'h' + Enter = help{Style.RESET_ALL}")
        print(f"{Fore.GREEN}🎤 Manual recording ready{Style.RESET_ALL}")
        print(f"{Fore.WHITE}💡 Type 's' + Enter to start recording{Style.RESET_ALL}")
        print(f"{Fore.WHITE}💡 Type 't' + Enter to stop recording{Style.RESET_ALL}")
        print(f"{Fore.WHITE}💡 Type 'q' + Enter to quit{Style.RESET_ALL}")
        print(f"{Fore.WHITE}💡 Type 'h' + Enter for help{Style.RESET_ALL}")
        
        while running:
            try:
                command = input(f"\n{Fore.CYAN}Voice Bot> {Style.RESET_ALL}").strip().lower()
                
                if command in ['s', 'start']:
                    if not is_recording:
                        is_recording = True
                        recording_data = []
                        print(f"\n{Fore.GREEN}🔴 RECORDING STARTED{Style.RESET_ALL}")
                        print(f"{Fore.WHITE}💡 Type 't' + Enter to stop recording{Style.RESET_ALL}")
                        
                        # Voice feedback for recording start
                        try:
                            import subprocess
                            subprocess.run(["say", "Recording started"], check=True)
                        except:
                            pass
                        
                        # Start recording
                        recorder.start_recording()
                        
                        # Use threading to handle recording without blocking input
                        def recording_loop():
                            nonlocal is_recording, recording_data
                            while is_recording and running:
                                try:
                                    data = recorder.stream.read(recorder.chunk_size, exception_on_overflow=False)
                                    recording_data.append(data)
                                except:
                                    break
                        
                        # Start recording in background thread
                        recording_thread = threading.Thread(target=recording_loop)
                        recording_thread.daemon = True
                        recording_thread.start()
                    else:
                        print(f"{Fore.YELLOW}⚠️  Already recording{Style.RESET_ALL}")
                        
                elif command in ['t', 'stop']:
                    if is_recording:
                        is_recording = False
                        recorder.stop_recording()
                        
                        print(f"\n{Fore.YELLOW}⏹️  RECORDING STOPPED{Style.RESET_ALL}")
                        
                        # Voice feedback for recording stop
                        try:
                            import subprocess
                            subprocess.run(["say", "Recording stopped"], check=True)
                        except:
                            pass
                        
                        # Calculate duration
                        if recording_data:
                            total_bytes = len(b''.join(recording_data))
                            duration = total_bytes / (2 * 16000)  # 16-bit, 16kHz
                            print(f"{Fore.CYAN}📊 Recording stats:{Style.RESET_ALL}")
                            print(f"  • Duration: {duration:.1f} seconds")
                            print(f"  • Audio chunks: {len(recording_data)}")
                            print(f"  • Total size: {total_bytes} bytes")
                            
                            # Transcribe audio with timeout protection
                            if transcriber:
                                print(f"{Fore.CYAN}🔄 Processing recording for transcription...{Style.RESET_ALL}")
                                audio_data = b''.join(recording_data)
                                
                                # Add timeout protection for transcription
                                try:
                                    import signal
                                    
                                    def timeout_handler(signum, frame):
                                        raise TimeoutError("Transcription timeout")
                                    
                                    # Set 10 second timeout for transcription
                                    old_handler = signal.signal(signal.SIGALRM, timeout_handler)
                                    signal.alarm(10)
                                    
                                    try:
                                        transcript = transcriber.transcribe_audio(audio_data)
                                    finally:
                                        signal.alarm(0)
                                        signal.signal(signal.SIGALRM, old_handler)
                                        
                                except TimeoutError:
                                    print(f"{Fore.YELLOW}⚠️  Transcription timeout - please try again{Style.RESET_ALL}")
                                    transcript = "Transcription timeout - please try again"
                                except Exception as e:
                                    print(f"{Fore.YELLOW}⚠️  Transcription error: {e}{Style.RESET_ALL}")
                                    transcript = "Transcription failed - please try again"
                            else:
                                print(f"{Fore.YELLOW}⚠️  Transcription disabled{Style.RESET_ALL}")
                                transcript = "Transcription not available"
                            
                            if transcript and transcript != "No speech detected":
                                print(f"\n{Fore.MAGENTA}📝 Transcript:{Style.RESET_ALL}")
                                print(f"{Fore.WHITE}'{transcript}'{Style.RESET_ALL}")
                                
                                # Speak the transcript back using system TTS
                                print(f"\n{Fore.WHITE}🔊 Speaking transcript...{Style.RESET_ALL}")
                                try:
                                    import subprocess
                                    subprocess.run(["say", f"I heard you say: {transcript}"], check=True)
                                except Exception as e:
                                    print(f"{Fore.YELLOW}⚠️  TTS failed: {e}{Style.RESET_ALL}")
                            else:
                                print(f"{Fore.YELLOW}⚠️  No speech detected{Style.RESET_ALL}")
                                try:
                                    import subprocess
                                    subprocess.run(["say", "I couldn't understand what you said."], check=True)
                                except:
                                    pass
                            
                            print(f"\n{Fore.GREEN}✅ Transcription completed{Style.RESET_ALL}")
                            print(f"{Fore.WHITE}💡 Type 's' + Enter to start new recording{Style.RESET_ALL}")
                            
                            # Clear recording data
                            recording_data = []
                    else:
                        print(f"{Fore.YELLOW}⚠️  Not currently recording{Style.RESET_ALL}")
                        
                elif command in ['q', 'quit', 'exit']:
                    print(f"{Fore.YELLOW}👋 Exiting manual mode...{Style.RESET_ALL}")
                    running = False
                    
                elif command in ['h', 'help']:
                    print(f"{Fore.CYAN}Commands (type + Enter):{Style.RESET_ALL}")
                    print(f"  {Fore.WHITE}s / start{Style.RESET_ALL} - Begin recording")
                    print(f"  {Fore.WHITE}t / stop{Style.RESET_ALL}  - Stop recording")
                    print(f"  {Fore.WHITE}q / quit{Style.RESET_ALL}  - Exit the bot")
                    print(f"  {Fore.WHITE}h / help{Style.RESET_ALL}  - Show this help")
                    print(f"\n{Fore.YELLOW}💡 Remember: Type the command and press Enter!{Style.RESET_ALL}")
                    
                elif command == '':
                    continue
                else:
                    print(f"{Fore.YELLOW}Unknown command: {command}{Style.RESET_ALL}")
                    print(f"{Fore.WHITE}Type 'h' + Enter for help{Style.RESET_ALL}")

            except EOFError:
                print(f"\n{Fore.YELLOW}👋 Exiting manual mode...{Style.RESET_ALL}")
                running = False
                break
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}👋 Manual mode stopped by user{Style.RESET_ALL}")
                running = False
                break
                
    except Exception as e:
        print(f"{Fore.RED}❌ Manual mode failed: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup
        try:
            if 'recorder' in locals():
                recorder.stop_recording()
            if 'transcriber' in locals() and transcriber:
                transcriber.cleanup()
            # Ensure any background threads are properly terminated
            import os
            import time
            time.sleep(0.5)  # Give threads time to cleanup
        except:
            pass

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
        # Test 1: System TTS (with Docker fallback)
        print(f"\n{Fore.YELLOW}🔊 Testing System TTS...{Style.RESET_ALL}")
        import subprocess
        try:
            subprocess.run(["say", "Voice bot test successful"], check=True)
            print(f"{Fore.GREEN}✅ System TTS works{Style.RESET_ALL}")
        except FileNotFoundError:
            print(f"{Fore.YELLOW}⚠️  System TTS not available (expected in Docker){Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.YELLOW}⚠️  System TTS test failed: {e}{Style.RESET_ALL}")
        
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
        
        print(f"\n{Fore.GREEN}🎉 Core tests completed!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}💡 Note: Some features may not work in Docker containers{Style.RESET_ALL}")
        
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
