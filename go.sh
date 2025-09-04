#!/bin/bash

# Dodge the Blocks Game Launcher
# This script activates the virtual environment and starts the game

echo "🎮 Starting Dodge the Blocks..."
echo "📁 Activating virtual environment..."

# Activate the virtual environment
source venv/bin/activate

if [ $? -eq 0 ]; then
    echo "✅ Virtual environment activated successfully"
    echo "🚀 Launching game..."
    echo "Controls: Use LEFT/RIGHT arrow keys to move"
    echo "Press R to restart, Q to quit"
    echo ""
    
    # Start the game using the new modular structure
    python main.py
else
    echo "❌ Failed to activate virtual environment"
    echo "Please make sure the virtual environment exists:"
    echo "  python3 -m venv venv"
    echo "  source venv/bin/activate"
    echo "  pip install -r requirements.txt"
    exit 1
fi
