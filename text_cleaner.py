"""
Text cleaning and post-processing module for transcriptions.
Removes repetitions, fixes formatting, and optionally uses AI for refinement.
"""

import re
from typing import Optional, List, Tuple


def remove_repetitions(text: str, min_repeat_length: int = 10) -> str:
    """
    Remove repetitive phrases from text.
    Detects and removes repeated sequences of words.
    """
    words = text.split()
    if len(words) < min_repeat_length:
        return text
    
    # Look for repeated sequences
    result_words = []
    i = 0
    
    while i < len(words):
        # Try to find a repeating pattern starting at position i
        found_repetition = False
        
        # Check sequences of different lengths (longer first for better detection)
        for seq_len in range(min(50, len(words) - i), min_repeat_length - 1, -1):
            if i + seq_len * 2 > len(words):
                continue
                
            sequence = words[i:i+seq_len]
            sequence_text = " ".join(sequence)
            
            # Check if this sequence repeats immediately after
            next_sequence = words[i+seq_len:i+seq_len*2]
            next_sequence_text = " ".join(next_sequence)
            
            # Normalize for comparison (lowercase, remove punctuation)
            seq_normalized = re.sub(r'[^\w\s]', '', sequence_text.lower())
            next_normalized = re.sub(r'[^\w\s]', '', next_sequence_text.lower())
            
            if seq_normalized == next_normalized and len(seq_normalized) > min_repeat_length:
                # Found repetition - count how many times it repeats
                repeat_count = 1
                check_pos = i + seq_len
                
                while check_pos + seq_len <= len(words):
                    check_seq = words[check_pos:check_pos+seq_len]
                    check_seq_text = " ".join(check_seq)
                    check_normalized = re.sub(r'[^\w\s]', '', check_seq_text.lower())
                    
                    if check_normalized == seq_normalized:
                        repeat_count += 1
                        check_pos += seq_len
                    else:
                        break
                
                # Keep only one instance if repeated more than once
                if repeat_count > 1:
                    result_words.extend(sequence)
                    i += seq_len * repeat_count
                    found_repetition = True
                    break
        
        if not found_repetition:
            result_words.append(words[i])
            i += 1
    
    return " ".join(result_words)


def clean_fragmented_sentences(text: str) -> str:
    """
    Clean up fragmented sentences and improve formatting.
    """
    # Remove excessive line breaks and spaces
    text = re.sub(r'\n\s*\n+', '\n\n', text)
    text = re.sub(r' +', ' ', text)
    
    # Fix sentence endings
    text = re.sub(r'\s+([\.\?!])', r'\1', text)
    
    # Capitalize sentences
    sentences = re.split(r'([\.\?!]\s+)', text)
    result = []
    
    for i, part in enumerate(sentences):
        if i == 0 or (i > 0 and sentences[i-1].endswith(('.', '!', '?'))):
            if part.strip():
                part = part.strip()
                if part:
                    part = part[0].upper() + part[1:] if len(part) > 1 else part.upper()
        result.append(part)
    
    return ''.join(result).strip()


def remove_short_repeats(text: str) -> str:
    """
    Remove short repeated phrases (like "es de la cartería" repeated many times).
    """
    lines = text.split('\n')
    cleaned_lines = []
    seen_phrases = {}
    
    for line in lines:
        line = line.strip()
        if not line:
            cleaned_lines.append('')
            continue
        
        # Normalize line for comparison
        normalized = re.sub(r'[^\w\s]', '', line.lower()).strip()
        
        # Skip if this phrase appeared recently (within last 3 lines)
        if normalized in seen_phrases:
            last_seen = seen_phrases[normalized]
            # If it appeared very recently, skip it
            if len(cleaned_lines) - last_seen < 3:
                continue
        
        cleaned_lines.append(line)
        seen_phrases[normalized] = len(cleaned_lines) - 1
        
        # Clean up old entries to avoid memory issues
        if len(seen_phrases) > 100:
            # Remove entries older than 20 lines
            old_keys = [k for k, v in seen_phrases.items() if v < len(cleaned_lines) - 20]
            for k in old_keys:
                del seen_phrases[k]
    
    return '\n'.join(cleaned_lines)


def clean_text(text: str, aggressive: bool = True) -> str:
    """
    Apply all cleaning methods to improve text quality.
    
    Args:
        text: Raw transcription text
        aggressive: Use more aggressive cleaning (removes more repetitions)
    
    Returns:
        Cleaned text
    """
    if not text:
        return text
    
    # Step 1: Remove obvious repetitions
    cleaned = remove_repetitions(text, min_repeat_length=8 if aggressive else 15)
    
    # Step 2: Remove short repeated phrases
    cleaned = remove_short_repeats(cleaned)
    
    # Step 3: Clean up formatting
    cleaned = clean_fragmented_sentences(cleaned)
    
    return cleaned


def refine_with_llm(text: str, model: Optional[str] = None) -> str:
    """
    Refine text using an LLM for better coherence and fluency.
    
    Uses Ollama (local LLM) for text refinement.
    
    Args:
        text: Text to refine
        model: Model identifier or None for default (tries available models)
    
    Returns:
        Refined text, or original text if refinement fails
    """
    prompt = f"""You are a text editor. Clean up and improve the following transcription. 
The text may contain repetitions, fragmented sentences, and disfluencies.

Requirements:
- Remove all repetitions
- Fix grammar and sentence structure
- Make it fluent and natural
- Preserve the original meaning and content
- Maintain the original language (Spanish in this case)
- Do not add information that wasn't in the original

Original text:
{text}

Cleaned and improved text:"""

    # Try Ollama (most common local setup)
    try:
        import requests
    except ImportError:
        raise ImportError("requests library is required for AI refinement. Install it with: pip install requests")
    
    # Try available models in order of preference
    models_to_try = []
    if model:
        models_to_try.append(model)
    
    # Add model names to try, ordered by best performance for text refinement
    # Priority: Models optimized for text editing/refinement tasks
    models_to_try.extend([
        "qwen2.5:7b-instruct",      # Best for text refinement - optimized for concise, accurate outputs
        "qwen2.5:7b",                # Alternative Qwen variant
        "phi3.5:mini-instruct",      # Fast and good for text refinement
        "llama3.2:3b-instruct",      # Better instruction following than 3.1
        "llama3.2:1b-instruct",      # Smaller, faster version
        "llama3.1:8b",               # Your current model (fallback)
        "mistral:7b",                # Your current model (fallback)
        "llama3.2:3b",               # Fallback variants
        "llama3.2:1b"
    ])
    
    ollama_url = "http://localhost:11434/api/generate"
    
    for model_name in models_to_try:
        try:
            response = requests.post(
                ollama_url,
                json={
                    "model": model_name,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json().get("response", "")
                if result:
                    # Extract just the cleaned text (sometimes LLM adds extra text)
                    lines = result.split("\n")
                    cleaned_lines = []
                    found_marker = False
                    
                    for line in lines:
                        if "cleaned" in line.lower() and "improved" in line.lower():
                            found_marker = True
                            continue
                        if found_marker and line.strip():
                            cleaned_lines.append(line.strip())
                    
                    if cleaned_lines:
                        return "\n".join(cleaned_lines)
                    
                    # If no marker found, return the result (might be the cleaned text already)
                    return result.strip()
        except requests.exceptions.ConnectionError:
            raise ConnectionError("Cannot connect to Ollama. Make sure it's running: ollama serve")
        except requests.exceptions.Timeout:
            # Try next model if this one times out
            continue
        except Exception as e:
            # Try next model if this one fails
            continue
    
    # If all models failed, return original text
    return text


def process_transcription(
    text: str,
    use_ai_refinement: bool = False,
    ai_model: Optional[str] = None
) -> str:
    """
    Complete transcription processing pipeline.
    
    Args:
        text: Raw transcription text
        use_ai_refinement: Whether to use AI for final refinement
        ai_model: AI model identifier (optional)
    
    Returns:
        Processed text
    """
    # Step 1: Basic cleaning
    cleaned = clean_text(text, aggressive=True)
    
    # Step 2: Optional AI refinement
    if use_ai_refinement:
        try:
            cleaned = refine_with_llm(cleaned, model=ai_model)
        except Exception as e:
            print(f"AI refinement failed: {e}. Using cleaned text without AI.")
    
    return cleaned

