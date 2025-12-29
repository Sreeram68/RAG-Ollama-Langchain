# RAG-Ollama-Langchain

A Python project demonstrating how to interact with Ollama using both direct API calls and LangChain.

## Features

- Direct Ollama API integration using requests
- LangChain integration with Ollama
- Support for local LLM inference
- Example queries and prompt templates

## Prerequisites

- Python 3.14+
- Ollama installed and running
- Ollama model installed (e.g., llama3.2:3b)

## Setup

1. Clone the repository
2. Create virtual environment: `uv venv`
3. Activate environment: `.venv\Scripts\Activate.ps1`
4. Install dependencies: `uv pip install -r requirements.txt --native-tls`
   - Note: `--native-tls` flag is required for corporate networks with SSL inspection
5. Make sure Ollama is running

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

Run the direct API example: `uv run main.py`

Run the LangChain example: `uv run langchain_example.py`

## License

MIT License
