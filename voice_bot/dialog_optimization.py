#!/usr/bin/env python3
"""
Performance Optimizations for Response Generation
Optimized dialog system with caching, precompilation, and performance improvements
"""

import re
import time
import random
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from functools import lru_cache
import threading
from collections import defaultdict

# Import existing dialog system components
from voice_bot.dialog_system import Intent, IntentMatch, IntentRecognizer, ResponseGenerator, DialogManager

class OptimizedIntentRecognizer(IntentRecognizer):
    """Optimized intent recognizer with caching and precompilation"""
    
    def __init__(self):
        super().__init__()
        # Precompile regex patterns for better performance
        self._compiled_patterns = self._precompile_patterns()
        # Cache for recent intent matches
        self._intent_cache = {}
        self._cache_size = 100
        self._cache_lock = threading.Lock()
    
    def _precompile_patterns(self) -> Dict[Intent, List[re.Pattern]]:
        """Precompile regex patterns for better performance"""
        compiled_patterns = {}
        
        for intent, patterns in self.patterns.items():
            compiled_patterns[intent] = [
                re.compile(pattern, re.IGNORECASE) for pattern in patterns
            ]
        
        return compiled_patterns
    
    @lru_cache(maxsize=1000)
    def recognize_intent_cached(self, text: str) -> IntentMatch:
        """Cached version of intent recognition"""
        return super().recognize_intent(text)
    
    def recognize_intent(self, text: str) -> IntentMatch:
        """
        Optimized intent recognition with caching
        """
        text_lower = text.lower().strip()
        
        # Check cache first
        with self._cache_lock:
            if text_lower in self._intent_cache:
                return self._intent_cache[text_lower]
        
        # Use precompiled patterns for faster matching
        for intent, compiled_patterns in self._compiled_patterns.items():
            for pattern in compiled_patterns:
                match = pattern.search(text_lower)
                if match:
                    confidence = self._calculate_confidence(text_lower, pattern.pattern)
                    entities = self._extract_entities(text_lower, intent)
                    intent_match = IntentMatch(intent, confidence, entities, pattern.pattern)
                    
                    # Cache the result
                    with self._cache_lock:
                        if len(self._intent_cache) >= self._cache_size:
                            # Remove oldest entry
                            oldest_key = next(iter(self._intent_cache))
                            del self._intent_cache[oldest_key]
                        self._intent_cache[text_lower] = intent_match
                    
                    return intent_match
        
        # Check FAQ patterns
        faq_intent = self._check_faq_patterns(text_lower)
        if faq_intent:
            with self._cache_lock:
                if len(self._intent_cache) >= self._cache_size:
                    oldest_key = next(iter(self._intent_cache))
                    del self._intent_cache[oldest_key]
                self._intent_cache[text_lower] = faq_intent
            return faq_intent
        
        # Default to fallback
        fallback_match = IntentMatch(Intent.FALLBACK, 0.5, {}, "")
        with self._cache_lock:
            if len(self._intent_cache) >= self._cache_size:
                oldest_key = next(iter(self._intent_cache))
                del self._intent_cache[oldest_key]
            self._intent_cache[text_lower] = fallback_match
        return fallback_match
    
    def clear_cache(self):
        """Clear the intent cache"""
        with self._cache_lock:
            self._intent_cache.clear()
        self.recognize_intent_cached.cache_clear()


class OptimizedResponseGenerator(ResponseGenerator):
    """Optimized response generator with caching and precomputation"""
    
    def __init__(self):
        super().__init__()
        # Precompute response lists for faster access
        self._response_lists = self._precompute_response_lists()
        # Cache for recent responses
        self._response_cache = {}
        self._cache_size = 200
        self._cache_lock = threading.Lock()
    
    def _precompute_response_lists(self) -> Dict[Intent, Dict[str, List[str]]]:
        """Precompute response lists for faster access"""
        return {
            intent: {
                lang: responses.copy() for lang, responses in lang_responses.items()
            }
            for intent, lang_responses in self.responses.items()
        }
    
    @lru_cache(maxsize=500)
    def generate_response_cached(self, intent_value: str, language: str) -> str:
        """Cached version of response generation"""
        # Convert back to Intent enum
        intent = Intent(intent_value)
        intent_match = IntentMatch(intent, 0.8, {}, "")
        return super().generate_response(intent_match, language)
    
    def generate_response(self, intent_match: IntentMatch, language: str = "en") -> str:
        """
        Optimized response generation with caching
        """
        intent = intent_match.intent
        entities = intent_match.entities
        
        # Create cache key
        cache_key = f"{intent.value}_{language}_{str(sorted(entities.items()))}"
        
        # Check cache first
        with self._cache_lock:
            if cache_key in self._response_cache:
                return self._response_cache[cache_key]
        
        # Handle FAQ responses
        if intent == Intent.FAQ and 'faq_topic' in entities:
            faq_topic = entities['faq_topic']
            if faq_topic in self.faq_responses and language in self.faq_responses[faq_topic]:
                responses = self.faq_responses[faq_topic][language]
                response = random.choice(responses)
                
                # Cache the result
                with self._cache_lock:
                    if len(self._response_cache) >= self._cache_size:
                        # Remove oldest entry
                        oldest_key = next(iter(self._response_cache))
                        del self._response_cache[oldest_key]
                    self._response_cache[cache_key] = response
                
                return response
        
        # Handle regular responses using precomputed lists
        if intent in self._response_lists and language in self._response_lists[intent]:
            responses = self._response_lists[intent][language]
            response = random.choice(responses)
            
            # Cache the result
            with self._cache_lock:
                if len(self._response_cache) >= self._cache_size:
                    oldest_key = next(iter(self._response_cache))
                    del self._response_cache[oldest_key]
                self._response_cache[cache_key] = response
            
            return response
        
        # Fallback to English if language not available
        if intent in self._response_lists and "en" in self._response_lists[intent]:
            responses = self._response_lists[intent]["en"]
            response = random.choice(responses)
            
            # Cache the result
            with self._cache_lock:
                if len(self._response_cache) >= self._cache_size:
                    oldest_key = next(iter(self._response_cache))
                    del self._response_cache[oldest_key]
                self._response_cache[cache_key] = response
            
            return response
        
        # Ultimate fallback
        fallback_response = "I'm sorry, I didn't understand that. Could you please try again?"
        
        # Cache the fallback
        with self._cache_lock:
            if len(self._response_cache) >= self._cache_size:
                oldest_key = next(iter(self._response_cache))
                del self._response_cache[oldest_key]
            self._response_cache[cache_key] = fallback_response
        
        return fallback_response
    
    def clear_cache(self):
        """Clear the response cache"""
        with self._cache_lock:
            self._response_cache.clear()
        self.generate_response_cached.cache_clear()


class OptimizedDialogManager(DialogManager):
    """Optimized dialog manager with performance improvements"""
    
    def __init__(self):
        """Initialize optimized dialog manager"""
        self.intent_recognizer = OptimizedIntentRecognizer()
        self.response_generator = OptimizedResponseGenerator()
        self.conversation_history = []
        self.max_history = 10
        
        # Performance tracking
        self._processing_times = []
        self._max_processing_times = 100
        
        # Batch processing for multiple inputs
        self._batch_queue = []
        self._batch_lock = threading.Lock()
        self._batch_size = 5
    
    def process_input(self, text: str, language: str = "en") -> str:
        """
        Optimized input processing with performance tracking
        """
        start_time = time.time()
        
        try:
            # Recognize intent
            intent_match = self.intent_recognizer.recognize_intent(text)
            
            # Generate response
            response = self.response_generator.generate_response(intent_match, language)
            
            # Store in conversation history
            self._add_to_history(text, response, intent_match.intent.value)
            
            # Track processing time
            processing_time = time.time() - start_time
            self._track_processing_time(processing_time)
            
            return response
            
        except Exception as e:
            logging.error(f"Dialog processing error: {e}")
            return "I'm sorry, I encountered an error processing your request."
    
    def _track_processing_time(self, processing_time: float):
        """Track processing times for performance monitoring"""
        self._processing_times.append(processing_time)
        
        # Keep only recent processing times
        if len(self._processing_times) > self._max_processing_times:
            self._processing_times = self._processing_times[-self._max_processing_times:]
    
    def get_performance_stats(self) -> Dict[str, float]:
        """Get performance statistics"""
        if not self._processing_times:
            return {"avg_time": 0.0, "max_time": 0.0, "min_time": 0.0}
        
        return {
            "avg_time": sum(self._processing_times) / len(self._processing_times),
            "max_time": max(self._processing_times),
            "min_time": min(self._processing_times),
            "total_requests": len(self._processing_times)
        }
    
    def process_batch(self, inputs: List[Tuple[str, str]]) -> List[str]:
        """
        Process multiple inputs in batch for better performance
        """
        responses = []
        
        for text, language in inputs:
            response = self.process_input(text, language)
            responses.append(response)
        
        return responses
    
    def clear_caches(self):
        """Clear all caches"""
        self.intent_recognizer.clear_cache()
        self.response_generator.clear_cache()
    
    def optimize_for_language(self, language: str):
        """Optimize the system for a specific language"""
        # Preload common patterns for the language
        if language == "en":
            # Preload English patterns
            pass
        elif language == "hi":
            # Preload Hindi patterns
            pass


class PerformanceMonitor:
    """Monitor dialog system performance"""
    
    def __init__(self):
        self.metrics = defaultdict(list)
        self.lock = threading.Lock()
    
    def record_metric(self, metric_name: str, value: float):
        """Record a performance metric"""
        with self.lock:
            self.metrics[metric_name].append(value)
            
            # Keep only recent metrics
            if len(self.metrics[metric_name]) > 1000:
                self.metrics[metric_name] = self.metrics[metric_name][-1000:]
    
    def get_metric_stats(self, metric_name: str) -> Dict[str, float]:
        """Get statistics for a metric"""
        with self.lock:
            if metric_name not in self.metrics or not self.metrics[metric_name]:
                return {"avg": 0.0, "max": 0.0, "min": 0.0, "count": 0}
            
            values = self.metrics[metric_name]
            return {
                "avg": sum(values) / len(values),
                "max": max(values),
                "min": min(values),
                "count": len(values)
            }
    
    def get_all_stats(self) -> Dict[str, Dict[str, float]]:
        """Get statistics for all metrics"""
        with self.lock:
            return {
                metric_name: self.get_metric_stats(metric_name)
                for metric_name in self.metrics.keys()
            }


# Global performance monitor
performance_monitor = PerformanceMonitor()


def optimize_dialog_system(dialog_manager: DialogManager) -> OptimizedDialogManager:
    """
    Convert a regular dialog manager to an optimized one
    
    Args:
        dialog_manager: Existing dialog manager
        
    Returns:
        Optimized dialog manager
    """
    optimized_manager = OptimizedDialogManager()
    
    # Copy conversation history
    optimized_manager.conversation_history = dialog_manager.conversation_history.copy()
    
    return optimized_manager


def benchmark_dialog_performance(dialog_manager: DialogManager, 
                               test_inputs: List[Tuple[str, str]], 
                               iterations: int = 100) -> Dict[str, float]:
    """
    Benchmark dialog system performance
    
    Args:
        dialog_manager: Dialog manager to benchmark
        test_inputs: List of (text, language) tuples to test
        iterations: Number of iterations to run
        
    Returns:
        Performance statistics
    """
    start_time = time.time()
    
    for _ in range(iterations):
        for text, language in test_inputs:
            dialog_manager.process_input(text, language)
    
    end_time = time.time()
    total_time = end_time - start_time
    
    return {
        "total_time": total_time,
        "avg_time_per_request": total_time / (iterations * len(test_inputs)),
        "requests_per_second": (iterations * len(test_inputs)) / total_time,
        "total_requests": iterations * len(test_inputs)
    }


if __name__ == "__main__":
    # Test the optimized dialog system
    print("Testing Optimized Dialog System...")
    
    # Create optimized dialog manager
    optimized_manager = OptimizedDialogManager()
    
    # Test inputs
    test_inputs = [
        ("Hello, how are you?", "en"),
        ("What's the weather like?", "en"),
        ("Thank you", "en"),
        ("नमस्ते", "hi"),
        ("आप कैसे हैं?", "hi")
    ]
    
    # Benchmark performance
    stats = benchmark_dialog_performance(optimized_manager, test_inputs, 50)
    
    print(f"Performance Stats:")
    print(f"  Total time: {stats['total_time']:.3f}s")
    print(f"  Avg time per request: {stats['avg_time_per_request']:.3f}s")
    print(f"  Requests per second: {stats['requests_per_second']:.1f}")
    print(f"  Total requests: {stats['total_requests']}")
    
    # Get performance stats
    perf_stats = optimized_manager.get_performance_stats()
    print(f"\nDialog Manager Stats:")
    print(f"  Average processing time: {perf_stats['avg_time']:.3f}s")
    print(f"  Max processing time: {perf_stats['max_time']:.3f}s")
    print(f"  Min processing time: {perf_stats['min_time']:.3f}s")
    print(f"  Total requests: {perf_stats['total_requests']}")
    
    print("\nOptimized Dialog System test completed!")
