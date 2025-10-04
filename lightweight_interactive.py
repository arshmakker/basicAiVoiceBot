#!/usr/bin/env python3
"""
Lightweight Interactive Voice Bot
Only loads text processing components - no heavy ASR/TTS models
"""

import sys
import time
from pathlib import Path
from colorama import Fore, Style, init

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

init(autoreset=True)

def lightweight_interactive():
    """Lightweight interactive mode with minimal components"""
    print(f"{Fore.CYAN}💬 Lightweight Interactive Voice Bot{Style.RESET_ALL}")
    print(f"{Fore.CYAN}===================================={Style.RESET_ALL}")
    
    try:
        print(f"\n{Fore.YELLOW}⏳ Loading lightweight components...{Style.RESET_ALL}")
        
        # Only load the lightweight components
        from voice_bot.language_detection import LanguageDetector
        from voice_bot.dialog_system import DialogManager
        
        print(f"{Fore.GREEN}✅ Language detection loaded{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✅ Dialog system loaded{Style.RESET_ALL}")
        
        # Initialize components
        detector = LanguageDetector()
        dialog = DialogManager()
        
        print(f"{Fore.GREEN}✅ All lightweight components ready!{Style.RESET_ALL}")
        
        # Show available commands
        print(f"\n{Fore.BLUE}🎯 Available Commands:{Style.RESET_ALL}")
        print(f"   • Type any text to get a response")
        print(f"   • 'help' - Show this help")
        print(f"   • 'status' - Show component status")
        print(f"   • 'quit' - Exit the program")
        
        print(f"\n{Fore.YELLOW}💡 Try typing: 'Hello' or 'नमस्ते'{Style.RESET_ALL}")
        
        # Interactive loop
        conversation_count = 0
        
        while True:
            try:
                # Get user input
                user_input = input(f"\n{Fore.BLUE}🤖> {Style.RESET_ALL}").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print(f"{Fore.YELLOW}👋 Goodbye!{Style.RESET_ALL}")
                    break
                
                elif user_input.lower() == 'help':
                    print(f"\n{Fore.CYAN}🤖 Lightweight Voice Bot Help{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}============================{Style.RESET_ALL}")
                    print(f"• Type any text to chat with the bot")
                    print(f"• Supports English and Hindi")
                    print(f"• 'status' - Show component status")
                    print(f"• 'quit' - Exit")
                    
                elif user_input.lower() == 'status':
                    print(f"\n{Fore.BLUE}📊 Component Status:{Style.RESET_ALL}")
                    print(f"   Language Detection: ✅ Ready")
                    print(f"   Dialog System: ✅ Ready")
                    print(f"   Conversations: {conversation_count}")
                    
                else:
                    # Process the input
                    print(f"{Fore.CYAN}Processing: '{user_input}'{Style.RESET_ALL}")
                    
                    # Detect language
                    lang, confidence = detector.detect_language(user_input)
                    print(f"{Fore.BLUE}Detected Language: {lang} (confidence: {confidence:.2f}){Style.RESET_ALL}")
                    
                    # Generate response
                    response = dialog.process_input(user_input, lang)
                    print(f"{Fore.GREEN}Bot: {response}{Style.RESET_ALL}")
                    
                    conversation_count += 1
                
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}👋 Goodbye!{Style.RESET_ALL}")
                break
            except Exception as e:
                print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")
        
        print(f"\n{Fore.GREEN}🎉 Interactive session completed!{Style.RESET_ALL}")
        print(f"Total conversations: {conversation_count}")
        
        return True
        
    except Exception as e:
        print(f"{Fore.RED}❌ Failed to start lightweight interactive mode: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = lightweight_interactive()
    sys.exit(0 if success else 1)
