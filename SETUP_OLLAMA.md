# Ollama Setup Guide

## Status: ✅ Ollama is Already Installed and Running!

You have the following models available:
- `mistral:7b` (4.4 GB)
- `llama3.1:8b` (4.9 GB)

## Quick Start

### 1. Verify Ollama is Running

```bash
ollama list
```

You should see your models listed.

### 2. Test the Connection

The app will automatically use your available models. The default order is:
1. `llama3.1:8b` (if available - you have this!)
2. `mistral:7b` (if available - you have this!)
3. Other models as fallback

### 3. Using AI Refinement in the App

1. Open the app in your browser
2. Upload an audio file
3. **Enable the "🤖 AI refinement" checkbox**
4. Click "Transcribe Audio"

The app will automatically use one of your available models.

## Troubleshooting

### "AI refinement not working"

1. **Check Ollama is running:**
   ```bash
   curl http://localhost:11434/api/tags
   ```
   Should return JSON with your models.

2. **Check requests library:**
   The app needs the `requests` library. It should already be installed, but if not:
   ```bash
   pip install requests
   ```

3. **Check server logs:**
   If AI refinement fails, check the terminal where your server is running for error messages.

### Install Additional Models (Optional)

If you want a smaller, faster model:

```bash
ollama pull llama3.2:1b  # Small, fast (1.3 GB)
ollama pull llama3.2:3b  # Medium, balanced (2.0 GB)
```

### Performance Tips

- **Smaller models** (like `llama3.2:1b`) are faster but less accurate
- **Larger models** (like `llama3.1:8b`) are slower but more accurate
- Your current models (`mistral:7b`, `llama3.1:8b`) are good for quality

## How It Works

When you enable AI refinement:
1. The raw transcription is cleaned (repetitions removed)
2. The cleaned text is sent to Ollama
3. Ollama improves the text for fluency
4. The refined text is returned to you

**Processing time:** Adds 10-30 seconds depending on text length and model size.

## Ready to Use!

Your setup is complete. Just enable the "🤖 AI refinement" checkbox in the app to use it!

