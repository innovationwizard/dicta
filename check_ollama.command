#!/bin/bash

# Quick Ollama Status Check

echo "🔍 Checking Ollama Status..."
echo ""

# Check if Ollama is installed
if command -v ollama &> /dev/null; then
    echo "✅ Ollama is installed"
    echo ""
    
    # Check if Ollama is running
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo "✅ Ollama is running"
        echo ""
        echo "📦 Available models:"
        ollama list
        echo ""
        echo "✅ Everything is ready! You can use AI refinement in the app."
    else
        echo "⚠️  Ollama is installed but not running"
        echo ""
        echo "Start it with: ollama serve"
    fi
else
    echo "❌ Ollama is not installed"
    echo ""
    echo "Install it from: https://ollama.ai"
fi

echo ""
read -p "Press Enter to close..."

