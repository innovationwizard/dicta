import mlx_whisper
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import shutil
import os
import tempfile
from pathlib import Path
from text_cleaner import process_transcription
from summarizer import generate_summary
from ollama_checker import check_ollama_status, get_recommended_model
from ollama_starter import ensure_ollama_running
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

# Enable CORS for localhost frontend (including file:// protocol)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for local development
    allow_credentials=False,  # Must be False when using wildcard origins
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model will be loaded on first request (lazy loading)
model_loaded = False
model_path = "mlx-community/whisper-large-v3-turbo"

@app.get("/")
async def root():
    return {"message": "Speech-to-Text API is running", "model": model_path}

@app.post("/transcribe")
async def transcribe(
    file: UploadFile = File(...),
    clean_text: str = Form("true"),
    use_ai_refinement: str = Form("false"),
    ai_model: Optional[str] = Form(None)
):
    """
    Transcribe an audio file to text using MLX Whisper.
    Supports common audio formats (wav, mp3, m4a, etc.)
    
    Parameters:
    - clean_text: Apply basic text cleaning (remove repetitions, fix formatting)
    - use_ai_refinement: Use AI for final refinement (requires Ollama or similar)
    - ai_model: AI model identifier (optional, defaults to llama3.2:1b for Ollama)
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Create temporary file to save uploaded audio
    temp_dir = tempfile.gettempdir()
    temp_file_path = os.path.join(temp_dir, f"temp_{file.filename}")
    
    try:
        # Save uploaded file temporarily
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Transcribe using MLX Whisper
        result = mlx_whisper.transcribe(
            temp_file_path,
            path_or_hf_repo=model_path,
            verbose=False
        )
        
        # Extract raw text from result
        raw_text = result.get("text", "")
        
        # Parse boolean parameters
        should_clean = clean_text.lower() in ("true", "1", "yes")
        should_use_ai = use_ai_refinement.lower() in ("true", "1", "yes")
        
        # Process and clean the text
        if should_clean or should_use_ai:
            processed_text = process_transcription(
                raw_text,
                use_ai_refinement=should_use_ai,
                ai_model=ai_model
            )
        else:
            processed_text = raw_text
        
        # Also return segments if available for more detailed output
        segments = result.get("segments", [])
        
        return {
            "transcription": processed_text,
            "raw_transcription": raw_text,  # Include raw for comparison
            "segments": segments,
            "filename": file.filename,
            "cleaned": should_clean,
            "ai_refined": should_use_ai
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")
    
    finally:
        # Clean up temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/ollama/status")
async def ollama_status():
    """
    Check Ollama status and available models.
    Automatically starts Ollama if it's not running.
    
    Returns:
        Status information including whether Ollama is running
        and which models are available.
    """
    # Ensure Ollama is running (will start it if needed)
    status = ensure_ollama_running()
    
    recommended_model = None
    if status["running"] and status["available_models"]:
        recommended_model = get_recommended_model(status["available_models"])
    
    return {
        "running": status["running"],
        "was_started": status.get("was_started", False),
        "available_models": status["available_models"],
        "recommended_model": recommended_model,
        "error": status["error"]
    }


class SummarizeRequest(BaseModel):
    text: str
    summary_type: str  # 'executive', 'top3', 'top5', 'top10'
    model: Optional[str] = None


@app.post("/summarize")
async def summarize(request: SummarizeRequest):
    """
    Generate summaries or extract key ideas from transcribed text.
    
    Parameters:
    - text: The cleaned/refined transcription text
    - summary_type: Type of summary ('executive', 'top3', 'top5', 'top10')
    - model: Optional AI model identifier (defaults to best available)
    
    Returns:
    - For 'executive': Executive summary text
    - For 'top3', 'top5', 'top10': List of key ideas
    """
    if not request.text or len(request.text.strip()) < 50:
        raise HTTPException(
            status_code=400, 
            detail="Text is too short to generate a summary. Minimum 50 characters required."
        )
    
    valid_types = ['executive', 'top3', 'top5', 'top10']
    if request.summary_type not in valid_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid summary_type. Must be one of: {', '.join(valid_types)}"
        )
    
    try:
        result = generate_summary(
            request.text,
            request.summary_type,
            request.model
        )
        
        return {
            "success": True,
            "summary_type": result['type'],
            "title": result['title'],
            "content": result['content'],
            "model_used": request.model or "auto-selected"
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Summarization failed: {str(e)}"
        )

