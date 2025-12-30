# RAG-Ollama-Langchain

A Python project demonstrating Retrieval-Augmented Generation (RAG) with Ollama using both direct API calls and LangChain, including multimodal vision capabilities for PDF processing.

## Features

- **Direct Ollama API integration** using requests
- **LangChain integration** with Ollama for RAG workflows
- **Multimodal Vision PDF Processing** - Extract text from scanned PDFs using vision models
- **Vector Database Storage** - ChromaDB for efficient document retrieval
- **Local LLM inference** - No external API costs
- **PDF-to-Image conversion** with Poppler support
- Example queries and prompt templates

## Prerequisites

- **Python 3.14+**
- **Ollama** installed and running ([Download Ollama](https://ollama.ai/))
- **Ollama models** installed:
  - Text model: `llama3.2:3b` or similar
  - Vision model: `llama3.2-vision:11b` or `gemma2:12b` (for PDF processing)
  - Embedding model: `mxbai-embed-large:latest`
- **Poppler** (required for PDF to image conversion)
  - Windows: Download from [poppler releases](https://github.com/oschwartz10612/poppler-windows/releases/)
  - Extract and note the `bin` folder path (e.g., `C:\...\poppler\Library\bin`)
  - **Important**: Update `POPPLER_PATH` in `rag-gemma-multimodel-ollma.py` with your actual path

## Setup

### 1. Clone and Install Dependencies

```powershell
# Clone the repository
git clone https://github.com/Sreeram68/RAG-Ollama-Langchain.git
cd RAG-Ollama-Langchain

# Create virtual environment
uv venv

# Activate environment
.venv\Scripts\Activate.ps1

# Install dependencies
uv pip install -r requirements.txt --native-tls
```

**Note**: `--native-tls` flag is required for corporate networks with SSL inspection.

**SSL Certificate Issues?** If you encounter SSL errors, try:
```powershell
uv pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org
```

### 2. Install Ollama Models

```powershell
# Install required models
ollama pull llama3.2:3b           # Text generation
ollama pull llama3.2-vision:11b   # Vision/PDF processing
ollama pull mxbai-embed-large     # Embeddings
```

### 3. Install Poppler (Windows)

1. Download Poppler: https://github.com/oschwartz10612/poppler-windows/releases/
2. Extract to a location (e.g., `C:\Users\YourName\AppData\Local\Programs\poppler`)
3. Update `POPPLER_PATH` in `rag-gemma-multimodel-ollma.py`:
   ```python
   POPPLER_PATH = r"C:\Users\YourName\AppData\Local\Programs\poppler\poppler-25.12.0\Library\bin"
   ```
4. (Optional) Add Poppler to PATH using `setpath.ps1`:
   ```powershell
   .\setpath.ps1
   ```

### 4. Configure PDF Path

Update the PDF file path in `rag-gemma-multimodel-ollma.py`:
```python
PDF_FILE = "C:\\path\\to\\your\\document.pdf"
```

### Optional: Customize PowerShell Prompt

To show the virtual environment name as a prefix in your terminal:

**Option 1: One-time per session**
```powershell
. .\setup_prompt.ps1
```

**Option 2: Permanent (for all PowerShell sessions)**
1. Run: `notepad $PROFILE`
2. Add this line: `. C:\python\projects\RAG-Ollama-Langchain\setup_prompt.ps1`
3. Save and restart PowerShell

Alternatively, check if your virtual environment is already showing a prefix after activation. By default, Python's venv shows `(.venv)` prefix.

## Usage

### Basic Examples

**Direct Ollama API:**
```powershell
uv run main.py
```

**LangChain Integration:**
```powershell
uv run langchain_example.py
```

**Traditional RAG (PyPDF):**
```powershell
uv run rag-langchain-ollama.py
```

### Multimodal Vision RAG (PDF Processing)

The `rag-gemma-multimodel-ollma.py` script uses vision models to extract text from scanned or image-based PDFs:

```powershell
uv run rag-gemma-multimodel-ollma.py
```

**How it works:**
1. **Converts PDF pages to images** using Poppler
2. **Extracts text using vision model** (gemma3:12b or llama3.2-vision)
3. **Creates vector embeddings** and stores in ChromaDB
4. **Enables semantic search** over the document
5. **Answers questions** using retrieved context

**Example queries:**
```python
query_rag("What is the main topic of this document?")
query_rag("What are the key principles discussed?")
query_rag("Who is the author?")
```

**Features:**
- ? Works with **scanned PDFs** and images
- ? Uses **local models** (no API costs)
- ? **Persistent vector database** (runs ingestion only once)
- ? **ChromaDB** for efficient retrieval
- ? **Configurable models** and DPI settings

### Configuration Options

In `rag-gemma-multimodel-ollma.py`:

```python
# Model configuration
MODEL_VISION = "gemma3:12b"           # Vision model for PDF extraction
MODEL_EMBED = "mxbai-embed-large"     # Embedding model
CHROMA_PATH = "local_rag_db"          # Database location
PDF_FILE = "path/to/your/file.pdf"    # Your PDF file
POPPLER_PATH = r"C:\...\bin"          # Poppler installation path
```

## Project Structure

```
RAG-Ollama-Langchain/
??? main.py                          # Direct Ollama API example
??? langchain_example.py             # Basic LangChain integration
??? rag-langchain-ollama.py          # Traditional RAG with PyPDF
??? rag-gemma-multimodel-ollma.py    # Multimodal Vision RAG ?
??? requirements.txt                 # Python dependencies
??? setpath.ps1                      # Windows PATH configuration
??? setup_prompt.ps1                 # PowerShell prompt customization
??? .gitignore                       # Git ignore rules
??? local_rag_db/                    # ChromaDB vector store (excluded from git)
```

## Troubleshooting

### Poppler Not Found
```
Error: Unable to get page count. Is poppler installed and in PATH?
```
**Solution**: Ensure `POPPLER_PATH` in the script points to the correct `bin` folder.

### SSL Certificate Errors
```
[SSL: CERTIFICATE_VERIFY_FAILED]
```
**Solution**: Use `--trusted-host` flag or update certificates:
```powershell
python -m pip install --upgrade certifi
```

### Ollama Connection Issues
```
Error: Failed to connect to Ollama
```
**Solution**: Ensure Ollama is running:
```powershell
ollama serve
```

### Model Not Found
```
Error: model 'gemma3:12b' not found
```
**Solution**: Pull the required model:
```powershell
ollama pull gemma3:12b
```

## Technologies Used

- **[Ollama](https://ollama.ai/)** - Local LLM runtime
- **[LangChain](https://www.langchain.com/)** - LLM application framework
- **[ChromaDB](https://www.trychroma.com/)** - Vector database
- **[Poppler](https://poppler.freedesktop.org/)** - PDF rendering library
- **[pdf2image](https://github.com/Belval/pdf2image)** - PDF to image conversion
- **[Pillow](https://python-pillow.org/)** - Image processing

## License

MIT License
