"""
Dialog System Module
Handles conversation logic, intent recognition, and response generation
"""

import re
import random
import logging
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum


class Intent(Enum):
    """Supported intents"""
    GREETING = "greeting"
    FAQ = "faq"
    SMALL_TALK = "small_talk"
    GOODBYE = "goodbye"
    HELP = "help"
    FALLBACK = "fallback"


@dataclass
class IntentMatch:
    """Represents an intent match result"""
    intent: Intent
    confidence: float
    entities: Dict[str, Any]
    matched_pattern: str


class DialogSystemError(Exception):
    """Custom exception for dialog system errors"""
    pass


class IntentRecognizer:
    """Recognizes user intents from text input"""
    
    def __init__(self):
        """Initialize intent recognizer with patterns"""
        self.patterns = self._initialize_patterns()
        self.faq_patterns = self._initialize_faq_patterns()
    
    def _initialize_patterns(self) -> Dict[Intent, List[str]]:
        """Initialize intent patterns for English and Hindi"""
        return {
            Intent.GREETING: [
                # English patterns
                r'\b(hi|hello|hey|good morning|good afternoon|good evening)\b',
                r'\b(how are you|how do you do)\b',
                r'\b(nice to meet you|pleased to meet you)\b',
                
                # Hindi patterns
                r'\b(नमस्ते|नमस्कार|हैलो|हाय|सुप्रभात|शुभ संध्या)\b',
                r'\b(आप कैसे हैं|कैसे हो|कैसी हैं)\b',
                r'\b(मिलकर खुशी हुई|आपसे मिलकर अच्छा लगा)\b'
            ],
            
            Intent.GOODBYE: [
                # English patterns
                r'\b(bye|goodbye|see you|farewell|take care)\b',
                r'\b(have a good day|have a nice day)\b',
                r'\b(catch you later|talk to you later)\b',
                
                # Hindi patterns
                r'\b(अलविदा|बाय|फिर मिलते हैं|खुदा हाफिज)\b',
                r'\b(शुभ दिन|अच्छा दिन)\b',
                r'\b(बाद में बात करते हैं|फिर बात करते हैं)\b'
            ],
            
            Intent.HELP: [
                # English patterns
                r'\b(help|can you help|what can you do)\b',
                r'\b(how does this work|how to use)\b',
                r'\b(what are your capabilities|what can you help with)\b',
                
                # Hindi patterns
                r'\b(मदद|सहायता|क्या आप मदद कर सकते हैं)\b',
                r'\b(यह कैसे काम करता है|कैसे उपयोग करें)\b',
                r'\b(आप क्या कर सकते हैं|क्या मदद कर सकते हैं)\b'
            ],
            
            Intent.SMALL_TALK: [
                # English patterns
                r'\b(how is the weather|what is the weather)\b',
                r'\b(tell me about yourself|who are you)\b',
                r'\b(what time is it|what is the time)\b',
                r'\b(how old are you|what is your age)\b',
                r'\b(where are you from|where do you live)\b',
                
                # Hindi patterns
                r'\b(मौसम कैसा है|आज मौसम कैसा है)\b',
                r'\b(आपके बारे में बताइए|आप कौन हैं)\b',
                r'\b(क्या समय हुआ है|समय क्या है)\b',
                r'\b(आपकी उम्र क्या है|आप कितने साल के हैं)\b',
                r'\b(आप कहाँ से हैं|आप कहाँ रहते हैं)\b'
            ]
        }
    
    def _initialize_faq_patterns(self) -> Dict[str, List[str]]:
        """Initialize FAQ patterns"""
        return {
            "what_is_voice_bot": [
                r'\b(what is a voice bot|what is voice assistant)\b',
                r'\b(explain voice bot|define voice bot)\b',
                r'\b(क्या है वॉयस बॉट|वॉयस असिस्टेंट क्या है)\b'
            ],
            "how_it_works": [
                r'\b(how does voice recognition work|how does speech recognition work)\b',
                r'\b(how does tts work|how does text to speech work)\b',
                r'\b(वॉयस रिकग्निशन कैसे काम करता है|स्पीच रिकग्निशन कैसे काम करता है)\b'
            ],
            "supported_languages": [
                r'\b(what languages do you support|which languages are supported)\b',
                r'\b(do you speak hindi|do you understand hindi)\b',
                r'\b(कौन सी भाषाएं सपोर्ट करते हैं|हिंदी बोलते हैं)\b'
            ],
            "privacy": [
                r'\b(is my data safe|do you store my conversations)\b',
                r'\b(privacy policy|data protection)\b',
                r'\b(क्या मेरा डेटा सुरक्षित है|प्राइवेसी पॉलिसी)\b'
            ]
        }
    
    def recognize_intent(self, text: str) -> IntentMatch:
        """
        Recognize intent from user input
        
        Args:
            text: User input text
            
        Returns:
            IntentMatch object with recognized intent
        """
        text_lower = text.lower().strip()
        
        # Check each intent pattern
        for intent, patterns in self.patterns.items():
            for pattern in patterns:
                match = re.search(pattern, text_lower, re.IGNORECASE)
                if match:
                    confidence = self._calculate_confidence(text_lower, pattern)
                    entities = self._extract_entities(text_lower, intent)
                    return IntentMatch(intent, confidence, entities, pattern)
        
        # Check FAQ patterns
        faq_intent = self._check_faq_patterns(text_lower)
        if faq_intent:
            return faq_intent
        
        # Default to fallback
        return IntentMatch(Intent.FALLBACK, 0.5, {}, "")
    
    def _calculate_confidence(self, text: str, pattern: str) -> float:
        """Calculate confidence score for pattern match"""
        # Simple confidence based on pattern match strength
        match_length = len(re.search(pattern, text, re.IGNORECASE).group())
        text_length = len(text)
        
        # Higher confidence for longer matches relative to text length
        confidence = min(0.9, match_length / text_length + 0.3)
        return confidence
    
    def _extract_entities(self, text: str, intent: Intent) -> Dict[str, Any]:
        """Extract entities from text based on intent"""
        entities = {}
        
        if intent == Intent.GREETING:
            # Extract greeting type
            if re.search(r'\b(good morning|सुप्रभात)\b', text, re.IGNORECASE):
                entities['greeting_type'] = 'morning'
            elif re.search(r'\b(good afternoon|good evening|शुभ संध्या)\b', text, re.IGNORECASE):
                entities['greeting_type'] = 'evening'
            else:
                entities['greeting_type'] = 'general'
        
        elif intent == Intent.SMALL_TALK:
            # Extract topic
            if re.search(r'\b(weather|मौसम)\b', text, re.IGNORECASE):
                entities['topic'] = 'weather'
            elif re.search(r'\b(time|समय)\b', text, re.IGNORECASE):
                entities['topic'] = 'time'
            elif re.search(r'\b(age|उम्र)\b', text, re.IGNORECASE):
                entities['topic'] = 'age'
            elif re.search(r'\b(location|जगह|कहाँ)\b', text, re.IGNORECASE):
                entities['topic'] = 'location'
            else:
                entities['topic'] = 'general'
        
        return entities
    
    def _check_faq_patterns(self, text: str) -> Optional[IntentMatch]:
        """Check FAQ patterns and return FAQ intent"""
        for faq_key, patterns in self.faq_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    entities = {'faq_topic': faq_key}
                    return IntentMatch(Intent.FAQ, 0.8, entities, pattern)
        return None


class ResponseGenerator:
    """Generates responses based on recognized intents"""
    
    def __init__(self):
        """Initialize response generator with response templates"""
        self.responses = self._initialize_responses()
        self.faq_responses = self._initialize_faq_responses()
    
    def _initialize_responses(self) -> Dict[Intent, Dict[str, List[str]]]:
        """Initialize response templates for different intents and languages"""
        return {
            Intent.GREETING: {
                "en": [
                    "Hello! Nice to meet you. How can I help you today?",
                    "Hi there! Great to see you. What would you like to know?",
                    "Good day! I'm here to assist you. What can I do for you?",
                    "Hello! Welcome! How may I be of service to you?"
                ],
                "hi": [
                    "नमस्ते! आपसे मिलकर खुशी हुई। आज मैं आपकी कैसे मदद कर सकता हूँ?",
                    "हैलो! आपको देखकर अच्छा लगा। आप क्या जानना चाहते हैं?",
                    "शुभ दिन! मैं यहाँ आपकी सहायता के लिए हूँ। मैं आपके लिए क्या कर सकता हूँ?",
                    "नमस्कार! स्वागत है! मैं आपकी कैसे सेवा कर सकता हूँ?"
                ]
            },
            
            Intent.GOODBYE: {
                "en": [
                    "Goodbye! It was nice talking to you. Take care!",
                    "See you later! Have a wonderful day!",
                    "Farewell! Thanks for the conversation. Take care!",
                    "Goodbye! Hope to talk to you again soon!"
                ],
                "hi": [
                    "अलविदा! आपसे बात करके अच्छा लगा। खुदा हाफिज!",
                    "फिर मिलते हैं! आपका दिन शुभ हो!",
                    "विदा! बातचीत के लिए धन्यवाद। खुदा हाफिज!",
                    "अलविदा! जल्द ही फिर बात करने की उम्मीद है!"
                ]
            },
            
            Intent.HELP: {
                "en": [
                    "I'm a voice assistant that can help you with various tasks. I can answer questions, have conversations, and assist with information. What would you like to know?",
                    "I'm here to help! I can chat with you, answer questions, and provide information. Just ask me anything!",
                    "I'm a multilingual voice bot that supports English and Hindi. I can help with conversations, questions, and general assistance. How can I help you?"
                ],
                "hi": [
                    "मैं एक वॉयस असिस्टेंट हूँ जो विभिन्न कार्यों में आपकी मदद कर सकता हूँ। मैं सवालों के जवाब दे सकता हूँ, बातचीत कर सकता हूँ और जानकारी प्रदान कर सकता हूँ। आप क्या जानना चाहते हैं?",
                    "मैं यहाँ मदद के लिए हूँ! मैं आपसे बात कर सकता हूँ, सवालों के जवाब दे सकता हूँ और जानकारी प्रदान कर सकता हूँ। बस मुझसे कुछ भी पूछें!",
                    "मैं एक बहुभाषी वॉयस बॉट हूँ जो अंग्रेजी और हिंदी का समर्थन करता है। मैं बातचीत, सवालों और सामान्य सहायता में मदद कर सकता हूँ। मैं आपकी कैसे मदद कर सकता हूँ?"
                ]
            },
            
            Intent.SMALL_TALK: {
                "en": [
                    "I'm doing well, thank you for asking! I'm a voice assistant created to help people. How about you?",
                    "I'm great! I enjoy helping people and having conversations. What about you?",
                    "I'm doing fantastic! I'm here to assist and chat. How are you doing today?"
                ],
                "hi": [
                    "मैं ठीक हूँ, पूछने के लिए धन्यवाद! मैं लोगों की मदद करने के लिए बनाया गया एक वॉयस असिस्टेंट हूँ। आप कैसे हैं?",
                    "मैं बहुत अच्छा हूँ! मुझे लोगों की मदद करना और बातचीत करना पसंद है। आप कैसे हैं?",
                    "मैं बहुत अच्छा हूँ! मैं यहाँ सहायता और बातचीत के लिए हूँ। आज आप कैसे हैं?"
                ]
            },
            
            Intent.FALLBACK: {
                "en": [
                    "I'm not sure I understood that. Could you please rephrase your question?",
                    "I didn't quite catch that. Can you try asking in a different way?",
                    "I'm having trouble understanding. Could you please clarify what you're asking?",
                    "I'm not sure how to help with that. Could you ask me something else?"
                ],
                "hi": [
                    "मुझे समझ नहीं आया। क्या आप अपना सवाल दोबारा पूछ सकते हैं?",
                    "मुझे समझ नहीं आया। क्या आप इसे अलग तरीके से पूछ सकते हैं?",
                    "मुझे समझने में परेशानी हो रही है। क्या आप स्पष्ट कर सकते हैं कि आप क्या पूछ रहे हैं?",
                    "मुझे नहीं पता कि इससे कैसे मदद करूं। क्या आप मुझसे कुछ और पूछ सकते हैं?"
                ]
            }
        }
    
    def _initialize_faq_responses(self) -> Dict[str, Dict[str, List[str]]]:
        """Initialize FAQ responses"""
        return {
            "what_is_voice_bot": {
                "en": [
                    "A voice bot is an artificial intelligence assistant that can understand spoken language and respond using speech. I use speech recognition to understand what you say and text-to-speech to respond back to you.",
                    "I'm a voice bot - a computer program that can listen to your voice, understand what you're saying, and respond back to you using speech. I can help with conversations, questions, and various tasks."
                ],
                "hi": [
                    "वॉयस बॉट एक कृत्रिम बुद्धिमत्ता असिस्टेंट है जो बोली गई भाषा को समझ सकता है और भाषण का उपयोग करके जवाब दे सकता है। मैं स्पीच रिकग्निशन का उपयोग करता हूँ जो आप कहते हैं उसे समझने के लिए और टेक्स्ट-टू-स्पीच का उपयोग आपको जवाब देने के लिए करता हूँ।",
                    "मैं एक वॉयस बॉट हूँ - एक कंप्यूटर प्रोग्राम जो आपकी आवाज सुन सकता है, समझ सकता है कि आप क्या कह रहे हैं, और भाषण का उपयोग करके आपको जवाब दे सकता है। मैं बातचीत, सवालों और विभिन्न कार्यों में मदद कर सकता हूँ।"
                ]
            },
            
            "how_it_works": {
                "en": [
                    "I work by listening to your voice through a microphone, converting your speech to text using speech recognition technology, understanding what you mean using natural language processing, generating an appropriate response, and then converting that response back to speech using text-to-speech technology.",
                    "The process involves: 1) Listening to your voice, 2) Converting speech to text, 3) Understanding your intent, 4) Generating a response, and 5) Converting the response back to speech for you to hear."
                ],
                "hi": [
                    "मैं माइक्रोफोन के माध्यम से आपकी आवाज सुनकर काम करता हूँ, स्पीच रिकग्निशन तकनीक का उपयोग करके आपके भाषण को टेक्स्ट में बदलता हूँ, प्राकृतिक भाषा प्रसंस्करण का उपयोग करके समझता हूँ कि आपका क्या मतलब है, उपयुक्त जवाब उत्पन्न करता हूँ, और फिर टेक्स्ट-टू-स्पीच तकनीक का उपयोग करके उस जवाब को वापस भाषण में बदलता हूँ।",
                    "प्रक्रिया में शामिल है: 1) आपकी आवाज सुनना, 2) भाषण को टेक्स्ट में बदलना, 3) आपके इरादे को समझना, 4) जवाब उत्पन्न करना, और 5) आपके सुनने के लिए जवाब को वापस भाषण में बदलना।"
                ]
            },
            
            "supported_languages": {
                "en": [
                    "I currently support English and Hindi languages. I can understand and respond in both languages, and I automatically detect which language you're speaking.",
                    "I'm bilingual! I can communicate in English and Hindi. Just speak naturally in either language, and I'll understand and respond appropriately."
                ],
                "hi": [
                    "मैं वर्तमान में अंग्रेजी और हिंदी भाषाओं का समर्थन करता हूँ। मैं दोनों भाषाओं में समझ और जवाब दे सकता हूँ, और मैं स्वचालित रूप से पता लगाता हूँ कि आप कौन सी भाषा बोल रहे हैं।",
                    "मैं द्विभाषी हूँ! मैं अंग्रेजी और हिंदी में संवाद कर सकता हूँ। बस किसी भी भाषा में स्वाभाविक रूप से बोलें, और मैं समझूंगा और उपयुक्त जवाब दूंगा।"
                ]
            },
            
            "privacy": {
                "en": [
                    "I respect your privacy. I don't store your conversations permanently, and I only process your speech to understand and respond to you. Your data is not shared with third parties.",
                    "Privacy is important to me. I process your speech in real-time to provide responses, but I don't keep permanent records of our conversations. Your information stays private."
                ],
                "hi": [
                    "मैं आपकी गोपनीयता का सम्मान करता हूँ। मैं आपकी बातचीत को स्थायी रूप से स्टोर नहीं करता, और मैं केवल आपको समझने और जवाब देने के लिए आपके भाषण को प्रोसेस करता हूँ। आपका डेटा तीसरे पक्ष के साथ साझा नहीं किया जाता।",
                    "गोपनीयता मेरे लिए महत्वपूर्ण है। मैं जवाब प्रदान करने के लिए आपके भाषण को रियल-टाइम में प्रोसेस करता हूँ, लेकिन मैं हमारी बातचीत का स्थायी रिकॉर्ड नहीं रखता। आपकी जानकारी निजी रहती है।"
                ]
            }
        }
    
    def generate_response(self, intent_match: IntentMatch, language: str = "en") -> str:
        """
        Generate response based on intent match
        
        Args:
            intent_match: Recognized intent with entities
            language: Target language for response
            
        Returns:
            Generated response text
        """
        intent = intent_match.intent
        entities = intent_match.entities
        
        # Handle FAQ responses
        if intent == Intent.FAQ and 'faq_topic' in entities:
            faq_topic = entities['faq_topic']
            if faq_topic in self.faq_responses and language in self.faq_responses[faq_topic]:
                responses = self.faq_responses[faq_topic][language]
                return random.choice(responses)
        
        # Handle regular responses
        if intent in self.responses and language in self.responses[intent]:
            responses = self.responses[intent][language]
            return random.choice(responses)
        
        # Fallback to English if language not available
        if intent in self.responses and "en" in self.responses[intent]:
            responses = self.responses[intent]["en"]
            return random.choice(responses)
        
        # Ultimate fallback
        return "I'm sorry, I didn't understand that. Could you please try again?"


class DialogManager:
    """
    Main dialog manager that coordinates intent recognition and response generation
    """
    
    def __init__(self):
        """Initialize dialog manager"""
        self.intent_recognizer = IntentRecognizer()
        self.response_generator = ResponseGenerator()
        self.conversation_history = []
        self.max_history = 10  # Keep last 10 exchanges
    
    def process_input(self, text: str, language: str = "en") -> str:
        """
        Process user input and generate response
        
        Args:
            text: User input text
            language: Detected language
            
        Returns:
            Generated response
        """
        # Recognize intent
        intent_match = self.intent_recognizer.recognize_intent(text)
        
        # Generate response
        response = self.response_generator.generate_response(intent_match, language)
        
        # Store in conversation history
        self._add_to_history(text, response, intent_match.intent.value)
        
        return response
    
    def _add_to_history(self, user_input: str, bot_response: str, intent: str):
        """Add exchange to conversation history"""
        exchange = {
            'user_input': user_input,
            'bot_response': bot_response,
            'intent': intent,
            'timestamp': self._get_timestamp()
        }
        
        self.conversation_history.append(exchange)
        
        # Keep only recent history
        if len(self.conversation_history) > self.max_history:
            self.conversation_history = self.conversation_history[-self.max_history:]
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        import datetime
        return datetime.datetime.now().isoformat()
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get conversation history"""
        return self.conversation_history.copy()
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def get_supported_intents(self) -> List[str]:
        """Get list of supported intents"""
        return [intent.value for intent in Intent]
    
    def add_custom_intent(self, intent_name: str, patterns: List[str], responses: Dict[str, List[str]]):
        """
        Add custom intent (for future extension)
        
        Args:
            intent_name: Name of the custom intent
            patterns: List of regex patterns for intent recognition
            responses: Dictionary of language -> response lists
        """
        # This is a placeholder for future extension
        # In a more advanced system, you could dynamically add intents
        logging.info(f"Custom intent '{intent_name}' would be added here")
