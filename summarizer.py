"""
Summarization module for generating executive summaries and extracting key ideas.
Uses Ollama for AI-powered summarization.
"""

import requests
from typing import Optional, List


def generate_executive_summary(text: str, model: Optional[str] = None) -> str:
    """
    Generate an executive summary of the transcribed text.
    
    Args:
        text: The cleaned/refined transcription text
        model: Optional model name (defaults to available models)
    
    Returns:
        Executive summary text
    """
    if not text or len(text.strip()) < 50:
        return "Text is too short to generate a summary."
    
    prompt = f"""You are an expert at creating executive summaries. 

Create a concise executive summary of the following transcription in Spanish.

Requirements:
- Summarize the main points and key topics discussed
- Keep it concise (2-4 paragraphs)
- Write in clear, professional Spanish
- Focus on the most important information
- Maintain the original meaning and context

Transcription:
{text}

Executive Summary:"""

    return _call_ollama(prompt, model)


def extract_key_ideas(text: str, num_ideas: int = 10, model: Optional[str] = None) -> List[str]:
    """
    Extract the top N key ideas from the transcribed text.
    
    Args:
        text: The cleaned/refined transcription text
        num_ideas: Number of ideas to extract (3, 5, or 10)
        model: Optional model name (defaults to available models)
    
    Returns:
        List of key ideas as bullet points
    """
    if not text or len(text.strip()) < 50:
        return ["Text is too short to extract ideas."]
    
    if num_ideas not in [3, 5, 10]:
        num_ideas = 10  # Default to 10
    
    prompt = f"""You are an expert at extracting key ideas from transcriptions.

Extract the top {num_ideas} most important ideas from the following transcription in Spanish.

Requirements:
- Extract the {num_ideas} most important and relevant ideas
- Each idea should be a clear, concise bullet point
- Write in Spanish, matching the language of the transcription
- Focus on actionable insights, key decisions, or important information
- Number each idea
- Be specific and concrete

Transcription:
{text}

Top {num_ideas} Ideas:
1."""

    result = _call_ollama(prompt, model)
    
    # Parse the response into a list of ideas
    ideas = []
    lines = result.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Remove leading numbers and bullet points
        line = line.lstrip('0123456789.-•* ')
        
        # Only add substantial ideas (at least 10 characters)
        if len(line) > 10:
            ideas.append(line)
        
        # Stop at the requested number
        if len(ideas) >= num_ideas:
            break
    
    # If we didn't get enough ideas, add what we have
    if len(ideas) < num_ideas and ideas:
        return ideas
    
    # If no ideas extracted, return a single message
    if not ideas:
        return [f"No se pudieron extraer {num_ideas} ideas del texto."]
    
    return ideas[:num_ideas]


def _call_ollama(prompt: str, model: Optional[str] = None) -> str:
    """
    Call Ollama API to generate text using the specified model.
    
    Args:
        prompt: The prompt to send to the model
        model: Optional model name (defaults to available models)
    
    Returns:
        Generated text response
    """
    try:
        import requests
    except ImportError:
        raise ImportError("requests library is required. Install it with: pip install requests")
    
    # Try available models in order of preference
    models_to_try = []
    if model:
        models_to_try.append(model)
    
    # Add model names to try (prioritize text-focused models)
    models_to_try.extend([
        "qwen2.5:7b-instruct",      # Best for text tasks
        "qwen2.5:7b",
        "llama3.1:8b",
        "mistral:7b",
        "phi3.5:mini-instruct",
        "llama3.2:3b-instruct"
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
                timeout=180  # Longer timeout for summarization
            )
            
            if response.status_code == 200:
                result = response.json().get("response", "")
                if result:
                    return result.strip()
        except requests.exceptions.ConnectionError:
            raise ConnectionError("Cannot connect to Ollama. Make sure it's running: ollama serve")
        except requests.exceptions.Timeout:
            continue  # Try next model
        except Exception:
            continue  # Try next model
    
    # If all models failed
    raise Exception("Failed to generate summary. Make sure Ollama is running and models are available.")


def generate_summary(text: str, summary_type: str, model: Optional[str] = None) -> dict:
    """
    Generate the requested type of summary.
    
    Args:
        text: The cleaned/refined transcription text
        summary_type: Type of summary ('executive', 'top3', 'top5', 'top10')
        model: Optional model name
    
    Returns:
        Dictionary with summary data
    """
    if summary_type == 'executive':
        summary_text = generate_executive_summary(text, model)
        return {
            'type': 'executive',
            'title': 'Executive Summary',
            'content': summary_text
        }
    elif summary_type == 'top3':
        ideas = extract_key_ideas(text, 3, model)
        return {
            'type': 'top3',
            'title': 'Top 3 Ideas',
            'content': ideas
        }
    elif summary_type == 'top5':
        ideas = extract_key_ideas(text, 5, model)
        return {
            'type': 'top5',
            'title': 'Top 5 Ideas',
            'content': ideas
        }
    elif summary_type == 'top10':
        ideas = extract_key_ideas(text, 10, model)
        return {
            'type': 'top10',
            'title': 'Top 10 Ideas',
            'content': ideas
        }
    else:
        raise ValueError(f"Unknown summary type: {summary_type}")

