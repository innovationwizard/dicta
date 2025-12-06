# Speech to Text Converter

A high-performance web application for converting speech files to text, optimized for Apple Silicon (M1/M2/M3) using MLX Whisper.

## Features

- 🚀 **Optimized for Apple Silicon**: Uses MLX framework for 2-6x faster transcription than standard implementations
- 🎯 **High Accuracy**: Uses `whisper-large-v3-turbo` model for near-Large accuracy at higher speeds
- 🧹 **Smart Text Cleaning**: Automatically removes repetitions and fixes formatting issues
- 🤖 **Optional AI Refinement**: Enhance transcriptions with local AI (Ollama) for better fluency
- 🎨 **Modern UI**: Clean, responsive web interface
- 📁 **Multiple Formats**: Supports WAV, MP3, M4A, and other common audio formats
- 💾 **Export Results**: Download transcriptions as text files

## Requirements

- macOS with Apple Silicon (M1/M2/M3)
- Python 3.8 or higher
- Modern web browser (Chrome, Safari, Firefox)

## Installation

1. **Clone or navigate to the project directory**

2. **Create a virtual environment (recommended)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   Note: The first time you run the app, MLX Whisper will automatically download the `whisper-large-v3-turbo` model (~3GB). This is a one-time download.

## Usage

### 🚀 Quick Start (Easiest Method)

**Double-click `start-servers.command`** - This will:
- Start both backend and frontend servers automatically
- Open the app in your browser
- No CORS issues!

### Manual Start

#### Start the Backend Server

```bash
uvicorn server:app --reload
```

The server will start on `http://localhost:8000`

#### Start the Frontend Server

```bash
python3 -m http.server 3000
```

Then open `http://localhost:3000` in your browser

### 📌 Easy Access Options

**Option 1: Launcher Script**
- Double-click `launch.command` to open the app (servers must be running)

**Option 2: Bookmark**
- Open `app.html` in your browser and bookmark it
- Or bookmark `http://localhost:3000` directly

**Option 3: Desktop Shortcut**
- Right-click `start-servers.command` → "Make Alias"
- Move the alias to your Desktop
- Double-click to start everything

### Transcribe Audio

1. Click the upload area or drag and drop an audio file
2. **Choose processing options:**
   - **🧹 Clean text** (recommended, enabled by default) - Automatically removes repetitions and fixes formatting
   - **🤖 AI refinement** (optional) - Uses local AI (Ollama) for enhanced fluency
3. Click "Transcribe Audio"
4. Wait for processing (typically 1-2 minutes per hour of audio on M1 Pro)
5. View the transcription and download as a text file if needed

### Text Cleaning Feature

The app includes intelligent text cleaning to fix common transcription issues:
- **Removes repetitions**: Detects and removes repeated phrases (like "es de la cartería" repeated many times)
- **Fixes formatting**: Improves sentence structure and capitalization
- **Optional AI refinement**: For even better results, enable AI refinement (requires Ollama)

**Setting up AI Refinement (Optional):**
1. Install Ollama: https://ollama.ai
2. Pull a small model: `ollama pull llama3.2:1b` (or any model you prefer)
3. Enable "AI refinement" checkbox in the app

## API Endpoints

- `GET /` - API status and model information
- `GET /health` - Health check endpoint
- `POST /transcribe` - Upload audio file and receive transcription

## Performance

On an M1 Pro, expect:
- **Speed**: ~1 hour of audio transcribed in less than 2 minutes
- **Memory**: Efficient 4-bit quantization reduces RAM usage
- **Accuracy**: Near-Large model accuracy with Turbo model speed

## Troubleshooting

### "Cannot connect to API server"
- Make sure the backend server is running (`uvicorn server:app --reload`)
- Check that the server is running on port 8000
- Verify CORS settings in `server.py` if accessing from a different port

### Model download issues
- Ensure you have sufficient disk space (~3GB for the model)
- Check your internet connection
- The model downloads automatically on first use

### Slow performance
- Make sure you're using Apple Silicon (M1/M2/M3)
- Close other resource-intensive applications
- The first transcription may be slower as the model loads into memory

## Technical Details

- **Backend**: FastAPI with MLX Whisper
- **Model**: `mlx-community/whisper-large-v3-turbo`
- **Quantization**: 4-bit (default) for optimal performance/memory balance
- **Frontend**: Vanilla JavaScript, HTML5, CSS3

## License

For personal use as specified.

