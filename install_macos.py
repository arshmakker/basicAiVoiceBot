#!/usr/bin/env python3
"""
macOS Installation Helper for Voice Bot
Handles macOS-specific installation issues
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"   stdout: {e.stdout}")
        if e.stderr:
            print(f"   stderr: {e.stderr}")
        return False


def check_homebrew():
    """Check if Homebrew is installed"""
    print("🍺 Checking Homebrew installation...")
    
    if run_command("which brew", "Checking for Homebrew"):
        print("✅ Homebrew is installed")
        return True
    else:
        print("❌ Homebrew not found")
        print("\n📋 To install Homebrew, run:")
        print('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"')
        return False


def install_portaudio():
    """Install portaudio via Homebrew"""
    print("🔊 Installing portaudio...")
    
    if not run_command("brew install portaudio", "Installing portaudio"):
        print("❌ Failed to install portaudio")
        return False
    
    print("✅ portaudio installed successfully")
    return True


def install_pyaudio():
    """Install PyAudio with proper flags"""
    print("🎤 Installing PyAudio...")
    
    # Try different installation methods
    methods = [
        "pip install pyaudio",
        "pip install --global-option='build_ext' --global-option='-I/opt/homebrew/include' --global-option='-L/opt/homebrew/lib' pyaudio",
        "pip install --global-option='build_ext' --global-option='-I/usr/local/include' --global-option='-L/usr/local/lib' pyaudio"
    ]
    
    for method in methods:
        print(f"🔄 Trying: {method}")
        if run_command(method, f"Installing PyAudio with method: {method}"):
            print("✅ PyAudio installed successfully")
            return True
    
    print("❌ All PyAudio installation methods failed")
    print("\n📋 Alternative solutions:")
    print("1. Try installing via conda:")
    print("   conda install pyaudio")
    print("2. Try installing via pip with system Python:")
    print("   python3 -m pip install pyaudio")
    print("3. Use a different Python environment manager")
    
    return False


def install_requirements():
    """Install requirements.txt with error handling"""
    print("📚 Installing requirements...")
    
    # Install basic dependencies first
    basic_deps = [
        "numpy",
        "scipy", 
        "requests",
        "tqdm",
        "colorama",
        "langdetect"
    ]
    
    for dep in basic_deps:
        if not run_command(f"pip install {dep}", f"Installing {dep}"):
            print(f"⚠️  Failed to install {dep}")
    
    # Try to install PyAudio separately
    if not install_pyaudio():
        print("⚠️  PyAudio installation failed - continuing without it")
    
    # Install remaining dependencies
    remaining_deps = [
        "vosk>=0.3.38",
        "openai-whisper>=20231117", 
        "TTS>=0.20.6",
        "librosa>=0.10.0",
        "soundfile>=0.12.1",
        "pygame>=2.5.0",
        "webrtcvad>=2.0.10",
        "pydub>=0.25.1"
    ]
    
    for dep in remaining_deps:
        if not run_command(f"pip install {dep}", f"Installing {dep}"):
            print(f"⚠️  Failed to install {dep}")
    
    print("✅ Requirements installation completed")
    return True


def test_installation():
    """Test the installation"""
    print("🧪 Testing installation...")
    
    # Test basic imports
    test_imports = [
        "import numpy",
        "import requests", 
        "import tqdm",
        "import colorama",
        "import langdetect"
    ]
    
    for test in test_imports:
        if not run_command(f"python -c '{test}'", f"Testing {test}"):
            print(f"❌ Failed to import {test.split()[-1]}")
            return False
    
    # Test PyAudio separately
    if not run_command("python -c 'import pyaudio'", "Testing PyAudio"):
        print("⚠️  PyAudio not available - audio features will be limited")
    
    print("✅ Installation test completed")
    return True


def main():
    """Main installation function"""
    print("🍎 macOS Voice Bot Installation Helper")
    print("=" * 50)
    
    steps = [
        ("Homebrew Check", check_homebrew),
        ("PortAudio Installation", install_portaudio),
        ("Requirements Installation", install_requirements),
        ("Installation Test", test_installation)
    ]
    
    failed_steps = []
    
    for step_name, step_func in steps:
        print(f"\n📋 {step_name}")
        print("-" * len(step_name))
        
        if not step_func():
            failed_steps.append(step_name)
    
    print("\n" + "=" * 50)
    
    if failed_steps:
        print(f"⚠️  Installation completed with {len(failed_steps)} failed steps:")
        for step in failed_steps:
            print(f"   - {step}")
        print("\nYou may need to fix these issues manually.")
    else:
        print("🎉 Installation completed successfully!")
        print("\nNext steps:")
        print("1. Download models: python download_models.py --all")
        print("2. Run tests: python test_voice_bot.py")
        print("3. Start voice bot: python voice_bot_cli.py")
    
    return len(failed_steps) == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
