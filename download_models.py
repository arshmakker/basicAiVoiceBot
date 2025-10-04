#!/usr/bin/env python3
"""
Model Downloader for Voice Bot
Automatically downloads required models for ASR and TTS
"""

import os
import sys
import requests
import zipfile
import tarfile
from pathlib import Path
from tqdm import tqdm
import argparse


class ModelDownloader:
    """Handles downloading and setup of required models"""
    
    def __init__(self, models_dir="models"):
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(exist_ok=True)
        
        # Model configurations
        self.models = {
            "vosk_en": {
                "url": "https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip",
                "filename": "vosk-model-en-us-0.22.zip",
                "extract_dir": "vosk-model-en-us-0.22"
            },
            "vosk_hi": {
                "url": "https://alphacephei.com/vosk/models/vosk-model-hi-0.22.zip", 
                "filename": "vosk-model-hi-0.22.zip",
                "extract_dir": "vosk-model-hi-0.22"
            },
            "whisper": {
                "url": "https://openaipublic.azureedge.net/main/whisper/models/ed3a0b6b1c0edf879ad9b11b1af5a0e6d1bb5de3bea4046af3849889c54472b/medium.pt",
                "filename": "whisper-medium.pt",
                "extract_dir": None
            }
        }
    
    def download_file(self, url, filename, chunk_size=8192):
        """Download file with progress bar"""
        filepath = self.models_dir / filename
        
        if filepath.exists():
            print(f"✓ {filename} already exists, skipping download")
            return filepath
            
        print(f"Downloading {filename}...")
        
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            
            with open(filepath, 'wb') as f:
                with tqdm(total=total_size, unit='B', unit_scale=True, desc=filename) as pbar:
                    for chunk in response.iter_content(chunk_size=chunk_size):
                        if chunk:
                            f.write(chunk)
                            pbar.update(len(chunk))
            
            print(f"✓ Downloaded {filename}")
            return filepath
            
        except Exception as e:
            print(f"✗ Error downloading {filename}: {e}")
            if filepath.exists():
                filepath.unlink()
            return None
    
    def extract_zip(self, zip_path, extract_dir):
        """Extract zip file"""
        extract_path = self.models_dir / extract_dir
        
        if extract_path.exists():
            print(f"✓ {extract_dir} already extracted")
            return extract_path
            
        print(f"Extracting {zip_path.name}...")
        
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(self.models_dir)
            
            print(f"✓ Extracted to {extract_path}")
            return extract_path
            
        except Exception as e:
            print(f"✗ Error extracting {zip_path.name}: {e}")
            return None
    
    def download_model(self, model_name):
        """Download and setup a specific model"""
        if model_name not in self.models:
            print(f"✗ Unknown model: {model_name}")
            return False
            
        model_config = self.models[model_name]
        
        # Download the file
        filepath = self.download_file(model_config["url"], model_config["filename"])
        if not filepath:
            return False
        
        # Extract if it's a zip file
        if model_config["extract_dir"]:
            extract_path = self.extract_zip(filepath, model_config["extract_dir"])
            if not extract_path:
                return False
            
            # Clean up zip file
            filepath.unlink()
        
        return True
    
    def download_all(self):
        """Download all required models"""
        print("Starting model download...")
        print(f"Models will be saved to: {self.models_dir.absolute()}")
        
        success_count = 0
        total_models = len(self.models)
        
        for model_name in self.models:
            print(f"\n--- Downloading {model_name} ---")
            if self.download_model(model_name):
                success_count += 1
        
        print(f"\n--- Download Summary ---")
        print(f"Successfully downloaded: {success_count}/{total_models} models")
        
        if success_count == total_models:
            print("✓ All models downloaded successfully!")
            return True
        else:
            print("✗ Some models failed to download")
            return False
    
    def setup_tts_models(self):
        """Setup Coqui TTS models"""
        print("\n--- Setting up TTS models ---")
        print("TTS models will be downloaded automatically on first use")
        print("This may take some time depending on your internet connection")
        return True


def main():
    parser = argparse.ArgumentParser(description="Download models for Voice Bot")
    parser.add_argument("--model", help="Download specific model (vosk_en, vosk_hi, whisper)")
    parser.add_argument("--all", action="store_true", help="Download all models")
    parser.add_argument("--models-dir", default="models", help="Directory to save models")
    
    args = parser.parse_args()
    
    downloader = ModelDownloader(args.models_dir)
    
    if args.model:
        success = downloader.download_model(args.model)
        sys.exit(0 if success else 1)
    elif args.all:
        success = downloader.download_all()
        downloader.setup_tts_models()
        sys.exit(0 if success else 1)
    else:
        print("Please specify --model <name> or --all")
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()

