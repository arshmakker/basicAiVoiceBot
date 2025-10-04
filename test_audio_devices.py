#!/usr/bin/env python3
"""
Audio Device Handling Test
Tests audio device disconnection, switching, and permission scenarios
"""

import sys
import time
import threading
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional
import pyaudio
import numpy as np
from colorama import Fore, Style, init

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from voice_bot import VoiceBot, VoiceBotError
from voice_bot.audio_utils import AudioRecorder

init(autoreset=True)

class AudioDeviceTester:
    """Audio device handling tester"""
    
    def __init__(self):
        self.test_results: List[Dict[str, Any]] = []
        self.audio_recorder: Optional[AudioRecorder] = None
        
    def test_device_enumeration(self) -> bool:
        """Test audio device enumeration"""
        print(f"{Fore.CYAN}🔍 Testing Audio Device Enumeration{Style.RESET_ALL}")
        
        try:
            p = pyaudio.PyAudio()
            device_count = p.get_device_count()
            
            input_devices = []
            output_devices = []
            
            for i in range(device_count):
                device_info = p.get_device_info_by_index(i)
                if device_info['maxInputChannels'] > 0:
                    input_devices.append({
                        'index': i,
                        'name': device_info['name'],
                        'channels': device_info['maxInputChannels'],
                        'sample_rate': device_info['defaultSampleRate']
                    })
                if device_info['maxOutputChannels'] > 0:
                    output_devices.append({
                        'index': i,
                        'name': device_info['name'],
                        'channels': device_info['maxOutputChannels'],
                        'sample_rate': device_info['defaultSampleRate']
                    })
            
            p.terminate()
            
            print(f"{Fore.GREEN}✅ Found {len(input_devices)} input devices{Style.RESET_ALL}")
            print(f"{Fore.GREEN}✅ Found {len(output_devices)} output devices{Style.RESET_ALL}")
            
            # Display device details
            for device in input_devices:
                print(f"   Input {device['index']}: {device['name']} ({device['channels']} channels, {device['sample_rate']}Hz)")
            
            for device in output_devices:
                print(f"   Output {device['index']}: {device['name']} ({device['channels']} channels, {device['sample_rate']}Hz)")
            
            self.test_results.append({
                "test": "device_enumeration",
                "input_devices": len(input_devices),
                "output_devices": len(output_devices),
                "passed": len(input_devices) > 0 and len(output_devices) > 0
            })
            
            return len(input_devices) > 0 and len(output_devices) > 0
            
        except Exception as e:
            print(f"{Fore.RED}❌ Device enumeration failed: {e}{Style.RESET_ALL}")
            self.test_results.append({
                "test": "device_enumeration",
                "error": str(e),
                "passed": False
            })
            return False
    
    def test_device_selection(self) -> bool:
        """Test audio device selection and prioritization"""
        print(f"\n{Fore.CYAN}🎯 Testing Device Selection{Style.RESET_ALL}")
        
        try:
            # Test AudioRecorder device selection
            self.audio_recorder = AudioRecorder(sample_rate=16000, chunk_size=1024)
            
            # Test finding input device
            input_device = self.audio_recorder._find_input_device()
            
            if input_device is not None:
                print(f"{Fore.GREEN}✅ Selected input device: {input_device}{Style.RESET_ALL}")
                
                # Test device prioritization (MacBook Air Microphone)
                p = pyaudio.PyAudio()
                device_info = p.get_device_info_by_index(input_device)
                device_name = device_info['name']
                p.terminate()
                
                print(f"{Fore.GREEN}✅ Device name: {device_name}{Style.RESET_ALL}")
                
                # Check if it's the preferred device
                if "MacBook Air Microphone" in device_name:
                    print(f"{Fore.GREEN}✅ Using preferred MacBook Air Microphone{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}⚠️  Using fallback device: {device_name}{Style.RESET_ALL}")
                
                self.test_results.append({
                    "test": "device_selection",
                    "selected_device": input_device,
                    "device_name": device_name,
                    "is_preferred": "MacBook Air Microphone" in device_name,
                    "passed": True
                })
                
                return True
            else:
                print(f"{Fore.RED}❌ No input device selected{Style.RESET_ALL}")
                return False
                
        except Exception as e:
            print(f"{Fore.RED}❌ Device selection failed: {e}{Style.RESET_ALL}")
            self.test_results.append({
                "test": "device_selection",
                "error": str(e),
                "passed": False
            })
            return False
    
    def test_audio_stream_creation(self) -> bool:
        """Test audio stream creation and basic functionality"""
        print(f"\n{Fore.CYAN}🎵 Testing Audio Stream Creation{Style.RESET_ALL}")
        
        try:
            if not self.audio_recorder:
                print(f"{Fore.RED}❌ Audio recorder not initialized{Style.RESET_ALL}")
                return False
            
            # Test starting recording
            print(f"{Fore.YELLOW}Starting audio recording...{Style.RESET_ALL}")
            self.audio_recorder.start_recording()
            
            if self.audio_recorder.is_recording:
                print(f"{Fore.GREEN}✅ Audio recording started successfully{Style.RESET_ALL}")
                
                # Test getting audio chunks
                print(f"{Fore.YELLOW}Testing audio chunk retrieval...{Style.RESET_ALL}")
                
                chunk_count = 0
                valid_chunks = 0
                
                for i in range(10):  # Test 10 chunks
                    chunk = self.audio_recorder.get_audio_chunk()
                    chunk_count += 1
                    
                    if chunk is not None and len(chunk) > 0:
                        valid_chunks += 1
                        rms = np.sqrt(np.mean(chunk**2))
                        print(f"   Chunk {i+1}: {len(chunk)} samples, RMS: {rms:.4f}")
                    else:
                        print(f"   Chunk {i+1}: No data")
                    
                    time.sleep(0.1)  # Small delay
                
                print(f"{Fore.GREEN}✅ Retrieved {valid_chunks}/{chunk_count} valid audio chunks{Style.RESET_ALL}")
                
                # Test stopping recording
                print(f"{Fore.YELLOW}Stopping audio recording...{Style.RESET_ALL}")
                self.audio_recorder.stop_recording()
                
                if not self.audio_recorder.is_recording:
                    print(f"{Fore.GREEN}✅ Audio recording stopped successfully{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}❌ Audio recording failed to stop{Style.RESET_ALL}")
                    return False
                
                self.test_results.append({
                    "test": "audio_stream_creation",
                    "chunks_retrieved": valid_chunks,
                    "total_chunks": chunk_count,
                    "success_rate": valid_chunks / chunk_count,
                    "passed": valid_chunks >= chunk_count * 0.8  # 80% success rate
                })
                
                return valid_chunks >= chunk_count * 0.8
                
            else:
                print(f"{Fore.RED}❌ Audio recording failed to start{Style.RESET_ALL}")
                return False
                
        except Exception as e:
            print(f"{Fore.RED}❌ Audio stream test failed: {e}{Style.RESET_ALL}")
            self.test_results.append({
                "test": "audio_stream_creation",
                "error": str(e),
                "passed": False
            })
            return False
    
    def test_device_fallback(self) -> bool:
        """Test device fallback when primary device fails"""
        print(f"\n{Fore.CYAN}🔄 Testing Device Fallback{Style.RESET_ALL}")
        
        try:
            # Create a new audio recorder
            fallback_recorder = AudioRecorder(sample_rate=16000, chunk_size=1024)
            
            # Test with invalid device index
            print(f"{Fore.YELLOW}Testing with invalid device index...{Style.RESET_ALL}")
            
            # Temporarily set an invalid device
            original_device = fallback_recorder.input_device
            fallback_recorder.input_device = 999  # Invalid device index
            
            try:
                fallback_recorder.start_recording()
                print(f"{Fore.GREEN}✅ Fallback mechanism activated{Style.RESET_ALL}")
                
                # Check if it found a working device
                if fallback_recorder.input_device != 999:
                    print(f"{Fore.GREEN}✅ Fallback device selected: {fallback_recorder.input_device}{Style.RESET_ALL}")
                    
                    # Test that the fallback device works
                    chunk = fallback_recorder.get_audio_chunk()
                    if chunk is not None:
                        print(f"{Fore.GREEN}✅ Fallback device is functional{Style.RESET_ALL}")
                        fallback_recorder.stop_recording()
                        
                        self.test_results.append({
                            "test": "device_fallback",
                            "fallback_activated": True,
                            "fallback_device": fallback_recorder.input_device,
                            "passed": True
                        })
                        
                        return True
                    else:
                        print(f"{Fore.RED}❌ Fallback device not functional{Style.RESET_ALL}")
                        return False
                else:
                    print(f"{Fore.RED}❌ Fallback mechanism not working{Style.RESET_ALL}")
                    return False
                    
            except Exception as e:
                print(f"{Fore.RED}❌ Fallback test failed: {e}{Style.RESET_ALL}")
                return False
            
        except Exception as e:
            print(f"{Fore.RED}❌ Device fallback test failed: {e}{Style.RESET_ALL}")
            self.test_results.append({
                "test": "device_fallback",
                "error": str(e),
                "passed": False
            })
            return False
    
    def test_audio_permissions(self) -> bool:
        """Test audio permissions and access"""
        print(f"\n{Fore.CYAN}🔐 Testing Audio Permissions{Style.RESET_ALL}")
        
        try:
            # Test microphone access
            print(f"{Fore.YELLOW}Testing microphone access...{Style.RESET_ALL}")
            
            p = pyaudio.PyAudio()
            
            # Try to open a stream
            try:
                stream = p.open(
                    format=pyaudio.paFloat32,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=1024
                )
                
                print(f"{Fore.GREEN}✅ Microphone access granted{Style.RESET_ALL}")
                
                # Test reading from stream
                data = stream.read(1024, exception_on_overflow=False)
                audio_data = np.frombuffer(data, dtype=np.float32)
                rms = np.sqrt(np.mean(audio_data**2))
                
                print(f"{Fore.GREEN}✅ Audio data read successfully (RMS: {rms:.4f}){Style.RESET_ALL}")
                
                stream.stop_stream()
                stream.close()
                p.terminate()
                
                self.test_results.append({
                    "test": "audio_permissions",
                    "microphone_access": True,
                    "data_read": True,
                    "passed": True
                })
                
                return True
                
            except Exception as e:
                print(f"{Fore.RED}❌ Microphone access denied: {e}{Style.RESET_ALL}")
                p.terminate()
                
                self.test_results.append({
                    "test": "audio_permissions",
                    "microphone_access": False,
                    "error": str(e),
                    "passed": False
                })
                
                return False
                
        except Exception as e:
            print(f"{Fore.RED}❌ Audio permissions test failed: {e}{Style.RESET_ALL}")
            self.test_results.append({
                "test": "audio_permissions",
                "error": str(e),
                "passed": False
            })
            return False
    
    def test_voice_bot_audio_integration(self) -> bool:
        """Test voice bot audio integration"""
        print(f"\n{Fore.CYAN}🤖 Testing Voice Bot Audio Integration{Style.RESET_ALL}")
        
        try:
            # Check if models directory exists
            models_dir = Path("models")
            if not models_dir.exists():
                print(f"{Fore.RED}❌ Models directory not found{Style.RESET_ALL}")
                return False
            
            # Create voice bot with minimal settings
            print(f"{Fore.YELLOW}Creating voice bot...{Style.RESET_ALL}")
            voice_bot = VoiceBot(
                models_dir=str(models_dir),
                vosk_en_model="vosk-model-en-us-0.22",
                vosk_hi_model="vosk-model-hi-0.22",
                whisper_model="tiny",  # Use tiny model for faster testing
                tts_language="en",
                use_gpu=False,
                sample_rate=16000,
                chunk_size=1024
            )
            
            print(f"{Fore.GREEN}✅ Voice bot created successfully{Style.RESET_ALL}")
            
            # Test starting voice bot
            print(f"{Fore.YELLOW}Starting voice bot...{Style.RESET_ALL}")
            voice_bot.start()
            
            if voice_bot.is_listening:
                print(f"{Fore.GREEN}✅ Voice bot started listening{Style.RESET_ALL}")
                
                # Let it run for a few seconds
                time.sleep(3)
                
                # Test stopping voice bot
                print(f"{Fore.YELLOW}Stopping voice bot...{Style.RESET_ALL}")
                voice_bot.stop()
                
                if not voice_bot.is_listening:
                    print(f"{Fore.GREEN}✅ Voice bot stopped successfully{Style.RESET_ALL}")
                    
                    self.test_results.append({
                        "test": "voice_bot_audio_integration",
                        "bot_created": True,
                        "bot_started": True,
                        "bot_stopped": True,
                        "passed": True
                    })
                    
                    return True
                else:
                    print(f"{Fore.RED}❌ Voice bot failed to stop{Style.RESET_ALL}")
                    return False
            else:
                print(f"{Fore.RED}❌ Voice bot failed to start listening{Style.RESET_ALL}")
                return False
                
        except Exception as e:
            print(f"{Fore.RED}❌ Voice bot audio integration test failed: {e}{Style.RESET_ALL}")
            self.test_results.append({
                "test": "voice_bot_audio_integration",
                "error": str(e),
                "passed": False
            })
            return False
    
    def run_all_tests(self) -> bool:
        """Run all audio device tests"""
        print(f"{Fore.BLUE}🚀 Starting Audio Device Handling Tests{Style.RESET_ALL}")
        print(f"{Fore.BLUE}=========================================={Style.RESET_ALL}")
        
        # Run tests
        tests = [
            ("Device Enumeration", self.test_device_enumeration),
            ("Device Selection", self.test_device_selection),
            ("Audio Stream Creation", self.test_audio_stream_creation),
            ("Device Fallback", self.test_device_fallback),
            ("Audio Permissions", self.test_audio_permissions),
            ("Voice Bot Audio Integration", self.test_voice_bot_audio_integration),
        ]
        
        passed_tests = 0
        total_tests = len(tests)
        
        for test_name, test_func in tests:
            try:
                if test_func():
                    passed_tests += 1
                    print(f"{Fore.GREEN}✅ {test_name} PASSED{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}❌ {test_name} FAILED{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}❌ {test_name} ERROR: {e}{Style.RESET_ALL}")
        
        # Summary
        success_rate = passed_tests / total_tests
        print(f"\n{Fore.BLUE}📊 Test Summary{Style.RESET_ALL}")
        print(f"{Fore.BLUE}==============={Style.RESET_ALL}")
        print(f"Passed: {passed_tests}/{total_tests} ({success_rate:.1%})")
        
        if success_rate >= 0.8:
            print(f"{Fore.GREEN}🎉 Audio Device Handling Tests PASSED{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.RED}❌ Audio Device Handling Tests FAILED{Style.RESET_ALL}")
            return False

def main():
    """Main test runner"""
    tester = AudioDeviceTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()



