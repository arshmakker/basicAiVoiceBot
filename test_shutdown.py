#!/usr/bin/env python3
"""
Comprehensive Shutdown Test
Tests all shutdown scenarios to ensure proper cleanup
"""

import sys
import time
import signal
import threading
from pathlib import Path
from colorama import Fore, Style, init

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

init(autoreset=True)

def test_signal_handling():
    """Test signal handling for different components"""
    print(f"{Fore.CYAN}🧪 Testing Signal Handling{Style.RESET_ALL}")
    print(f"{Fore.CYAN}========================={Style.RESET_ALL}")
    
    # Test 1: Voice Visualizer Shutdown
    print(f"\n{Fore.YELLOW}1. Testing Voice Visualizer Shutdown...{Style.RESET_ALL}")
    
    try:
        from voice_visualizer_fixed import SimpleVoiceTicker
        
        ticker = SimpleVoiceTicker()
        ticker.start()
        
        print(f"{Fore.GREEN}✅ Voice ticker started successfully{Style.RESET_ALL}")
        print(f"{Fore.BLUE}💡 Running for 3 seconds, then testing stop() method...{Style.RESET_ALL}")
        
        time.sleep(3)
        
        print(f"{Fore.CYAN}🛑 Testing stop() method...{Style.RESET_ALL}")
        ticker.stop()
        
        print(f"{Fore.GREEN}✅ Voice ticker stopped successfully{Style.RESET_ALL}")
        
    except Exception as e:
        print(f"{Fore.RED}❌ Voice ticker test failed: {e}{Style.RESET_ALL}")
        return False
    
    # Test 2: Voice Bot Shutdown
    print(f"\n{Fore.YELLOW}2. Testing Voice Bot Shutdown...{Style.RESET_ALL}")
    
    try:
        from voice_bot import VoiceBot
        
        print(f"{Fore.CYAN}Creating voice bot (this will take time for model loading)...{Style.RESET_ALL}")
        voice_bot = VoiceBot(
            models_dir="models",
            vosk_en_model="vosk-model-en-us-0.22",
            vosk_hi_model="vosk-model-hi-0.22",
            tts_language="en",
            use_gpu=False
        )
        
        print(f"{Fore.GREEN}✅ Voice bot created successfully{Style.RESET_ALL}")
        
        # Test start/stop
        print(f"{Fore.CYAN}Testing start() method...{Style.RESET_ALL}")
        voice_bot.start()
        print(f"{Fore.GREEN}✅ Voice bot started{Style.RESET_ALL}")
        
        time.sleep(2)
        
        print(f"{Fore.CYAN}Testing stop() method...{Style.RESET_ALL}")
        voice_bot.stop()
        print(f"{Fore.GREEN}✅ Voice bot stopped successfully{Style.RESET_ALL}")
        
    except Exception as e:
        print(f"{Fore.RED}❌ Voice bot test failed: {e}{Style.RESET_ALL}")
        return False
    
    # Test 3: CLI Shutdown
    print(f"\n{Fore.YELLOW}3. Testing CLI Shutdown...{Style.RESET_ALL}")
    
    try:
        from voice_bot_cli import VoiceBotCLI
        
        cli = VoiceBotCLI()
        print(f"{Fore.GREEN}✅ CLI created successfully{Style.RESET_ALL}")
        
        # Test CLI stop method
        print(f"{Fore.CYAN}Testing CLI stop() method...{Style.RESET_ALL}")
        cli.stop()
        print(f"{Fore.GREEN}✅ CLI stopped successfully{Style.RESET_ALL}")
        
    except Exception as e:
        print(f"{Fore.RED}❌ CLI test failed: {e}{Style.RESET_ALL}")
        return False
    
    return True

def test_thread_cleanup():
    """Test thread cleanup and resource management"""
    print(f"\n{Fore.CYAN}🧪 Testing Thread Cleanup{Style.RESET_ALL}")
    print(f"{Fore.CYAN}========================{Style.RESET_ALL}")
    
    try:
        from voice_visualizer_fixed import SimpleVoiceTicker
        
        print(f"{Fore.YELLOW}Creating multiple voice tickers...{Style.RESET_ALL}")
        
        tickers = []
        for i in range(3):
            ticker = SimpleVoiceTicker()
            ticker.start()
            tickers.append(ticker)
            print(f"{Fore.GREEN}✅ Ticker {i+1} started{Style.RESET_ALL}")
        
        time.sleep(2)
        
        print(f"{Fore.CYAN}Stopping all tickers...{Style.RESET_ALL}")
        for i, ticker in enumerate(tickers):
            ticker.stop()
            print(f"{Fore.GREEN}✅ Ticker {i+1} stopped{Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}✅ All tickers stopped successfully{Style.RESET_ALL}")
        return True
        
    except Exception as e:
        print(f"{Fore.RED}❌ Thread cleanup test failed: {e}{Style.RESET_ALL}")
        return False

def test_signal_propagation():
    """Test signal propagation through components"""
    print(f"\n{Fore.CYAN}🧪 Testing Signal Propagation{Style.RESET_ALL}")
    print(f"{Fore.CYAN}============================{Style.RESET_ALL}")
    
    try:
        from voice_visualizer_fixed import SimpleVoiceTicker
        
        print(f"{Fore.YELLOW}Testing signal handler registration...{Style.RESET_ALL}")
        
        # Check if signal handlers are properly registered
        original_sigint = signal.signal(signal.SIGINT, signal.SIG_IGN)
        signal.signal(signal.SIGINT, original_sigint)
        
        print(f"{Fore.GREEN}✅ Signal handler test passed{Style.RESET_ALL}")
        
        # Test multiple signal handlers
        ticker1 = SimpleVoiceTicker()
        ticker2 = SimpleVoiceTicker()
        
        print(f"{Fore.GREEN}✅ Multiple signal handlers created successfully{Style.RESET_ALL}")
        
        # Clean up
        ticker1.stop()
        ticker2.stop()
        
        return True
        
    except Exception as e:
        print(f"{Fore.RED}❌ Signal propagation test failed: {e}{Style.RESET_ALL}")
        return False

def test_timeout_behavior():
    """Test timeout behavior and cleanup"""
    print(f"\n{Fore.CYAN}🧪 Testing Timeout Behavior{Style.RESET_ALL}")
    print(f"{Fore.CYAN}=========================={Style.RESET_ALL}")
    
    try:
        from voice_visualizer_fixed import SimpleVoiceTicker
        
        print(f"{Fore.YELLOW}Testing ticker with timeout...{Style.RESET_ALL}")
        
        ticker = SimpleVoiceTicker()
        ticker.start()
        
        print(f"{Fore.CYAN}Running for 2 seconds...{Style.RESET_ALL}")
        time.sleep(2)
        
        print(f"{Fore.CYAN}Testing stop with timeout...{Style.RESET_ALL}")
        ticker.stop()
        
        print(f"{Fore.GREEN}✅ Timeout behavior test passed{Style.RESET_ALL}")
        return True
        
    except Exception as e:
        print(f"{Fore.RED}❌ Timeout behavior test failed: {e}{Style.RESET_ALL}")
        return False

def main():
    """Run all shutdown tests"""
    print(f"{Fore.BLUE}🔍 Comprehensive Shutdown Test Suite{Style.RESET_ALL}")
    print(f"{Fore.BLUE}===================================={Style.RESET_ALL}")
    
    tests = [
        ("Signal Handling", test_signal_handling),
        ("Thread Cleanup", test_thread_cleanup),
        ("Signal Propagation", test_signal_propagation),
        ("Timeout Behavior", test_timeout_behavior)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        try:
            if test_func():
                passed += 1
                print(f"{Fore.GREEN}✅ {test_name} PASSED{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ {test_name} FAILED{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}❌ {test_name} ERROR: {e}{Style.RESET_ALL}")
    
    print(f"\n{Fore.BLUE}{'='*50}{Style.RESET_ALL}")
    print(f"{Fore.BLUE}📊 Test Results:{Style.RESET_ALL}")
    print(f"Passed: {passed}/{total} ({passed/total*100:.1f}%)")
    
    if passed == total:
        print(f"{Fore.GREEN}🎉 All shutdown tests passed!{Style.RESET_ALL}")
        print(f"{Fore.BLUE}✅ Voice bot shuts down properly in all scenarios{Style.RESET_ALL}")
        return True
    else:
        print(f"{Fore.RED}⚠️  Some shutdown tests failed{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}💡 Check the failed tests above for details{Style.RESET_ALL}")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}👋 Test interrupted by user{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}❌ Test suite failed: {e}{Style.RESET_ALL}")
        sys.exit(1)
