#!/usr/bin/env python3
"""
Cleanup Voice Bot Entry Points
Remove redundant files and keep only essential ones
"""

import os
import sys
from pathlib import Path
from colorama import Fore, Style, init

init(autoreset=True)

def cleanup_entry_points():
    """Clean up redundant entry points"""
    print(f"{Fore.CYAN}🧹 Cleaning Up Voice Bot Entry Points{Style.RESET_ALL}")
    print(f"{Fore.CYAN}===================================={Style.RESET_ALL}")
    
    # Files to keep (essential)
    keep_files = [
        "voice_bot.py",                    # Main entry point
        "minimal_voice_bot.py",            # Simple mode implementation
        "smart_voice_bot.py",              # Smart mode implementation
        "voice_bot_cli.py",                # Full mode implementation
        "voice_bot/",                      # Core voice bot modules
        "models/",                         # AI models
        "venv/",                          # Virtual environment
        "requirements.txt",                # Dependencies
        "README.md",                       # Documentation
        "PROJECT_SUMMARY.md",              # Project summary
        "MINIMAL_VOICE_BOT_GUIDE.md",      # Simple mode guide
        "SMART_VOICE_BOT_GUIDE.md",        # Smart mode guide
        ".gitignore",                      # Git ignore
    ]
    
    # Files to remove (redundant/test files)
    remove_files = [
        # Test files
        "test_minimal_bot.py",
        "test_smart_voice_bot.py",
        "test_iterm_compatibility.py",
        "test_tts_fix.py",
        "test_startup_announcement.py",
        "test_voice_input.py",
        "test_microphone_access.py",
        "test_simple_e2e.py",
        "test_e2e_conversation.py",
        "test_speech_recognition_accuracy.py",
        "test_error_recovery.py",
        "test_microphone.py",
        "test_voice_bot.py",
        "test_shutdown.py",
        
        # Debug files
        "debug_audio.py",
        "debug_voice_bot.py",
        "debug_audio_stream.py",
        "debug_iterm_voice_input.py",
        "iterm_compatibility_test.py",
        "iterm_compatible_voice_bot.py",
        
        # Demo files
        "demo_voice_bot.py",
        "simple_demo.py",
        "quick_demo.py",
        "live_test_guide.py",
        
        # Utility files
        "quick_voice_test.py",
        "simple_voice_test.py",
        "minimal_audio_test.py",
        "quick_audio_test.py",
        "lightweight_voice_bot.py",
        "memory_leak_investigation.py",
        "memory_leak_fix.py",
        "fix_tts_issues.py",
        "progress_bar.py",
        "voice_visualizer.py",
        "voice_visualizer_fixed.py",
        "text_chat.py",
        "check_microphone_permissions.py",
        
        # Install scripts
        "install_macos.py",
        "download_models.py",
        "setup.py",
        
        # Documentation
        "MACOS_INSTALL.md",
        
        # Log files
        "voice_bot.log",
        "audio_debug.log",
        "voice_bot_debug.log",
        
        # Temporary files
        "=0.10.0",
        "=0.12.1", 
        "=0.20.6",
        "=0.25.1",
        "=0.3.38",
        "=2.0.10",
        "=2.5.0",
        "=20231117",
    ]
    
    print(f"\n{Fore.YELLOW}📋 Files to Keep (Essential):{Style.RESET_ALL}")
    for file in keep_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} (not found)")
    
    print(f"\n{Fore.YELLOW}🗑️  Files to Remove (Redundant):{Style.RESET_ALL}")
    removed_count = 0
    for file in remove_files:
        if os.path.exists(file):
            try:
                if os.path.isdir(file):
                    import shutil
                    shutil.rmtree(file)
                    print(f"  🗂️  Removed directory: {file}")
                else:
                    os.remove(file)
                    print(f"  📄 Removed file: {file}")
                removed_count += 1
            except Exception as e:
                print(f"  ❌ Failed to remove {file}: {e}")
        else:
            print(f"  ⚪ Not found: {file}")
    
    print(f"\n{Fore.GREEN}✅ Cleanup completed!{Style.RESET_ALL}")
    print(f"{Fore.CYAN}📊 Removed {removed_count} redundant files{Style.RESET_ALL}")
    
    # Show final structure
    print(f"\n{Fore.CYAN}📁 Final Project Structure:{Style.RESET_ALL}")
    show_project_structure()

def show_project_structure():
    """Show the cleaned up project structure"""
    def print_tree(path, prefix="", max_depth=3, current_depth=0):
        if current_depth >= max_depth:
            return
        
        try:
            items = sorted(os.listdir(path))
            for i, item in enumerate(items):
                if item.startswith('.'):
                    continue
                
                is_last = i == len(items) - 1
                current_prefix = "└── " if is_last else "├── "
                print(f"{prefix}{current_prefix}{item}")
                
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    next_prefix = prefix + ("    " if is_last else "│   ")
                    print_tree(item_path, next_prefix, max_depth, current_depth + 1)
        except PermissionError:
            pass
    
    print_tree(".")

def create_usage_summary():
    """Create a usage summary"""
    print(f"\n{Fore.CYAN}📖 Usage Summary{Style.RESET_ALL}")
    print(f"{Fore.CYAN}==============={Style.RESET_ALL}")
    
    print(f"\n{Fore.YELLOW}🎯 Single Entry Point:{Style.RESET_ALL}")
    print(f"  python voice_bot.py [mode]")
    
    print(f"\n{Fore.YELLOW}📋 Available Modes:{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}smart{Style.RESET_ALL}   - Auto start/stop recording (recommended)")
    print(f"  {Fore.GREEN}simple{Style.RESET_ALL}  - Basic voice bot with startup announcement")
    print(f"  {Fore.GREEN}full{Style.RESET_ALL}    - Complete voice bot (may hang)")
    print(f"  {Fore.GREEN}test{Style.RESET_ALL}    - Run tests")
    
    print(f"\n{Fore.YELLOW}🚀 Quick Start:{Style.RESET_ALL}")
    print(f"  # Recommended mode")
    print(f"  python voice_bot.py smart")
    print(f"  ")
    print(f"  # Basic mode")
    print(f"  python voice_bot.py simple")
    print(f"  ")
    print(f"  # Run tests")
    print(f"  python voice_bot.py test")
    
    print(f"\n{Fore.YELLOW}💡 Features:{Style.RESET_ALL}")
    print(f"  • Single entry point with multiple modes")
    print(f"  • Clean project structure")
    print(f"  • Comprehensive help system")
    print(f"  • Automatic mode selection")
    print(f"  • Terminal compatibility")

def main():
    """Main cleanup function"""
    print(f"{Fore.BLUE}🧹 Voice Bot Cleanup{Style.RESET_ALL}")
    print(f"{Fore.BLUE}==================={Style.RESET_ALL}")
    
    print(f"\n{Fore.YELLOW}💡 This will clean up redundant files and create a single entry point{Style.RESET_ALL}")
    
    # Confirm cleanup
    response = input(f"\n{Fore.CYAN}Proceed with cleanup? (y/N): {Style.RESET_ALL}")
    if response.lower() not in ['y', 'yes']:
        print(f"{Fore.YELLOW}👋 Cleanup cancelled{Style.RESET_ALL}")
        return
    
    # Perform cleanup
    cleanup_entry_points()
    
    # Show usage summary
    create_usage_summary()
    
    print(f"\n{Fore.GREEN}🎉 Voice bot cleanup completed!{Style.RESET_ALL}")
    print(f"{Fore.CYAN}💡 You now have a clean, organized voice bot with a single entry point{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}👋 Cleanup interrupted{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}❌ Cleanup failed: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
