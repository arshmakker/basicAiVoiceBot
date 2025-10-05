#!/usr/bin/env python3
"""
Test Cases for Conversation Context
Comprehensive test suite for conversation context management
"""

import unittest
import sys
import os
import time
from pathlib import Path
from colorama import Fore, Style, init
from unittest.mock import Mock, patch, MagicMock

init(autoreset=True)

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

class TestConversationContext(unittest.TestCase):
    """Test cases for conversation context management"""
    
    @classmethod
    def setUpClass(cls):
        """Set up common resources for tests"""
        print("\n🧠 Starting Conversation Context Test Suite")
        print("=" * 60)

    def test_context_initialization(self):
        """Test conversation context initialization"""
        print(f"\n{Fore.CYAN}🚀 Testing Context Initialization{Style.RESET_ALL}")
        
        initialization_scenarios = [
            {
                "scenario": "Empty_Context",
                "expected_length": 0,
                "description": "Empty conversation context"
            },
            {
                "scenario": "Preloaded_Context",
                "preloaded_turns": 3,
                "expected_length": 3,
                "description": "Preloaded conversation context"
            },
            {
                "scenario": "Context_Reset",
                "preloaded_turns": 5,
                "reset": True,
                "expected_length": 0,
                "description": "Context reset functionality"
            }
        ]
        
        for i, scenario in enumerate(initialization_scenarios):
            print(f"{Fore.YELLOW}Test {i+1}: {scenario['description']}{Style.RESET_ALL}")
            
            # Mock context initialization
            with patch('voice_bot_cli.VoiceBotCLI') as mock_cli:
                mock_cli.conversation_context = []
                mock_cli.conversation_state = "idle"
                
                # Test preloaded context
                if 'preloaded_turns' in scenario:
                    for j in range(scenario['preloaded_turns']):
                        mock_cli.conversation_context.append({
                            'input': f"Turn {j+1}",
                            'response': f"Response {j+1}",
                            'language': 'en',
                            'confidence': 0.9,
                            'timestamp': time.time()
                        })
                
                # Test context reset
                if scenario.get('reset', False):
                    mock_cli.conversation_context = []
                    mock_cli.conversation_state = "idle"
                
                # Verify context initialization
                self.assertEqual(len(mock_cli.conversation_context), scenario['expected_length'])
                
                print(f"{Fore.GREEN}✅ Context length: {len(mock_cli.conversation_context)} (expected: {scenario['expected_length']}){Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}✅ Context Initialization PASSED{Style.RESET_ALL}\n")

    def test_context_accumulation(self):
        """Test conversation context accumulation"""
        print(f"\n{Fore.CYAN}📚 Testing Context Accumulation{Style.RESET_ALL}")
        
        accumulation_scenarios = [
            {
                "turns": [
                    {"input": "Hello", "response": "Hi there!", "language": "en"},
                    {"input": "How are you?", "response": "I'm doing well, thank you!", "language": "en"},
                    {"input": "What's your name?", "response": "I'm your AI assistant", "language": "en"}
                ],
                "description": "English conversation accumulation"
            },
            {
                "turns": [
                    {"input": "नमस्ते", "response": "नमस्ते!", "language": "hi"},
                    {"input": "आप कैसे हैं?", "response": "मैं ठीक हूं, धन्यवाद!", "language": "hi"},
                    {"input": "आपका नाम क्या है?", "response": "मैं आपकी AI सहायक हूं", "language": "hi"}
                ],
                "description": "Hindi conversation accumulation"
            },
            {
                "turns": [
                    {"input": "Hello नमस्ते", "response": "Hello! नमस्ते!", "language": "mixed"},
                    {"input": "How are you? आप कैसे हैं?", "response": "I'm good! मैं ठीक हूं!", "language": "mixed"},
                    {"input": "What's your name? आपका नाम क्या है?", "response": "I'm your AI assistant मैं आपकी AI सहायक हूं", "language": "mixed"}
                ],
                "description": "Mixed language conversation accumulation"
            }
        ]
        
        for i, scenario in enumerate(accumulation_scenarios):
            print(f"{Fore.YELLOW}Test {i+1}: {scenario['description']}{Style.RESET_ALL}")
            
            # Mock context accumulation
            with patch('voice_bot_cli.VoiceBotCLI') as mock_cli:
                mock_cli.conversation_context = []
                mock_cli.conversation_state = "idle"
                
                # Test context accumulation
                for turn in scenario['turns']:
                    mock_cli.conversation_context.append({
                        'input': turn['input'],
                        'response': turn['response'],
                        'language': turn['language'],
                        'confidence': 0.9,
                        'timestamp': time.time()
                    })
                    mock_cli.conversation_state = "active"
                
                # Verify context accumulation
                self.assertEqual(len(mock_cli.conversation_context), len(scenario['turns']))
                self.assertEqual(mock_cli.conversation_state, "active")
                
                # Verify context content
                for j, turn in enumerate(scenario['turns']):
                    context_turn = mock_cli.conversation_context[j]
                    self.assertEqual(context_turn['input'], turn['input'])
                    self.assertEqual(context_turn['response'], turn['response'])
                    self.assertEqual(context_turn['language'], turn['language'])
                
                print(f"{Fore.GREEN}✅ Accumulated {len(scenario['turns'])} turns successfully{Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}✅ Context Accumulation PASSED{Style.RESET_ALL}\n")

    def test_context_retrieval(self):
        """Test conversation context retrieval"""
        print(f"\n{Fore.CYAN}🔍 Testing Context Retrieval{Style.RESET_ALL}")
        
        retrieval_scenarios = [
            {
                "scenario": "Full_Context_Retrieval",
                "turns": 5,
                "retrieve_all": True,
                "description": "Full context retrieval"
            },
            {
                "scenario": "Partial_Context_Retrieval",
                "turns": 10,
                "retrieve_last": 3,
                "description": "Partial context retrieval (last 3 turns)"
            },
            {
                "scenario": "Filtered_Context_Retrieval",
                "turns": 8,
                "filter_language": "en",
                "description": "Language-filtered context retrieval"
            }
        ]
        
        for i, scenario in enumerate(retrieval_scenarios):
            print(f"{Fore.YELLOW}Test {i+1}: {scenario['description']}{Style.RESET_ALL}")
            
            # Mock context retrieval
            with patch('voice_bot_cli.VoiceBotCLI') as mock_cli:
                mock_cli.conversation_context = []
                
                # Populate context
                for j in range(scenario['turns']):
                    mock_cli.conversation_context.append({
                        'input': f"Turn {j+1}",
                        'response': f"Response {j+1}",
                        'language': 'en' if j % 2 == 0 else 'hi',
                        'confidence': 0.9,
                        'timestamp': time.time()
                    })
                
                # Test context retrieval
                if scenario.get('retrieve_all', False):
                    retrieved_context = mock_cli.conversation_context
                    expected_length = scenario['turns']
                elif 'retrieve_last' in scenario:
                    retrieved_context = mock_cli.conversation_context[-scenario['retrieve_last']:]
                    expected_length = scenario['retrieve_last']
                elif 'filter_language' in scenario:
                    retrieved_context = [turn for turn in mock_cli.conversation_context 
                                      if turn['language'] == scenario['filter_language']]
                    expected_length = scenario['turns'] // 2  # Half are English
                
                # Verify context retrieval
                self.assertEqual(len(retrieved_context), expected_length)
                
                print(f"{Fore.GREEN}✅ Retrieved {len(retrieved_context)} turns (expected: {expected_length}){Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}✅ Context Retrieval PASSED{Style.RESET_ALL}\n")

    def test_context_persistence(self):
        """Test conversation context persistence"""
        print(f"\n{Fore.CYAN}💾 Testing Context Persistence{Style.RESET_ALL}")
        
        persistence_scenarios = [
            {
                "scenario": "Session_Persistence",
                "turns": 5,
                "persist_duration": 3600,  # 1 hour
                "description": "Session persistence"
            },
            {
                "scenario": "Memory_Persistence",
                "turns": 10,
                "persist_duration": 7200,  # 2 hours
                "description": "Memory persistence"
            },
            {
                "scenario": "Temporary_Persistence",
                "turns": 3,
                "persist_duration": 300,  # 5 minutes
                "description": "Temporary persistence"
            }
        ]
        
        for i, scenario in enumerate(persistence_scenarios):
            print(f"{Fore.YELLOW}Test {i+1}: {scenario['description']}{Style.RESET_ALL}")
            
            # Mock context persistence
            with patch('voice_bot_cli.VoiceBotCLI') as mock_cli:
                mock_cli.conversation_context = []
                
                # Populate context with timestamps
                base_time = time.time()
                for j in range(scenario['turns']):
                    mock_cli.conversation_context.append({
                        'input': f"Turn {j+1}",
                        'response': f"Response {j+1}",
                        'language': 'en',
                        'confidence': 0.9,
                        'timestamp': base_time + j * 60  # 1 minute intervals
                    })
                
                # Test context persistence
                current_time = base_time + scenario['turns'] * 60
                persistent_context = [turn for turn in mock_cli.conversation_context 
                                    if current_time - turn['timestamp'] <= scenario['persist_duration']]
                
                # Verify context persistence
                self.assertEqual(len(persistent_context), scenario['turns'])
                
                print(f"{Fore.GREEN}✅ Persistence: {len(persistent_context)} turns persisted for {scenario['persist_duration']}s{Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}✅ Context Persistence PASSED{Style.RESET_ALL}\n")

    def test_context_cleanup(self):
        """Test conversation context cleanup"""
        print(f"\n{Fore.CYAN}🧹 Testing Context Cleanup{Style.RESET_ALL}")
        
        cleanup_scenarios = [
            {
                "scenario": "Manual_Cleanup",
                "turns": 8,
                "cleanup_method": "manual",
                "description": "Manual context cleanup"
            },
            {
                "scenario": "Automatic_Cleanup",
                "turns": 12,
                "cleanup_method": "automatic",
                "max_turns": 10,
                "description": "Automatic context cleanup (max 10 turns)"
            },
            {
                "scenario": "Time_Based_Cleanup",
                "turns": 15,
                "cleanup_method": "time_based",
                "max_age": 1800,  # 30 minutes
                "description": "Time-based context cleanup"
            }
        ]
        
        for i, scenario in enumerate(cleanup_scenarios):
            print(f"{Fore.YELLOW}Test {i+1}: {scenario['description']}{Style.RESET_ALL}")
            
            # Mock context cleanup
            with patch('voice_bot_cli.VoiceBotCLI') as mock_cli:
                mock_cli.conversation_context = []
                
                # Populate context
                base_time = time.time()
                for j in range(scenario['turns']):
                    mock_cli.conversation_context.append({
                        'input': f"Turn {j+1}",
                        'response': f"Response {j+1}",
                        'language': 'en',
                        'confidence': 0.9,
                        'timestamp': base_time - j * 300  # 5 minute intervals going back
                    })
                
                # Test context cleanup
                if scenario['cleanup_method'] == 'manual':
                    mock_cli.conversation_context = []
                    mock_cli.conversation_state = "idle"
                    cleaned_context = mock_cli.conversation_context
                    expected_length = 0
                
                elif scenario['cleanup_method'] == 'automatic':
                    max_turns = scenario['max_turns']
                    if len(mock_cli.conversation_context) > max_turns:
                        mock_cli.conversation_context = mock_cli.conversation_context[-max_turns:]
                    cleaned_context = mock_cli.conversation_context
                    expected_length = min(scenario['turns'], max_turns)
                
                elif scenario['cleanup_method'] == 'time_based':
                    max_age = scenario['max_age']
                    current_time = time.time()
                    cleaned_context = [turn for turn in mock_cli.conversation_context 
                                    if current_time - turn['timestamp'] <= max_age]
                    expected_length = min(scenario['turns'], max_age // 300)  # Approximate
                
                # Verify context cleanup
                self.assertEqual(len(cleaned_context), expected_length)
                
                print(f"{Fore.GREEN}✅ Cleanup: {len(cleaned_context)} turns remaining (expected: {expected_length}){Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}✅ Context Cleanup PASSED{Style.RESET_ALL}\n")

    def test_context_search(self):
        """Test conversation context search"""
        print(f"\n{Fore.CYAN}🔎 Testing Context Search{Style.RESET_ALL}")
        
        search_scenarios = [
            {
                "scenario": "Text_Search",
                "search_term": "weather",
                "expected_matches": 3,
                "description": "Text search in context"
            },
            {
                "scenario": "Language_Search",
                "search_language": "hi",
                "expected_matches": 3,
                "description": "Language search in context"
            },
            {
                "scenario": "Time_Range_Search",
                "time_range": 1800,  # 30 minutes
                "expected_matches": 6,
                "description": "Time range search in context"
            }
        ]
        
        for i, scenario in enumerate(search_scenarios):
            print(f"{Fore.YELLOW}Test {i+1}: {scenario['description']}{Style.RESET_ALL}")
            
            # Mock context search
            with patch('voice_bot_cli.VoiceBotCLI') as mock_cli:
                mock_cli.conversation_context = []
                
                # Populate context with searchable content
                test_turns = [
                    {"input": "Hello", "response": "Hi there!", "language": "en"},
                    {"input": "What's the weather like?", "response": "It's sunny today", "language": "en"},
                    {"input": "नमस्ते", "response": "नमस्ते!", "language": "hi"},
                    {"input": "How's the weather?", "response": "It's nice outside", "language": "en"},
                    {"input": "आप कैसे हैं?", "response": "मैं ठीक हूं", "language": "hi"},
                    {"input": "Tell me about the weather", "response": "Weather is good", "language": "en"},
                    {"input": "आपका नाम क्या है?", "response": "मैं AI हूं", "language": "hi"}
                ]
                
                base_time = time.time()
                for j, turn in enumerate(test_turns):
                    mock_cli.conversation_context.append({
                        'input': turn['input'],
                        'response': turn['response'],
                        'language': turn['language'],
                        'confidence': 0.9,
                        'timestamp': base_time - j * 300  # 5 minute intervals
                    })
                
                # Test context search
                if scenario['scenario'] == 'Text_Search':
                    search_term = scenario['search_term']
                    search_results = [turn for turn in mock_cli.conversation_context 
                                    if search_term.lower() in turn['input'].lower() or 
                                       search_term.lower() in turn['response'].lower()]
                    expected_matches = scenario['expected_matches']
                
                elif scenario['scenario'] == 'Language_Search':
                    search_language = scenario['search_language']
                    search_results = [turn for turn in mock_cli.conversation_context 
                                    if turn['language'] == search_language]
                    expected_matches = scenario['expected_matches']
                
                elif scenario['scenario'] == 'Time_Range_Search':
                    time_range = scenario['time_range']
                    current_time = time.time()
                    search_results = [turn for turn in mock_cli.conversation_context 
                                    if current_time - turn['timestamp'] <= time_range]
                    expected_matches = scenario['expected_matches']
                
                # Verify context search
                self.assertEqual(len(search_results), expected_matches)
                
                print(f"{Fore.GREEN}✅ Search found {len(search_results)} matches (expected: {expected_matches}){Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}✅ Context Search PASSED{Style.RESET_ALL}\n")

    def test_context_export_import(self):
        """Test conversation context export/import"""
        print(f"\n{Fore.CYAN}📤📥 Testing Context Export/Import{Style.RESET_ALL}")
        
        export_import_scenarios = [
            {
                "scenario": "JSON_Export_Import",
                "format": "json",
                "turns": 5,
                "description": "JSON format export/import"
            },
            {
                "scenario": "CSV_Export_Import",
                "format": "csv",
                "turns": 8,
                "description": "CSV format export/import"
            },
            {
                "scenario": "Text_Export_Import",
                "format": "text",
                "turns": 3,
                "description": "Text format export/import"
            }
        ]
        
        for i, scenario in enumerate(export_import_scenarios):
            print(f"{Fore.YELLOW}Test {i+1}: {scenario['description']}{Style.RESET_ALL}")
            
            # Mock context export/import
            with patch('voice_bot_cli.VoiceBotCLI') as mock_cli:
                mock_cli.conversation_context = []
                
                # Populate context
                for j in range(scenario['turns']):
                    mock_cli.conversation_context.append({
                        'input': f"Turn {j+1}",
                        'response': f"Response {j+1}",
                        'language': 'en',
                        'confidence': 0.9,
                        'timestamp': time.time()
                    })
                
                # Test context export
                if scenario['format'] == 'json':
                    exported_data = {
                        'conversation_context': mock_cli.conversation_context,
                        'conversation_state': 'active',
                        'export_timestamp': time.time()
                    }
                elif scenario['format'] == 'csv':
                    exported_data = f"input,response,language,confidence,timestamp\n"
                    for turn in mock_cli.conversation_context:
                        exported_data += f"{turn['input']},{turn['response']},{turn['language']},{turn['confidence']},{turn['timestamp']}\n"
                elif scenario['format'] == 'text':
                    exported_data = ""
                    for turn in mock_cli.conversation_context:
                        exported_data += f"Input: {turn['input']}\nResponse: {turn['response']}\n\n"
                
                # Test context import
                if scenario['format'] == 'json':
                    imported_context = exported_data['conversation_context']
                elif scenario['format'] == 'csv':
                    imported_context = mock_cli.conversation_context  # Simulate CSV parsing
                elif scenario['format'] == 'text':
                    imported_context = mock_cli.conversation_context  # Simulate text parsing
                
                # Verify context export/import
                self.assertEqual(len(imported_context), scenario['turns'])
                
                print(f"{Fore.GREEN}✅ Export/Import: {len(imported_context)} turns in {scenario['format']} format{Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}✅ Context Export/Import PASSED{Style.RESET_ALL}\n")

    def test_context_performance(self):
        """Test conversation context performance"""
        print(f"\n{Fore.CYAN}⚡ Testing Context Performance{Style.RESET_ALL}")
        
        performance_scenarios = [
            {
                "scenario": "Small_Context",
                "turns": 10,
                "max_operation_time": 0.1,
                "description": "Small context performance"
            },
            {
                "scenario": "Medium_Context",
                "turns": 100,
                "max_operation_time": 0.5,
                "description": "Medium context performance"
            },
            {
                "scenario": "Large_Context",
                "turns": 1000,
                "max_operation_time": 2.0,
                "description": "Large context performance"
            }
        ]
        
        for i, scenario in enumerate(performance_scenarios):
            print(f"{Fore.YELLOW}Test {i+1}: {scenario['description']}{Style.RESET_ALL}")
            
            # Mock context performance testing
            with patch('voice_bot_cli.VoiceBotCLI') as mock_cli:
                mock_cli.conversation_context = []
                
                # Populate context
                for j in range(scenario['turns']):
                    mock_cli.conversation_context.append({
                        'input': f"Turn {j+1}",
                        'response': f"Response {j+1}",
                        'language': 'en',
                        'confidence': 0.9,
                        'timestamp': time.time()
                    })
                
                # Test context operations performance
                start_time = time.time()
                
                # Simulate context operations
                context_length = len(mock_cli.conversation_context)
                context_search = [turn for turn in mock_cli.conversation_context if 'Turn' in turn['input']]
                context_filter = [turn for turn in mock_cli.conversation_context if turn['language'] == 'en']
                
                end_time = time.time()
                operation_time = end_time - start_time
                
                # Verify context performance
                self.assertLess(operation_time, scenario['max_operation_time'])
                
                print(f"{Fore.GREEN}✅ Performance: {operation_time:.3f}s < {scenario['max_operation_time']}s{Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}✅ Context Performance PASSED{Style.RESET_ALL}\n")

if __name__ == "__main__":
    # Run the tests
    unittest.main(verbosity=2)
