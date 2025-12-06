#!/bin/bash

# Install the Best Model for Text Refinement

echo "🚀 Installing Qwen2.5:7b-instruct - Best model for text refinement"
echo ""
echo "This model is specifically optimized for:"
echo "  ✅ Text refinement and editing"
echo "  ✅ Concise, accurate outputs"
echo "  ✅ Spanish language support"
echo "  ✅ Fast inference on Apple Silicon"
echo ""
echo "Size: ~4.7 GB"
echo ""

read -p "Press Enter to start download (or Ctrl+C to cancel)..."

ollama pull qwen2.5:7b-instruct

echo ""
echo "✅ Download complete!"
echo ""
echo "The app will automatically use this model for AI refinement."
echo "You can test it now by enabling 'AI refinement' in the app."
echo ""
read -p "Press Enter to close..."

