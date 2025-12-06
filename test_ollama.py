#!/usr/bin/env python3
"""
Test Ollama connection and AI refinement functionality
"""

import requests
import json

def test_ollama_connection():
    """Test if Ollama is running and accessible"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            print("✅ Ollama is running!")
            print(f"📦 Available models: {len(models)}")
            for model in models:
                print(f"   - {model.get('name', 'unknown')}")
            return True, models
        else:
            print(f"❌ Ollama returned status code: {response.status_code}")
            return False, []
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Ollama. Is it running?")
        print("   Start it with: ollama serve")
        return False, []
    except Exception as e:
        print(f"❌ Error: {e}")
        return False, []

def test_ai_refinement():
    """Test AI refinement with a sample text"""
    # Use a small model for testing
    test_models = ["llama3.1:8b", "mistral:7b"]
    
    test_text = """porque aquel dijo no es que yo las liquidaciones le digo a no sé a chap gpt o no sé o a ese otro chuncho
porque aquel dijo no es que yo las liquidaciones le digo a no sé a chap gpt o no sé o a ese otro chuncho
porque aquel dijo no es que yo las liquidaciones le digo a no sé a chap gpt o no sé o a ese otro chuncho"""
    
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
{test_text}

Cleaned and improved text:"""

    for model_name in test_models:
        print(f"\n🧪 Testing with model: {model_name}")
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": model_name,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json().get("response", "")
                print("✅ AI refinement works!")
                print(f"\n📝 Result preview (first 200 chars):")
                print(result[:200] + "..." if len(result) > 200 else result)
                return True, model_name
            else:
                print(f"❌ Model returned status code: {response.status_code}")
        except requests.exceptions.Timeout:
            print(f"⏱️  Model {model_name} timed out (this is normal for large models)")
        except Exception as e:
            print(f"❌ Error with {model_name}: {e}")
    
    return False, None

if __name__ == "__main__":
    print("🔍 Testing Ollama Integration...\n")
    
    # Test connection
    is_running, models = test_ollama_connection()
    
    if is_running and models:
        print("\n" + "="*50)
        # Test AI refinement
        works, recommended_model = test_ai_refinement()
        
        if works:
            print(f"\n✅ Everything is set up! Recommended model: {recommended_model}")
        else:
            print("\n⚠️  AI refinement test failed, but Ollama is running.")
            print("   You can still use basic text cleaning.")
    else:
        print("\n❌ Please start Ollama first:")
        print("   ollama serve")

