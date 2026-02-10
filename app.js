const API_URL = 'http://localhost:8000';

// DOM elements
const fileInput = document.getElementById('fileInput');
const uploadArea = document.getElementById('uploadArea');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const removeFileBtn = document.getElementById('removeFile');
const transcribeBtn = document.getElementById('transcribeBtn');
const resultSection = document.getElementById('resultSection');
const transcriptionText = document.getElementById('transcriptionText');
const downloadBtn = document.getElementById('downloadBtn');
const errorMessage = document.getElementById('errorMessage');
const optionsSection = document.getElementById('optionsSection');
const cleanTextCheckbox = document.getElementById('cleanText');
const useAICheckbox = document.getElementById('useAI');
const aiRefinementHint = document.getElementById('aiRefinementHint');
const ollamaStatus = document.getElementById('ollamaStatus');
const statusIndicator = document.getElementById('statusIndicator');
const statusText = document.getElementById('statusText');

let selectedFile = null;
let ollamaRunning = false;
let availableModels = [];
let currentTranscription = "";

// Upload area click handler
uploadArea.addEventListener('click', () => {
    fileInput.click();
});

// File input change handler
fileInput.addEventListener('change', (e) => {
    handleFileSelect(e.target.files[0]);
});

// Drag and drop handlers
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('audio/')) {
        handleFileSelect(file);
    } else {
        showError('Please drop an audio file');
    }
});

// Handle file selection
function handleFileSelect(file) {
    if (!file) return;
    
    if (!file.type.startsWith('audio/')) {
        showError('Please select an audio file');
        return;
    }
    
    selectedFile = file;
    fileName.textContent = file.name;
    fileInfo.style.display = 'block';
    optionsSection.style.display = 'block';
    transcribeBtn.disabled = false;
    resultSection.style.display = 'none';
    hideError();
}

// Remove file handler
removeFileBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    selectedFile = null;
    fileInput.value = '';
    fileInfo.style.display = 'none';
    optionsSection.style.display = 'none';
    transcribeBtn.disabled = true;
    resultSection.style.display = 'none';
    hideError();
});

// Transcribe button handler
transcribeBtn.addEventListener('click', async () => {
    if (!selectedFile) return;
    
    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('clean_text', cleanTextCheckbox.checked.toString());
    formData.append('use_ai_refinement', useAICheckbox.checked.toString());
    
    // Show loading state
    transcribeBtn.disabled = true;
    transcribeBtn.querySelector('.btn-text').style.display = 'none';
    transcribeBtn.querySelector('.btn-loader').style.display = 'flex';
    hideError();
    resultSection.style.display = 'none';
    
    try {
        const response = await fetch(`${API_URL}/transcribe`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const ct = response.headers.get('content-type') || '';
            if (ct.includes('application/json')) {
                const err = await response.json();
                throw new Error(err.detail || 'Transcription failed');
            }
            if (response.status === 405) {
                throw new Error('Backend not responding correctly. Restart the server: uvicorn server:app --reload');
            }
            throw new Error(`Transcription failed (${response.status}). Is the backend running on port 8000?`);
        }
        
        const data = await response.json();
        
        // Display transcription
        const transcription = data.transcription || 'No transcription available';
        transcriptionText.value = transcription;
        currentTranscription = transcription; // Store for summaries
        resultSection.style.display = 'block';
        
        // Scroll to result
        resultSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        
    } catch (error) {
        console.error('Transcription error:', error);
        showError(`Error: ${error.message}`);
    } finally {
        // Reset button state
        transcribeBtn.disabled = false;
        transcribeBtn.querySelector('.btn-text').style.display = 'inline';
        transcribeBtn.querySelector('.btn-loader').style.display = 'none';
    }
});

// Download button handler
downloadBtn.addEventListener('click', () => {
    const text = transcriptionText.value;
    if (!text) return;
    
    const blob = new Blob([text], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = selectedFile 
        ? `${selectedFile.name.replace(/\.[^/.]+$/, '')}_transcription.txt`
        : 'transcription.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
});

// Error handling
function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
}

function hideError() {
    errorMessage.style.display = 'none';
}

// Check API health on load
async function checkAPIHealth() {
    try {
        const response = await fetch(`${API_URL}/health`);
        if (!response.ok) {
            showError('API server is not responding. Make sure the backend is running on port 8000.');
        }
    } catch (error) {
        showError('Cannot connect to API server. Make sure the backend is running on port 8000.');
    }
}

// Check health when page loads
checkAPIHealth();
checkOllamaStatus();

// Check Ollama status (will auto-start if needed)
async function checkOllamaStatus() {
    try {
        // Show starting status
        updateOllamaStatus(false, [], 'Starting Ollama automatically...');
        
        const response = await fetch(`${API_URL}/ollama/status`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) {
            updateOllamaStatus(false, [], 'Backend not available');
            setTimeout(() => checkOllamaStatus(), 5000);
            return;
        }
        
        const contentType = response.headers.get('content-type') || '';
        if (!contentType.includes('application/json')) {
            updateOllamaStatus(false, [], 'Backend not available. Start server: uvicorn server:app --reload');
            setTimeout(() => checkOllamaStatus(), 5000);
            return;
        }
        
        const data = await response.json();
        ollamaRunning = data.running || false;
        availableModels = data.available_models || [];
        
        if (ollamaRunning) {
            const modelCount = availableModels.length;
            const modelText = modelCount === 1 ? 'model' : 'models';
            const wasStarted = data.was_started || false;
            const statusMsg = wasStarted 
                ? `Ollama started automatically (${modelCount} ${modelText} available)` 
                : `Ollama running (${modelCount} ${modelText} available)`;
            updateOllamaStatus(true, availableModels, statusMsg);
            updateAIFeaturesHint('Optional - improves fluency with local AI');
            keepAIFeaturesEnabled();
        } else {
            // Still starting or failed - show status and retry
            const errorMsg = data.error || 'Starting Ollama...';
            updateOllamaStatus(false, [], errorMsg);
            updateAIFeaturesHint('Starting Ollama automatically. Features will work once ready.');
            keepAIFeaturesEnabled();
            
            // Retry after a delay if it's still starting
            if (errorMsg.includes('Starting') || errorMsg.includes('starting')) {
                setTimeout(() => checkOllamaStatus(), 3000);
            }
        }
    } catch (error) {
        console.error('Ollama status check failed:', error);
        updateOllamaStatus(false, [], 'Backend not available. Start server: uvicorn server:app --reload');
        updateAIFeaturesHint('Start the backend (port 8000) to use AI features.');
        keepAIFeaturesEnabled();
        setTimeout(() => checkOllamaStatus(), 5000);
    }
}

// Update Ollama status indicator
function updateOllamaStatus(running, models, message) {
    if (running) {
        statusIndicator.className = 'status-indicator status-running';
        statusIndicator.textContent = '●';
        statusText.textContent = message;
        ollamaStatus.className = 'ollama-status status-ok';
    } else if (message.includes('Starting') || message.includes('starting')) {
        statusIndicator.className = 'status-indicator status-starting';
        statusIndicator.textContent = '◐';
        statusText.textContent = message;
        ollamaStatus.className = 'ollama-status status-starting';
    } else {
        statusIndicator.className = 'status-indicator status-offline';
        statusIndicator.textContent = '○';
        statusText.textContent = message;
        ollamaStatus.className = 'ollama-status status-warning';
    }
}

// Update AI features hint
function updateAIFeaturesHint(message) {
    aiRefinementHint.textContent = message;
}

// Keep AI features always enabled - backend will start Ollama if needed
function keepAIFeaturesEnabled() {
    useAICheckbox.disabled = false;
    
    // Keep summary buttons enabled
    document.querySelectorAll('.btn-summary').forEach(btn => {
        btn.disabled = false;
    });
}

// Summary functionality
const summarySection = document.getElementById('summarySection');
const summaryResultSection = document.getElementById('summaryResultSection');
const summaryTitle = document.getElementById('summaryTitle');
const summaryResultContent = document.getElementById('summaryResultContent');
const closeSummaryBtn = document.getElementById('closeSummaryBtn');
const summaryButtons = document.querySelectorAll('.btn-summary');

// Store current transcription text for summaries
function setCurrentTranscription(text) {
    currentTranscription = text;
}

// Handle summary button clicks
summaryButtons.forEach(btn => {
    btn.addEventListener('click', async () => {
        const summaryType = btn.dataset.type;
        await requestSummary(summaryType, btn);
    });
});

// Close summary result
closeSummaryBtn.addEventListener('click', () => {
    summaryResultSection.style.display = 'none';
});

// Request summary from API
async function requestSummary(summaryType, buttonElement) {
    if (!currentTranscription || currentTranscription.length < 50) {
        showError('Transcription is too short to generate a summary. Please transcribe an audio file first.');
        return;
    }
    
    // Refresh Ollama status (will auto-start if needed)
    if (!ollamaRunning) {
        statusText.textContent = 'Starting Ollama...';
        await checkOllamaStatus();
    }
    
    // Show loading state
    const originalText = buttonElement.innerHTML;
    buttonElement.disabled = true;
    buttonElement.innerHTML = '<span class="spinner" style="width: 16px; height: 16px; border-width: 2px;"></span> Generating...';
    
    // Show summary result section with loading
    summaryTitle.textContent = getSummaryTitle(summaryType);
    summaryResultContent.innerHTML = '<div class="summary-loading"><div class="spinner"></div><p>Generating summary...</p></div>';
    summaryResultSection.style.display = 'block';
    summaryResultSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    
    try {
        const response = await fetch(`${API_URL}/summarize`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: currentTranscription,
                summary_type: summaryType
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Summary generation failed');
        }
        
        const data = await response.json();
        
        // Display summary
        displaySummary(data);
        
    } catch (error) {
        console.error('Summary error:', error);
        summaryResultContent.innerHTML = `<div class="error-message">Error: ${error.message}</div>`;
    } finally {
        // Reset button state
        buttonElement.disabled = false;
        buttonElement.innerHTML = originalText;
    }
}

// Display summary result
function displaySummary(data) {
    summaryTitle.textContent = data.title;
    
    if (data.summary_type === 'executive') {
        // Executive summary - plain text
        summaryResultContent.innerHTML = `<div class="summary-executive">${escapeHtml(data.content)}</div>`;
    } else {
        // Top ideas - bullet points
        const ideasList = Array.isArray(data.content) ? data.content : [data.content];
        const listItems = ideasList.map((idea, index) => 
            `<li>${escapeHtml(idea)}</li>`
        ).join('');
        summaryResultContent.innerHTML = `<ul class="summary-ideas">${listItems}</ul>`;
    }
}

// Get summary title
function getSummaryTitle(summaryType) {
    const titles = {
        'executive': 'Executive Summary',
        'top3': 'Top 3 Ideas',
        'top5': 'Top 5 Ideas',
        'top10': 'Top 10 Ideas'
    };
    return titles[summaryType] || 'Summary';
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

