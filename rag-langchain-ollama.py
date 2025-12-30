"""
RAG (Retrieval-Augmented Generation) Chat Interface
This script enables interactive Q&A with multiple PDF documents using:
- LangChain for orchestration
- Ollama for local LLM and embeddings
- ChromaDB for vector storage
"""

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
import os
import sys
from pathlib import Path
from typing import List


def load_pdf_documents(pdf_paths: List[str]) -> List[Document]:
    """
    Load multiple PDF documents and return combined document list.
    
    Args:
        pdf_paths: List of paths to PDF files
        
    Returns:
        List of Document objects containing page content and metadata
    """
    print("=" * 60)
    print("Loading PDF Documents...")
    print("=" * 60)
    
    all_documents = []
    successful_loads = 0
    
    for pdf_path in pdf_paths:
        if os.path.exists(pdf_path):
            try:
                print(f"\n📄 Loading: {pdf_path}")
                loader = PyPDFLoader(pdf_path)
                data = loader.load()
                all_documents.extend(data)
                successful_loads += 1
                print(f"   ✅ Loaded {len(data)} pages from {pdf_path}")
            except Exception as e:
                print(f"   ❌ Error loading {pdf_path}: {e}")
        else:
            print(f"   ⚠️  File not found: {pdf_path}")
    
    if not all_documents:
        print("\n❌ No documents loaded. Please check your PDF file paths.")
        sys.exit(1)
    
    print(f"\n✅ Total pages loaded: {len(all_documents)} from {successful_loads} file(s)")
    return all_documents


def split_documents(documents: List[Document], chunk_size: int = 1000, chunk_overlap: int = 100) -> List[Document]:
    """
    Split documents into smaller chunks for processing.
    
    Args:
        documents: List of Document objects to split
        chunk_size: Maximum size of each chunk
        chunk_overlap: Number of characters to overlap between chunks
        
    Returns:
        List of chunked Document objects
    """
    print("\n" + "=" * 60)
    print("Splitting text into chunks...")
    print("=" * 60)
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunks = text_splitter.split_documents(documents)
    print(f"✅ Created {len(chunks)} chunks")
    return chunks


def create_vector_database(chunks: List[Document], embedding_model: str = "mxbai-embed-large:latest"):
    """
    Create vector database from document chunks.
    
    Args:
        chunks: List of Document chunks
        embedding_model: Name of the Ollama embedding model
        
    Returns:
        Chroma vector database instance
    """
    print("\n" + "=" * 60)
    print("Creating embeddings and vector database...")
    print("=" * 60)
    print("⏳ This may take a few minutes depending on document size...")
    
    embeddings = OllamaEmbeddings(model=embedding_model)
    vector_db = Chroma.from_documents(documents=chunks, embedding=embeddings)
    print("✅ Vector database created")
    return vector_db


def initialize_llm(model_name: str = "gemma2:2b"):
    """
    Initialize the LLM for chat.
    
    Args:
        model_name: Name of the Ollama model to use
        
    Returns:
        ChatOllama instance
    """
    print("\n" + "=" * 60)
    print("Initializing LLM...")
    print("=" * 60)
    
    llm = ChatOllama(model=model_name)
    print("✅ LLM initialized")
    return llm


def create_rag_chain(vector_db, llm):
    """
    Create the RAG retrieval chain using LCEL.
    
    Args:
        vector_db: Chroma vector database
        llm: ChatOllama instance
        
    Returns:
        Configured RAG chain
    """
    print("\n" + "=" * 60)
    print("Setting up retrieval chain...")
    print("=" * 60)
    
    retriever = vector_db.as_retriever()
    
    # Create a prompt template
    prompt = ChatPromptTemplate.from_template(
        """Answer the following question based only on the provided context:

Context: {context}

Question: {question}

Answer:"""
    )
    
    # Helper function to format documents
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
    # Create the chain using LCEL
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    print("✅ Retrieval chain ready")
    return rag_chain


def run_interactive_chat(rag_chain, loaded_files: List[str]):
    """
    Run the interactive chat loop.
    
    Args:
        rag_chain: Configured RAG chain
        loaded_files: List of loaded PDF file names
    """
    print("\n" + "=" * 60)
    print("🤖 RAG Chat Interface - Multi-Document Q&A")
    print("=" * 60)
    print(f"📚 Loaded Documents: {', '.join(loaded_files)}")
    print("\n💡 Type your questions below")
    print("💡 Type 'q', 'quit', or 'exit' to close the application")
    print("=" * 60 + "\n")
    
    while True:
        # Get user input
        try:
            question = input("\n🤔 Your question: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n👋 Thank you for using RAG Chat! Goodbye!")
            break
        
        # Check for exit command
        if question.lower() in ['q', 'quit', 'exit']:
            print("\n👋 Thank you for using RAG Chat! Goodbye!")
            break
        
        # Skip empty questions
        if not question:
            print("⚠️  Please enter a question.")
            continue
        
        try:
            # Query the document
            print("\n🔍 Searching across all documents and generating answer...")
            response = rag_chain.invoke(question)
            
            print(f"\n💡 Answer:\n{response}")
            print("\n" + "-" * 60)
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again with a different question.")


def main():
    """Main entry point for the RAG chat application."""
    # Configuration
    PDF_FILES = [
        "policy doc.pdf",  # Add your PDF files here
        # "document2.pdf",
        # "document3.pdf",
    ]
    
    # Alternative: Load all PDFs from a directory
    # PDF_DIRECTORY = "documents"
    # PDF_FILES = [str(p) for p in Path(PDF_DIRECTORY).glob("*.pdf")]
    
    EMBEDDING_MODEL = "mxbai-embed-large:latest"
    LLM_MODEL = "gemma2:2b"
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 100
    
    try:
        # Step 1: Load PDF documents
        documents = load_pdf_documents(PDF_FILES)
        
        # Step 2: Split into chunks
        chunks = split_documents(documents, CHUNK_SIZE, CHUNK_OVERLAP)
        
        # Step 3: Create vector database
        vector_db = create_vector_database(chunks, EMBEDDING_MODEL)
        
        # Step 4: Initialize LLM
        llm = initialize_llm(LLM_MODEL)
        
        # Step 5: Create RAG chain
        rag_chain = create_rag_chain(vector_db, llm)
        
        # Step 6: Run interactive chat
        run_interactive_chat(rag_chain, PDF_FILES)
        
    except KeyboardInterrupt:
        print("\n\n👋 Application interrupted. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()




