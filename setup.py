#!/usr/bin/env python3
"""
Setup Script for Voice Bot
Automated setup and installation script
"""

import os
import sys
import subprocess
import platform
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


def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} is not supported")
        print("   Please install Python 3.8 or higher")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True


def install_system_dependencies():
    """Install system dependencies based on OS"""
    print("📦 Installing system dependencies...")
    
    system = platform.system().lower()
    
    if system == "linux":
        # Try to detect Linux distribution
        try:
            with open("/etc/os-release", "r") as f:
                content = f.read().lower()
                if "ubuntu" in content or "debian" in content:
                    return run_command(
                        "sudo apt-get update && sudo apt-get install -y portaudio19-dev python3-dev",
                        "Installing audio dependencies (Ubuntu/Debian)"
                    )
                elif "centos" in content or "rhel" in content:
                    return run_command(
                        "sudo yum install -y portaudio-devel python3-devel",
                        "Installing audio dependencies (CentOS/RHEL)"
                    )
        except:
            pass
        
        print("⚠️  Could not detect Linux distribution")
        print("   Please install portaudio development libraries manually")
        return True
    
    elif system == "darwin":  # macOS
        print("🍎 macOS detected")
        print("   Installing audio dependencies...")
        
        # Check if Homebrew is installed
        if not run_command("which brew", "Checking for Homebrew"):
            print("❌ Homebrew not found. Please install Homebrew first:")
            print("   /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")
            return False
        
        # Install portaudio
        if not run_command("brew install portaudio", "Installing portaudio via Homebrew"):
            print("⚠️  Failed to install portaudio via Homebrew")
            print("   You may need to install it manually or use conda")
            return False
        
        return True
    
    elif system == "windows":
        print("ℹ️  Windows detected")
        print("   PyAudio will be installed via pip")
        return True
    
    else:
        print(f"⚠️  Unknown operating system: {system}")
        return True


def create_virtual_environment():
    """Create virtual environment"""
    print("🏗️  Setting up virtual environment...")
    
    venv_path = Path("venv")
    
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return True
    
    if not run_command("python -m venv venv", "Creating virtual environment"):
        return False
    
    print("✅ Virtual environment created")
    return True


def activate_virtual_environment():
    """Get activation command for virtual environment"""
    system = platform.system().lower()
    
    if system == "windows":
        return "venv\\Scripts\\activate"
    else:
        return "source venv/bin/activate"


def install_python_dependencies():
    """Install Python dependencies"""
    print("📚 Installing Python dependencies...")
    
    # Determine pip command
    system = platform.system().lower()
    if system == "windows":
        pip_cmd = "venv\\Scripts\\pip"
    else:
        pip_cmd = "venv/bin/pip"
    
    # Upgrade pip first
    if not run_command(f"{pip_cmd} install --upgrade pip", "Upgrading pip"):
        return False
    
    # Install requirements
    if not run_command(f"{pip_cmd} install -r requirements.txt", "Installing requirements"):
        return False
    
    print("✅ Python dependencies installed")
    return True


def download_models():
    """Download required models"""
    print("📥 Downloading models...")
    
    # Determine python command
    system = platform.system().lower()
    if system == "windows":
        python_cmd = "venv\\Scripts\\python"
    else:
        python_cmd = "venv/bin/python"
    
    if not run_command(f"{python_cmd} download_models.py --all", "Downloading models"):
        print("⚠️  Model download failed")
        print("   You can download models manually later with:")
        print(f"   {python_cmd} download_models.py --all")
        return False
    
    print("✅ Models downloaded successfully")
    return True


def run_tests():
    """Run test suite"""
    print("🧪 Running tests...")
    
    # Determine python command
    system = platform.system().lower()
    if system == "windows":
        python_cmd = "venv\\Scripts\\python"
    else:
        python_cmd = "venv/bin/python"
    
    if not run_command(f"{python_cmd} test_voice_bot.py", "Running test suite"):
        print("⚠️  Some tests failed")
        print("   Check the test output above for details")
        return False
    
    print("✅ All tests passed")
    return True


def print_next_steps():
    """Print next steps for the user"""
    system = platform.system().lower()
    
    if system == "windows":
        python_cmd = "venv\\Scripts\\python"
        activate_cmd = "venv\\Scripts\\activate"
    else:
        python_cmd = "venv/bin/python"
        activate_cmd = "source venv/bin/activate"
    
    print("\n" + "=" * 60)
    print("🎉 Setup completed successfully!")
    print("\nNext steps:")
    print(f"1. Activate virtual environment:")
    print(f"   {activate_cmd}")
    print(f"\n2. Run the voice bot:")
    print(f"   {python_cmd} voice_bot_cli.py")
    print(f"\n3. Or run in interactive mode:")
    print(f"   {python_cmd} voice_bot_cli.py --mode interactive")
    print(f"\n4. For help:")
    print(f"   {python_cmd} voice_bot_cli.py --help")
    print("\n" + "=" * 60)


def main():
    """Main setup function"""
    print("Voice Bot Setup Script")
    print("=" * 40)
    
    steps = [
        ("Python Version Check", check_python_version),
        ("System Dependencies", install_system_dependencies),
        ("Virtual Environment", create_virtual_environment),
        ("Python Dependencies", install_python_dependencies),
        ("Model Download", download_models),
        ("Test Suite", run_tests),
    ]
    
    failed_steps = []
    
    for step_name, step_func in steps:
        print(f"\n📋 {step_name}")
        print("-" * len(step_name))
        
        if not step_func():
            failed_steps.append(step_name)
            print(f"❌ {step_name} failed")
        else:
            print(f"✅ {step_name} completed")
    
    print("\n" + "=" * 40)
    
    if failed_steps:
        print(f"⚠️  Setup completed with {len(failed_steps)} failed steps:")
        for step in failed_steps:
            print(f"   - {step}")
        print("\nYou may need to fix these issues manually.")
        print("Check the error messages above for details.")
    else:
        print_next_steps()
    
    return len(failed_steps) == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
