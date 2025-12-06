# Text Cleaning Feature

## Overview

The app now includes intelligent text cleaning to fix common transcription issues like repetitions, fragmented sentences, and formatting problems.

## Features

### 🧹 Automatic Text Cleaning (Default)

Enabled by default, this removes:
- **Repetitive phrases**: Detects and removes repeated sequences (e.g., "porque aquel dijo..." repeated multiple times)
- **Short repeats**: Eliminates phrases like "es de la cartería" that repeat many times
- **Formatting issues**: Fixes excessive line breaks, spaces, and capitalization

### 🤖 Optional AI Refinement

For even better results, you can enable AI refinement which uses a local LLM (via Ollama) to:
- Improve sentence structure and fluency
- Enhance naturalness of the text
- Maintain original meaning while improving readability

## How It Works

### Basic Cleaning (Always Available)

The cleaning process has multiple stages:

1. **Repetition Detection**: Identifies repeated word sequences and removes duplicates
2. **Short Repeat Removal**: Eliminates frequently repeating short phrases
3. **Formatting Cleanup**: Fixes sentence structure, capitalization, and spacing

### AI Refinement (Optional)

When enabled, the cleaned text is passed to a local LLM (Ollama) with instructions to:
- Remove remaining repetitions
- Fix grammar and sentence structure
- Make text more fluent and natural
- Preserve original meaning

## Setup

### Basic Cleaning

No setup required! Text cleaning is enabled by default.

### AI Refinement Setup

1. **Install Ollama**: Download from https://ollama.ai

2. **Pull a model** (choose based on your preference):
   ```bash
   # Small, fast model (recommended for quick results)
   ollama pull llama3.2:1b
   
   # Medium model (better quality, slower)
   ollama pull llama3.2:3b
   
   # Or any other model you prefer
   ```

3. **Start Ollama** (usually runs automatically as a service)

4. **Enable in the app**: Check the "🤖 AI refinement" checkbox before transcribing

## Performance

- **Basic cleaning**: Adds < 1 second processing time
- **AI refinement**: Adds 5-30 seconds depending on model size and text length

## Example

**Before (raw transcription):**
```
porque aquel dijo no es que yo las liquidaciones le digo a no sé a chap gpt o no sé o a ese otro chuncho
porque aquel dijo no es que yo las liquidaciones le digo a no sé a chap gpt o no sé o a ese otro chuncho
porque aquel dijo no es que yo las liquidaciones le digo a no sé a chap gpt o no sé o a ese otro chuncho
```

**After (cleaned):**
```
porque aquel dijo no es que yo las liquidaciones le digo a no sé a chap gpt o no sé o a ese otro chuncho
```

**After (with AI refinement):**
```
Le dije a ChatGPT o a otro servicio que no es que yo haga las liquidaciones.
```

## Tips

- **Start with basic cleaning**: It fixes most issues and is very fast
- **Use AI refinement for important documents**: Better results but slower
- **Try different Ollama models**: Larger models = better quality but slower processing
- **Disable cleaning if you want raw output**: Uncheck "Clean text" to see the original transcription

## Troubleshooting

### AI Refinement not working?

1. Make sure Ollama is installed and running
2. Check that you've pulled a model: `ollama list`
3. Verify Ollama is accessible: `curl http://localhost:11434/api/tags`
4. Try a smaller model if processing times out

### Cleaning too aggressive?

- The algorithm is tuned for common repetition patterns
- If it removes valid repeated phrases, you can disable cleaning
- Consider using AI refinement which is more context-aware

