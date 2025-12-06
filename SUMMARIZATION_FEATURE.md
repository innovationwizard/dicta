# Summarization Feature

## Overview

After transcribing and cleaning your audio, you can now generate intelligent summaries and extract key ideas using AI.

## Features

### 1. 📄 Executive Summary
Generate a concise executive summary (2-4 paragraphs) that captures the main points and key topics discussed.

### 2. 💡 Top 10 Ideas
Extract the 10 most important ideas, insights, decisions, or key points as bullet points.

### 3. 💡 Top 5 Ideas
Extract the 5 most important ideas as bullet points.

### 4. 💡 Top 3 Ideas
Extract the 3 most important ideas as bullet points.

## How to Use

1. **Transcribe your audio** (as usual)
   - Upload audio file
   - Enable text cleaning (recommended)
   - Optionally enable AI refinement
   - Click "Transcribe Audio"

2. **After transcription is complete**, you'll see summary buttons below the transcription:
   - 📄 Executive Summary
   - 💡 Top 10 Ideas
   - 💡 Top 5 Ideas
   - 💡 Top 3 Ideas

3. **Click any summary button** to generate that type of summary
   - The app will use your Ollama models (Qwen2.5:7b-instruct by default)
   - Processing typically takes 10-30 seconds
   - Results appear in a new section below

4. **View your summary**
   - Executive summaries appear as formatted text
   - Key ideas appear as numbered bullet points
   - You can close the summary and generate a different one

## Technical Details

### Backend
- **Endpoint**: `POST /summarize`
- **Uses**: Ollama AI models (Qwen2.5:7b-instruct prioritized)
- **Processing**: AI-powered summarization and key idea extraction

### Frontend
- Summary buttons appear after transcription
- Loading indicators during generation
- Formatted display for different summary types
- Easy to close and regenerate

## Requirements

- Ollama must be running (same as AI refinement)
- At least one model installed (Qwen2.5:7b-instruct recommended)
- Transcription text must be at least 50 characters

## Tips

- **Best results**: Use AI refinement on transcription first, then summarize
- **Multiple summaries**: You can generate all 4 types of summaries from the same transcription
- **Processing time**: Depends on text length and model size (10-30 seconds typical)

## Example Workflow

1. Upload audio → Transcribe with cleaning and AI refinement
2. Review cleaned transcription
3. Click "📄 Executive Summary" for a quick overview
4. Click "💡 Top 5 Ideas" for key takeaways
5. Download or copy as needed

Enjoy your new summarization capabilities! 🚀

