# Best Ollama Models for Text Refinement

## Current Models Analysis

You currently have:
- **mistral:7b** (4.4 GB) - Good general-purpose model
- **llama3.1:8b** (4.9 GB) - Strong for general tasks

### Are these optimal for text refinement?

**Short answer:** They're decent, but there are **better models specifically designed for text editing tasks**.

## Recommended Models for Text Refinement

Based on research and benchmarks, here are the best models for your use case:

### 🥇 Best Overall: Qwen2.5:7b-instruct

**Why it's best:**
- Specifically optimized for concise, accurate outputs
- Excellent at text refinement and summarization
- Fast inference on Apple Silicon
- Good multilingual support (including Spanish)
- Designed for instruction-following tasks

**Size:** ~4.7 GB  
**Speed:** Fast  
**Quality:** Excellent for text editing

**Install:**
```bash
ollama pull qwen2.5:7b-instruct
```

### 🥈 Best for Speed: Phi-3.5-mini-instruct

**Why it's good:**
- Very fast responses
- Concise, accurate outputs
- Small model size
- Perfect for quick text refinement

**Size:** ~2.3 GB  
**Speed:** Very Fast  
**Quality:** Very Good

**Install:**
```bash
ollama pull phi3.5:mini-instruct
```

### 🥉 Best for Quality: Llama 3.2 (Newer versions)

**Why it's good:**
- Better than your current llama3.1:8b
- Improved instruction following
- Better at text refinement tasks

**Options:**
```bash
# Large, high quality (recommended)
ollama pull llama3.2:3b-instruct

# Or smaller, faster
ollama pull llama3.2:1b-instruct
```

## Comparison Table

| Model | Size | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| **qwen2.5:7b-instruct** | 4.7 GB | Fast | ⭐⭐⭐⭐⭐ | **Text refinement (BEST)** |
| **phi3.5:mini-instruct** | 2.3 GB | Very Fast | ⭐⭐⭐⭐ | Quick refinement |
| **llama3.2:3b-instruct** | 2.0 GB | Fast | ⭐⭐⭐⭐ | Balanced quality/speed |
| **mistral:7b** (current) | 4.4 GB | Medium | ⭐⭐⭐ | General purpose |
| **llama3.1:8b** (current) | 4.9 GB | Medium | ⭐⭐⭐ | General purpose |

## Specific Recommendations for Your Use Case

### For Spanish Text Refinement

Since you're working with Spanish transcriptions:

1. **Qwen2.5:7b-instruct** - Excellent Spanish support, best overall
2. **Mistral models** - Known for good Spanish handling (you already have one)
3. **Llama 3.2** - Improved multilingual support over 3.1

### For Speed vs Quality Trade-off

- **Need speed?** → `phi3.5:mini-instruct` (2.3 GB, very fast)
- **Need quality?** → `qwen2.5:7b-instruct` (4.7 GB, best refinement)
- **Need balance?** → `llama3.2:3b-instruct` (2.0 GB, good all-around)

## Quick Setup

### Recommended Setup (Best Quality)

```bash
# Pull the best model for text refinement
ollama pull qwen2.5:7b-instruct

# The app will automatically use it (it's in the priority list)
```

### Alternative Setup (Best Speed)

```bash
# Pull the fastest model
ollama pull phi3.5:mini-instruct

# Or for a good balance
ollama pull llama3.2:3b-instruct
```

## Updating Your Code

The app will automatically detect and use these models. The current priority order in `text_cleaner.py` is:

1. llama3.1:8b (you have this)
2. mistral:7b (you have this)
3. llama3.2:1b
4. llama3.2:3b

We should update it to prioritize the better models. Let me know if you want me to update the code!

## Recommendation

**For your specific task (Spanish text refinement from transcriptions):**

1. **Install Qwen2.5:7b-instruct** - It's specifically designed for this type of task
   ```bash
   ollama pull qwen2.5:7b-instruct
   ```

2. **Keep your existing models** as fallbacks (they're still useful)

3. **Update the code** to prioritize Qwen2.5 first

This will give you the best results for cleaning up and refining your transcriptions.

## Testing

After installing a new model, test it:
```bash
# Test with a sample text
python3 test_ollama.py
```

Or just use it in the app - it will automatically try available models in order.

