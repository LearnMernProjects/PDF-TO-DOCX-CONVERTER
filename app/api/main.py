from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, HTMLResponse
import os
import uuid

from app.core.pdf_extract import extract_best_text
from app.core.pdf_contentType import group_content_under_headings
from app.core.pdf_toWord import build_word_document

app = FastAPI()

UPLOAD_DIR = "storage/uploadFiles"
OUTPUT_DIR = "storage/outputFiles"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


@app.get("/", response_class=HTMLResponse)
def upload_page():
    return """ 
#Writing basic code for frontend to submit pdf     
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>PDF to Word Converter | Convert PDFs Instantly</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            
            .container {
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                max-width: 600px;
                width: 100%;
                padding: 50px;
                text-align: center;
            }
            
            .header {
                margin-bottom: 40px;
            }
            
            .header h1 {
                color: #333;
                font-size: 2.5em;
                margin-bottom: 10px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            
            .header p {
                color: #666;
                font-size: 1.1em;
                font-weight: 300;
            }
            
            .upload-area {
                border: 3px dashed #667eea;
                border-radius: 15px;
                padding: 40px;
                margin: 30px 0;
                transition: all 0.3s ease;
                cursor: pointer;
                background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
            }
            
            .upload-area:hover {
                border-color: #764ba2;
                background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
            }
            
            .upload-area.dragover {
                border-color: #764ba2;
                background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
                transform: scale(1.02);
            }
            
            .upload-icon {
                font-size: 3em;
                margin-bottom: 15px;
            }
            
            .upload-text {
                color: #333;
                font-size: 1.2em;
                font-weight: 600;
                margin-bottom: 8px;
            }
            
            .upload-subtext {
                color: #999;
                font-size: 0.95em;
            }
            
            .file-input {
                display: none;
            }
            
            .button-group {
                display: flex;
                gap: 15px;
                margin-top: 30px;
            }
            
            .btn {
                flex: 1;
                padding: 14px 30px;
                border: none;
                border-radius: 10px;
                font-size: 1.05em;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            
            .btn-primary {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            
            .btn-primary:hover:not(:disabled) {
                transform: translateY(-2px);
                box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
            }
            
            .btn-primary:disabled {
                opacity: 0.5;
                cursor: not-allowed;
            }
            
            .btn-secondary {
                background: #f0f0f0;
                color: #333;
            }
            
            .btn-secondary:hover {
                background: #e0e0e0;
                transform: translateY(-2px);
            }
            
            .file-name {
                margin-top: 20px;
                padding: 15px;
                background: #f9f9f9;
                border-radius: 10px;
                color: #333;
                font-weight: 500;
            }
            
            .loading {
                display: none;
                text-align: center;
                margin: 30px 0;
            }
            
            .spinner {
                border: 4px solid #f0f0f0;
                border-top: 4px solid #667eea;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
                margin: 0 auto 15px;
            }
            
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            .loading-text {
                color: #667eea;
                font-weight: 600;
            }
            
            .success {
                display: none;
                padding: 20px;
                background: #d4edda;
                border: 2px solid #28a745;
                border-radius: 10px;
                color: #155724;
                margin: 20px 0;
            }
            
            .error {
                display: none;
                padding: 20px;
                background: #f8d7da;
                border: 2px solid #dc3545;
                border-radius: 10px;
                color: #721c24;
                margin: 20px 0;
            }
            
            .features {
                margin-top: 40px;
                padding-top: 40px;
                border-top: 2px solid #f0f0f0;
                display: grid;
                grid-template-columns: 1fr 1fr 1fr;
                gap: 20px;
            }
            
            .feature {
                color: #666;
            }
            
            .feature-icon {
                font-size: 2em;
                margin-bottom: 10px;
            }
            
            .feature-text {
                font-size: 0.9em;
                font-weight: 500;
            }
            
            @media (max-width: 600px) {
                .container {
                    padding: 30px;
                }
                
                .header h1 {
                    font-size: 1.8em;
                }
                
                .features {
                    grid-template-columns: 1fr;
                }
                
                .button-group {
                    flex-direction: column;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📄 PDF to Word</h1>
                <p>Convert your PDF files to Word documents instantly</p>
            </div>
            
            <div class="upload-area" id="uploadArea">
                <div class="upload-icon">⬆️</div>
                <div class="upload-text">Drag and drop your PDF here</div>
                <div class="upload-subtext">or click to browse</div>
                <input type="file" id="fileInput" class="file-input" accept=".pdf" />
            </div>
            
            <div class="file-name" id="fileName" style="display: none;"></div>
            
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <div class="loading-text">Converting your PDF...</div>
            </div>
            
            <div class="success" id="success">
                ✓ Conversion successful! Your file is ready to download.
            </div>
            
            <div class="error" id="error"></div>
            
            <div class="button-group">
                <button class="btn btn-primary" id="convertBtn" style="display: none;">Convert to Word</button>
                <button class="btn btn-secondary" id="clearBtn" style="display: none;">Clear</button>
            </div>
            
            <div class="features">
                <div class="feature">
                    <div class="feature-icon">⚡</div>
                    <div class="feature-text">Fast Conversion</div>
                </div>
                <div class="feature">
                    <div class="feature-icon">🔒</div>
                    <div class="feature-text">Secure & Private</div>
                </div>
                <div class="feature">
                    <div class="feature-icon">✨</div>
                    <div class="feature-text">High Quality</div>
                </div>
            </div>
        </div>
        
        <script>
            const uploadArea = document.getElementById('uploadArea');
            const fileInput = document.getElementById('fileInput');
            const fileName = document.getElementById('fileName');
            const convertBtn = document.getElementById('convertBtn');
            const clearBtn = document.getElementById('clearBtn');
            const loading = document.getElementById('loading');
            const success = document.getElementById('success');
            const error = document.getElementById('error');
            
            let selectedFile = null;
            
            // Click to select file
            uploadArea.addEventListener('click', () => fileInput.click());
            
            // File input change
            fileInput.addEventListener('change', (e) => {
                if (e.target.files.length > 0) {
                    selectedFile = e.target.files[0];
                    displayFileName();
                }
            });
            
            // Drag and drop
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
                
                const files = e.dataTransfer.files;
                if (files.length > 0) {
                    const file = files[0];
                    if (file.type === 'application/pdf') {
                        selectedFile = file;
                        fileInput.files = files;
                        displayFileName();
                    } else {
                        showError('Please drop a PDF file');
                    }
                }
            });
            
            function displayFileName() {
                if (selectedFile) {
                    const size = (selectedFile.size / 1024 / 1024).toFixed(2);
                    fileName.textContent = `📎 ${selectedFile.name} (${size} MB)`;
                    fileName.style.display = 'block';
                    convertBtn.style.display = 'flex';
                    clearBtn.style.display = 'flex';
                    success.style.display = 'none';
                    error.style.display = 'none';
                }
            }
            
            function showError(message) {
                error.textContent = 'error: ' + message;
                error.style.display = 'block';
                success.style.display = 'none';
            }
            
            clearBtn.addEventListener('click', () => {
                selectedFile = null;
                fileInput.value = '';
                fileName.style.display = 'none';
                convertBtn.style.display = 'none';
                clearBtn.style.display = 'none';
                success.style.display = 'none';
                error.style.display = 'none';
            });
            
            convertBtn.addEventListener('click', async () => {
                if (!selectedFile) return;
                
                const formData = new FormData();
                formData.append('file', selectedFile);
                
                loading.style.display = 'block';
                convertBtn.disabled = true;
                clearBtn.disabled = true;
                success.style.display = 'none';
                error.style.display = 'none';
                
                try {
                    const response = await fetch('/upload', {
                        method: 'POST',
                        body: formData
                    });
                    
                    if (response.ok) {
                        const blob = await response.blob();
                        const url = window.URL.createObjectURL(blob);
                        const a = document.createElement('a');
                        a.href = url;
                        a.download = selectedFile.name.replace('.pdf', '.docx');
                        document.body.appendChild(a);
                        a.click();
                        window.URL.revokeObjectURL(url);
                        document.body.removeChild(a);
                        
                        loading.style.display = 'none';
                        success.style.display = 'block';
                        clearBtn.disabled = false;
                    } else {
                        throw new Error('Conversion failed');
                    }
                } catch (err) {
                    loading.style.display = 'none';
                    showError('Failed to convert PDF. Please try again.');
                    convertBtn.disabled = false;
                    clearBtn.disabled = false;
                }
            });
        </script>
    </body>
    </html>
    """


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        pdf_id = str(uuid.uuid4())
        pdf_path = f"{UPLOAD_DIR}/{pdf_id}.pdf"
        docx_path = f"{OUTPUT_DIR}/{pdf_id}.docx"

        # Save uploaded PDF
        with open(pdf_path, "wb") as f:
            f.write(await file.read())

        # Pipeline
        text, _ = extract_best_text(pdf_path)
        structured = group_content_under_headings(text)
        build_word_document(structured, docx_path)

        # Return generated Word file
        return FileResponse(
            path=docx_path,
            filename="converted.docx",
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    except Exception as e:
        print(f"Error during conversion: {str(e)}")
        import traceback
        traceback.print_exc()
        raise
