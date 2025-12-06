"""
Utility module to start Ollama automatically if it's not running.
"""

import subprocess
import time
import requests
from typing import Dict, Optional


def start_ollama() -> Dict:
    """
    Start Ollama service if it's not already running.
    
    Returns:
        Dictionary with status information:
        {
            "started": bool,
            "already_running": bool,
            "error": Optional[str],
            "pid": Optional[int]
        }
    """
    # First check if it's already running
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            return {
                "started": False,
                "already_running": True,
                "error": None,
                "pid": None
            }
    except:
        pass  # Not running, continue to start it
    
    try:
        # Try to start Ollama
        # On macOS, Ollama typically runs as a service via launchd
        # We can try to start it using the ollama command
        
        # Method 1: Try using 'ollama serve' command
        try:
            process = subprocess.Popen(
                ["ollama", "serve"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                start_new_session=True
            )
            
            # Wait a bit for it to start
            time.sleep(3)
            
            # Check if it's running now
            try:
                response = requests.get("http://localhost:11434/api/tags", timeout=3)
                if response.status_code == 200:
                    return {
                        "started": True,
                        "already_running": False,
                        "error": None,
                        "pid": process.pid
                    }
            except:
                pass
            
            # If not responding yet, wait a bit more
            time.sleep(2)
            try:
                response = requests.get("http://localhost:11434/api/tags", timeout=3)
                if response.status_code == 200:
                    return {
                        "started": True,
                        "already_running": False,
                        "error": None,
                        "pid": process.pid
                    }
            except:
                pass
            
            # If still not working, try alternative method
            process.terminate()
            
        except FileNotFoundError:
            # Ollama command not found in PATH
            pass
        except Exception as e:
            pass
        
        # Method 2: Try to start via launchctl (macOS)
        try:
            result = subprocess.run(
                ["launchctl", "load", "-w", "~/Library/LaunchAgents/com.ollama.ollama.plist"],
                capture_output=True,
                timeout=5
            )
            time.sleep(3)
            
            try:
                response = requests.get("http://localhost:11434/api/tags", timeout=3)
                if response.status_code == 200:
                    return {
                        "started": True,
                        "already_running": False,
                        "error": None,
                        "pid": None
                    }
            except:
                pass
        except:
            pass
        
        # Method 3: Try open command (macOS - opens Ollama app if installed)
        try:
            subprocess.Popen(
                ["open", "-a", "Ollama"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            time.sleep(5)  # Wait longer for app to start
            
            # Check if it's running now
            for _ in range(3):
                try:
                    response = requests.get("http://localhost:11434/api/tags", timeout=3)
                    if response.status_code == 200:
                        return {
                            "started": True,
                            "already_running": False,
                            "error": None,
                            "pid": None
                        }
                except:
                    time.sleep(2)
        except:
            pass
        
        return {
            "started": False,
            "already_running": False,
            "error": "Could not start Ollama automatically. Please start it manually: ollama serve",
            "pid": None
        }
    
    except Exception as e:
        return {
            "started": False,
            "already_running": False,
            "error": f"Error starting Ollama: {str(e)}",
            "pid": None
        }


def ensure_ollama_running() -> Dict:
    """
    Ensure Ollama is running, start it if needed.
    
    Returns:
        Dictionary with final status:
        {
            "running": bool,
            "was_started": bool,
            "available_models": List[str],
            "error": Optional[str]
        }
    """
    # Check if already running
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=3)
        if response.status_code == 200:
            data = response.json()
            models = data.get("models", [])
            model_names = [model.get("name", "") for model in models if model.get("name")]
            
            return {
                "running": True,
                "was_started": False,
                "available_models": model_names,
                "error": None
            }
    except:
        pass
    
    # Not running, try to start it
    start_result = start_ollama()
    
    if start_result["started"] or start_result["already_running"]:
        # Give it a moment to fully initialize
        time.sleep(2)
        
        # Check again
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                models = data.get("models", [])
                model_names = [model.get("name", "") for model in models if model.get("name")]
                
                return {
                    "running": True,
                    "was_started": start_result["started"],
                    "available_models": model_names,
                    "error": None
                }
        except Exception as e:
            return {
                "running": False,
                "was_started": start_result["started"],
                "available_models": [],
                "error": f"Ollama started but not responding: {str(e)}"
            }
    
    return {
        "running": False,
        "was_started": False,
        "available_models": [],
        "error": start_result.get("error", "Failed to start Ollama")
    }

