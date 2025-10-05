#!/usr/bin/env python3
"""
Performance Benchmark for Dialog System Optimization
Test script to compare regular vs optimized dialog system performance
"""

import time
import sys
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

from voice_bot.dialog_system import DialogManager
from voice_bot.dialog_optimization import OptimizedDialogManager, benchmark_dialog_performance

def run_performance_benchmark():
    """Run comprehensive performance benchmark"""
    print("🚀 Starting Dialog System Performance Benchmark")
    print("=" * 60)
    
    # Test inputs
    test_inputs = [
        ("Hello, how are you?", "en"),
        ("What's the weather like today?", "en"),
        ("Can you help me with something?", "en"),
        ("Thank you very much", "en"),
        ("Goodbye", "en"),
        ("नमस्ते, आप कैसे हैं?", "hi"),
        ("आज मौसम कैसा है?", "hi"),
        ("क्या आप मेरी मदद कर सकते हैं?", "hi"),
        ("बहुत धन्यवाद", "hi"),
        ("अलविदा", "hi"),
        ("Hello नमस्ते", "mixed"),
        ("How are you? आप कैसे हैं?", "mixed"),
        ("What's your name? आपका नाम क्या है?", "mixed")
    ]
    
    iterations = 100
    
    print(f"📊 Test Configuration:")
    print(f"  Test inputs: {len(test_inputs)}")
    print(f"  Iterations: {iterations}")
    print(f"  Total requests: {iterations * len(test_inputs)}")
    print()
    
    # Test regular dialog manager
    print("🔍 Testing Regular Dialog Manager...")
    regular_manager = DialogManager()
    
    start_time = time.time()
    for _ in range(iterations):
        for text, language in test_inputs:
            regular_manager.process_input(text, language)
    regular_time = time.time() - start_time
    
    regular_stats = {
        "total_time": regular_time,
        "avg_time_per_request": regular_time / (iterations * len(test_inputs)),
        "requests_per_second": (iterations * len(test_inputs)) / regular_time,
        "total_requests": iterations * len(test_inputs)
    }
    
    print(f"✅ Regular Dialog Manager Results:")
    print(f"  Total time: {regular_stats['total_time']:.3f}s")
    print(f"  Avg time per request: {regular_stats['avg_time_per_request']:.3f}s")
    print(f"  Requests per second: {regular_stats['requests_per_second']:.1f}")
    print()
    
    # Test optimized dialog manager
    print("⚡ Testing Optimized Dialog Manager...")
    optimized_manager = OptimizedDialogManager()
    
    start_time = time.time()
    for _ in range(iterations):
        for text, language in test_inputs:
            optimized_manager.process_input(text, language)
    optimized_time = time.time() - start_time
    
    optimized_stats = {
        "total_time": optimized_time,
        "avg_time_per_request": optimized_time / (iterations * len(test_inputs)),
        "requests_per_second": (iterations * len(test_inputs)) / optimized_time,
        "total_requests": iterations * len(test_inputs)
    }
    
    print(f"✅ Optimized Dialog Manager Results:")
    print(f"  Total time: {optimized_stats['total_time']:.3f}s")
    print(f"  Avg time per request: {optimized_stats['avg_time_per_request']:.3f}s")
    print(f"  Requests per second: {optimized_stats['requests_per_second']:.1f}")
    print()
    
    # Calculate performance improvements
    time_improvement = (regular_time - optimized_time) / regular_time * 100
    speed_improvement = (optimized_stats['requests_per_second'] - regular_stats['requests_per_second']) / regular_stats['requests_per_second'] * 100
    
    print("📈 Performance Improvements:")
    print(f"  Time reduction: {time_improvement:.1f}%")
    print(f"  Speed increase: {speed_improvement:.1f}%")
    print(f"  Speedup factor: {regular_time / optimized_time:.2f}x")
    print()
    
    # Test cache effectiveness
    print("🗄️ Testing Cache Effectiveness...")
    
    # Test with repeated inputs (should benefit from caching)
    repeated_inputs = [
        ("Hello, how are you?", "en"),
        ("Hello, how are you?", "en"),  # Repeated
        ("What's the weather like?", "en"),
        ("What's the weather like?", "en"),  # Repeated
        ("Thank you", "en"),
        ("Thank you", "en")  # Repeated
    ]
    
    # Test regular manager with repeated inputs
    start_time = time.time()
    for _ in range(50):
        for text, language in repeated_inputs:
            regular_manager.process_input(text, language)
    regular_repeated_time = time.time() - start_time
    
    # Test optimized manager with repeated inputs
    start_time = time.time()
    for _ in range(50):
        for text, language in repeated_inputs:
            optimized_manager.process_input(text, language)
    optimized_repeated_time = time.time() - start_time
    
    cache_improvement = (regular_repeated_time - optimized_repeated_time) / regular_repeated_time * 100
    
    print(f"✅ Cache Effectiveness Results:")
    print(f"  Regular manager (repeated): {regular_repeated_time:.3f}s")
    print(f"  Optimized manager (repeated): {optimized_repeated_time:.3f}s")
    print(f"  Cache improvement: {cache_improvement:.1f}%")
    print()
    
    # Test batch processing
    print("📦 Testing Batch Processing...")
    
    batch_inputs = [
        ("Hello", "en"),
        ("How are you?", "en"),
        ("What's your name?", "en"),
        ("Thank you", "en"),
        ("Goodbye", "en")
    ]
    
    # Test individual processing
    start_time = time.time()
    for _ in range(20):
        for text, language in batch_inputs:
            optimized_manager.process_input(text, language)
    individual_time = time.time() - start_time
    
    # Test batch processing
    start_time = time.time()
    for _ in range(20):
        optimized_manager.process_batch(batch_inputs)
    batch_time = time.time() - start_time
    
    batch_improvement = (individual_time - batch_time) / individual_time * 100
    
    print(f"✅ Batch Processing Results:")
    print(f"  Individual processing: {individual_time:.3f}s")
    print(f"  Batch processing: {batch_time:.3f}s")
    print(f"  Batch improvement: {batch_improvement:.1f}%")
    print()
    
    # Get detailed performance stats
    print("📊 Detailed Performance Statistics:")
    perf_stats = optimized_manager.get_performance_stats()
    print(f"  Average processing time: {perf_stats['avg_time']:.3f}s")
    print(f"  Max processing time: {perf_stats['max_time']:.3f}s")
    print(f"  Min processing time: {perf_stats['min_time']:.3f}s")
    print(f"  Total requests processed: {perf_stats['total_requests']}")
    print()
    
    # Summary
    print("🎯 Performance Optimization Summary:")
    print(f"  ✅ Overall speedup: {regular_time / optimized_time:.2f}x")
    print(f"  ✅ Cache effectiveness: {cache_improvement:.1f}% improvement")
    print(f"  ✅ Batch processing: {batch_improvement:.1f}% improvement")
    print(f"  ✅ Average response time: {perf_stats['avg_time']:.3f}s")
    print(f"  ✅ Requests per second: {optimized_stats['requests_per_second']:.1f}")
    print()
    
    print("🚀 Performance benchmark completed successfully!")

if __name__ == "__main__":
    run_performance_benchmark()
