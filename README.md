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
4. Install dependencies: `uv pip install -r requirements.txt`
5. Make sure Ollama is running

## Usage

Run the direct API example: `uv run main.py`

Run the LangChain example: `uv run langchain_example.py`

## License

MIT License
