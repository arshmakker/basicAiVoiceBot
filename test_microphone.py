#!/usr/bin/env python3
"""
Microphone Test Script
Tests microphone connection and audio input
"""

import pyaudio
import numpy as np
import time
import sys

def test_microphone():
    """Test microphone connection and audio input"""
    print("🎤 Testing Microphone Connection")
    print("=" * 50)
    
    # Initialize PyAudio
    p = pyaudio.PyAudio()
    
    try:
        # List available devices
        print("Available Audio Devices:")
        print("-" * 30)
        input_devices = []
        for i in range(p.get_device_count()):
            info = p.get_device_info_by_index(i)
            if info['maxInputChannels'] > 0:
                input_devices.append((i, info['name']))
                print(f"Input Device {i}: {info['name']}")
        
        if not input_devices:
            print("❌ No input devices found!")
            return False
        
        # Find MacBook Air Microphone
        macbook_device = None
        for device_id, device_name in input_devices:
            if "MacBook Air Microphone" in device_name:
                macbook_device = device_id
                break
        
        # Use MacBook Air Microphone if available, otherwise first device
        if macbook_device is not None:
            device_id = macbook_device
            device_name = "MacBook Air Microphone"
            print(f"\n✅ Using MacBook Air Microphone (Device {device_id})")
        else:
            device_id, device_name = input_devices[0]
            print(f"\n⚠️  Using fallback device: {device_name} (Device {device_id})")
        
        # Test audio recording
        print(f"\n🎙️  Testing audio input from {device_name}...")
        print("Speak into the microphone for 3 seconds...")
        
        # Audio parameters
        CHUNK = 1024
        FORMAT = pyaudio.paFloat32
        CHANNELS = 1
        RATE = 16000
        
        # Open audio stream
        stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            input_device_index=device_id,
            frames_per_buffer=CHUNK
        )
        
        # Record for 3 seconds
        frames = []
        for i in range(int(RATE / CHUNK * 3)):
            data = stream.read(CHUNK)
            frames.append(data)
        
        # Stop recording
        stream.stop_stream()
        stream.close()
        
        # Analyze audio
        audio_data = np.frombuffer(b''.join(frames), dtype=np.float32)
        rms = np.sqrt(np.mean(audio_data ** 2))
        
        print(f"\n📊 Audio Analysis:")
        print(f"   RMS Level: {rms:.4f}")
        
        if rms > 0.001:
            print("✅ Microphone is working! Audio detected.")
            return True
        else:
            print("⚠️  Very low audio level detected. Check microphone volume.")
            return True
            
    except Exception as e:
        print(f"❌ Error testing microphone: {e}")
        return False
    
    finally:
        p.terminate()

def main():
    """Main function"""
    success = test_microphone()
    
    if success:
        print("\n🎉 Microphone test completed successfully!")
        print("You can now run the voice bot:")
        print("python voice_bot_cli.py --mode interactive")
    else:
        print("\n❌ Microphone test failed!")
        print("Please check your microphone connection and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()

