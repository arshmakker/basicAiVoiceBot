#!/bin/bash
# Hybrid Docker + Native Audio Solution

echo "🐳 Starting Hybrid Voice Bot (Docker + Native Audio)"
echo "===================================================="

# Check if we're in the right directory
if [ ! -f "voice_bot.py" ]; then
    echo "❌ Please run this from the voice bot directory"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Run with native audio access
echo "🎤 Starting voice bot with native audio access..."
echo "💡 This will have full microphone access but may crash"
echo "💡 Press Ctrl+C to stop"

python3 voice_bot.py manual
