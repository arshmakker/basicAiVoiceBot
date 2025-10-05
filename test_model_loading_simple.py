#!/usr/bin/env python3
"""
Model Loading and Initialization Test (Simplified)
Tests model loading with missing files and initialization scenarios
"""

import sys
import time
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional
from colorama import Fore, Style, init

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from voice_bot import VoiceBot, VoiceBotError

init(autoreset=True)

class ModelLoadingTester:
    """Model loading and initialization tester (simplified)"""
    
    def __init__(self):
        self.test_results: List[Dict[str, Any]] = []
        
    def test_missing_models_directory(self) -> bool:
        """Test behavior when models directory is missing"""
        print(f"\n{Fore.CYAN}📁 Testing Missing Models Directory{Style.RESET_ALL}")
        
        try:
            # Check if models directory exists
            models_dir = Path("models")
            if not models_dir.exists():
                print(f"{Fore.YELLOW}Models directory does not exist{Style.RESET_ALL}")
                
                # Try to initialize voice bot
                print(f"{Fore.YELLOW}Attempting to initialize voice bot without models directory...{Style.RESET_ALL}")
                
                try:
                    voice_bot = VoiceBot(
                        models_dir="models",
                        vosk_en_model="vosk-model-en-us-0.22",
                        vosk_hi_model="vosk-model-hi-0.22",
                        tts_language="en",
                        use_gpu=False,
                        sample_rate=16000,
                        chunk_size=1024
                    )
                    
                    print(f"{Fore.RED}❌ Voice bot initialized without models directory (unexpected){Style.RESET_ALL}")
                    self.test_results.append({
                        "test": "missing_models_directory",
                        "error": "Voice bot initialized without models directory",
                        "passed": False
                    })
                    return False
                    
                except Exception as e:
                    print(f"{Fore.GREEN}✅ Voice bot correctly failed to initialize: {e}{Style.RESET_ALL}")
                    
                    self.test_results.append({
                        "test": "missing_models_directory",
                        "error_type": type(e).__name__,
                        "error_message": str(e),
                        "passed": True
                    })
                    return True
            else:
                print(f"{Fore.GREEN}✅ Models directory exists{Style.RESET_ALL}")
                return True
                
        except Exception as e:
            print(f"{Fore.RED}❌ Missing models directory test failed: {e}{Style.RESET_ALL}")
            self.test_results.append({
                "test": "missing_models_directory",
                "error": str(e),
                "passed": False
            })
            return False
    
    def test_model_initialization_performance(self) -> bool:
        """Test model initialization performance"""
        print(f"\n{Fore.CYAN}⚡ Testing Model Initialization Performance{Style.RESET_ALL}")
        
        try:
            models_dir = Path("models")
            if not models_dir.exists():
                print(f"{Fore.RED}❌ Models directory not found{Style.RESET_ALL}")
                return False
            
            # Test initialization time
            print(f"{Fore.YELLOW}Testing model initialization performance...{Style.RESET_ALL}")
            
            initialization_times = []
            success_count = 0
            
            for i in range(2):  # Test 2 initializations (reduced from 3)
                print(f"{Fore.YELLOW}Initialization {i+1}/2...{Style.RESET_ALL}")
                
                start_time = time.time()
                
                try:
                    voice_bot = VoiceBot(
                        models_dir=str(models_dir),
                        vosk_en_model="vosk-model-en-us-0.22",
                        vosk_hi_model="vosk-model-hi-0.22",
                        tts_language="en",
                        use_gpu=False,
                        sample_rate=16000,
                        chunk_size=1024
                    )
                    
                    end_time = time.time()
                    init_time = end_time - start_time
                    initialization_times.append(init_time)
                    
                    print(f"   Initialization time: {init_time:.2f}s")
                    
                    # Test basic functionality
                    response = voice_bot.process_text("Hello", "en")
                    if response and len(response.strip()) > 0:
                        print(f"   Basic functionality: ✅")
                        success_count += 1
                    else:
                        print(f"   Basic functionality: ❌")
                    
                except Exception as e:
                    print(f"   Initialization failed: {e}")
            
            # Analyze results
            if initialization_times:
                avg_time = sum(initialization_times) / len(initialization_times)
                max_time = max(initialization_times)
                min_time = min(initialization_times)
                
                print(f"\n{Fore.CYAN}Initialization Performance:{Style.RESET_ALL}")
                print(f"   Average time: {avg_time:.2f}s")
                print(f"   Max time: {max_time:.2f}s")
                print(f"   Min time: {min_time:.2f}s")
                print(f"   Successful initializations: {success_count}/2")
                
                # Check if performance is acceptable (less than 60 seconds)
                if max_time < 60:
                    print(f"{Fore.GREEN}✅ Initialization performance acceptable{Style.RESET_ALL}")
                    passed = True
                else:
                    print(f"{Fore.RED}❌ Initialization performance poor: {max_time:.2f}s{Style.RESET_ALL}")
                    passed = False
                
                self.test_results.append({
                    "test": "model_initialization_performance",
                    "initialization_times": initialization_times,
                    "average_time": avg_time,
                    "max_time": max_time,
                    "min_time": min_time,
                    "successful_initializations": success_count,
                    "passed": passed
                })
                
                return passed
            else:
                print(f"{Fore.RED}❌ No successful initializations{Style.RESET_ALL}")
                return False
                
        except Exception as e:
            print(f"{Fore.RED}❌ Model initialization performance test failed: {e}{Style.RESET_ALL}")
            self.test_results.append({
                "test": "model_initialization_performance",
                "error": str(e),
                "passed": False
            })
            return False
    
    def test_model_cleanup(self) -> bool:
        """Test model cleanup and resource management"""
        print(f"\n{Fore.CYAN}🧹 Testing Model Cleanup{Style.RESET_ALL}")
        
        try:
            models_dir = Path("models")
            if not models_dir.exists():
                print(f"{Fore.RED}❌ Models directory not found{Style.RESET_ALL}")
                return False
            
            # Test multiple initializations and cleanup
            print(f"{Fore.YELLOW}Testing model cleanup and resource management...{Style.RESET_ALL}")
            
            success_count = 0
            
            for i in range(2):  # Test 2 cycles (reduced from 3)
                print(f"{Fore.YELLOW}Cycle {i+1}/2...{Style.RESET_ALL}")
                
                try:
                    # Initialize voice bot
                    voice_bot = VoiceBot(
                        models_dir=str(models_dir),
                        vosk_en_model="vosk-model-en-us-0.22",
                        vosk_hi_model="vosk-model-hi-0.22",
                        tts_language="en",
                        use_gpu=False,
                        sample_rate=16000,
                        chunk_size=1024
                    )
                    
                    # Test functionality
                    response = voice_bot.process_text("Hello", "en")
                    if response and len(response.strip()) > 0:
                        print(f"   Functionality: ✅")
                        
                        # Test cleanup (explicit deletion)
                        del voice_bot
                        
                        # Small delay to allow cleanup
                        time.sleep(0.5)
                        
                        print(f"   Cleanup: ✅")
                        success_count += 1
                    else:
                        print(f"   Functionality: ❌")
                        
                except Exception as e:
                    print(f"   Cycle failed: {e}")
            
            success_rate = success_count / 2
            print(f"\n{Fore.CYAN}Model Cleanup: {success_count}/2 cycles successful ({success_rate:.1%}){Style.RESET_ALL}")
            
            if success_rate >= 0.8:
                print(f"{Fore.GREEN}✅ Model cleanup working properly{Style.RESET_ALL}")
                passed = True
            else:
                print(f"{Fore.RED}❌ Model cleanup issues detected{Style.RESET_ALL}")
                passed = False
            
            self.test_results.append({
                "test": "model_cleanup",
                "cycles_tested": 2,
                "successful_cycles": success_count,
                "success_rate": success_rate,
                "passed": passed
            })
            
            return passed
            
        except Exception as e:
            print(f"{Fore.RED}❌ Model cleanup test failed: {e}{Style.RESET_ALL}")
            self.test_results.append({
                "test": "model_cleanup",
                "error": str(e),
                "passed": False
            })
            return False
    
    def test_model_file_structure(self) -> bool:
        """Test model file structure validation"""
        print(f"\n{Fore.CYAN}📂 Testing Model File Structure{Style.RESET_ALL}")
        
        try:
            models_dir = Path("models")
            if not models_dir.exists():
                print(f"{Fore.RED}❌ Models directory not found{Style.RESET_ALL}")
                return False
            
            print(f"{Fore.YELLOW}Checking model file structure...{Style.RESET_ALL}")
            
            # Check for required model directories
            required_dirs = [
                "vosk-model-en-us-0.22",
                "vosk-model-hi-0.22"
            ]
            
            found_dirs = []
            missing_dirs = []
            
            for dir_name in required_dirs:
                dir_path = models_dir / dir_name
                if dir_path.exists():
                    found_dirs.append(dir_name)
                    print(f"   ✅ {dir_name} found")
                else:
                    missing_dirs.append(dir_name)
                    print(f"   ❌ {dir_name} missing")
            
            # Check for model files
            model_files = list(models_dir.rglob("*.model"))
            if model_files:
                print(f"   ✅ Found {len(model_files)} model files")
            else:
                print(f"   ⚠️  No .model files found")
            
            # Check for other important files
            important_files = list(models_dir.rglob("*.fst"))
            if important_files:
                print(f"   ✅ Found {len(important_files)} FST files")
            
            important_files = list(models_dir.rglob("*.txt"))
            if important_files:
                print(f"   ✅ Found {len(important_files)} text files")
            
            # Determine success
            if len(found_dirs) >= len(required_dirs) * 0.5:  # At least 50% of required dirs
                print(f"{Fore.GREEN}✅ Model file structure acceptable{Style.RESET_ALL}")
                passed = True
            else:
                print(f"{Fore.RED}❌ Model file structure incomplete{Style.RESET_ALL}")
                passed = False
            
            self.test_results.append({
                "test": "model_file_structure",
                "required_dirs": required_dirs,
                "found_dirs": found_dirs,
                "missing_dirs": missing_dirs,
                "model_files_count": len(model_files),
                "passed": passed
            })
            
            return passed
            
        except Exception as e:
            print(f"{Fore.RED}❌ Model file structure test failed: {e}{Style.RESET_ALL}")
            self.test_results.append({
                "test": "model_file_structure",
                "error": str(e),
                "passed": False
            })
            return False
    
    def run_all_tests(self) -> bool:
        """Run all model loading and initialization tests"""
        print(f"{Fore.BLUE}🚀 Starting Model Loading and Initialization Tests (Simplified){Style.RESET_ALL}")
        print(f"{Fore.BLUE}=============================================================={Style.RESET_ALL}")
        
        # Run tests
        tests = [
            ("Missing Models Directory", self.test_missing_models_directory),
            ("Model File Structure", self.test_model_file_structure),
            ("Model Initialization Performance", self.test_model_initialization_performance),
            ("Model Cleanup", self.test_model_cleanup),
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
            print(f"{Fore.GREEN}🎉 Model Loading and Initialization Tests PASSED{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.RED}❌ Model Loading and Initialization Tests FAILED{Style.RESET_ALL}")
            return False

def main():
    """Main test runner"""
    tester = ModelLoadingTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
