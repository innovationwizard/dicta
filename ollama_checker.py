"""
Utility module to check Ollama status and available models.
"""

import requests
from typing import Dict, List, Optional


def check_ollama_status() -> Dict:
    """
    Check if Ollama is running and return status information.
    
    Returns:
        Dictionary with status information:
        {
            "running": bool,
            "available_models": List[str],
            "error": Optional[str]
        }
    """
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=3)
        
        if response.status_code == 200:
            data = response.json()
            models = data.get("models", [])
            model_names = [model.get("name", "") for model in models if model.get("name")]
            
            return {
                "running": True,
                "available_models": model_names,
                "error": None
            }
        else:
            return {
                "running": False,
                "available_models": [],
                "error": f"Ollama returned status code {response.status_code}"
            }
    
    except requests.exceptions.ConnectionError:
        return {
            "running": False,
            "available_models": [],
            "error": "Ollama is not running. Start it with: ollama serve"
        }
    except requests.exceptions.Timeout:
        return {
            "running": False,
            "available_models": [],
            "error": "Ollama connection timed out"
        }
    except Exception as e:
        return {
            "running": False,
            "available_models": [],
            "error": f"Error checking Ollama: {str(e)}"
        }


def get_recommended_model(available_models: List[str]) -> Optional[str]:
    """
    Get the recommended model from available models for text tasks.
    
    Args:
        available_models: List of available model names
    
    Returns:
        Recommended model name or None
    """
    # Priority order for text refinement/summarization
    priority_models = [
        "qwen2.5:7b-instruct",
        "qwen2.5:7b",
        "phi3.5:mini-instruct",
        "llama3.2:3b-instruct",
        "llama3.1:8b",
        "mistral:7b",
        "llama3.2:1b-instruct"
    ]
    
    for model in priority_models:
        if model in available_models:
            return model
    
    # Return first available model if none match priority
    return available_models[0] if available_models else None

