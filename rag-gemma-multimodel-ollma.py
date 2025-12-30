import base64
import os
from io import BytesIO
from pdf2image import convert_from_path
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.messages import HumanMessage
from langchain_chroma import Chroma
from langchain_core.documents import Document

# --- CONFIGURATION ---
PDF_FILE = "C:\\python\\projects\\RAG-PDF-FILES\\Atomic habits 1753703096175.pdf"
MODEL_VISION = "gemma3:12b"  # Fixed: gemma3:12b doesn't exist
MODEL_EMBED = "mxbai-embed-large:latest"  # For the database
CHROMA_PATH = "local_rag_db"
# CRITICAL FIX: Explicitly set Poppler path
POPPLER_PATH = r"C:\Users\SRETH\AppData\Local\Programs\poppler\poppler-25.12.0\Library\bin"

def image_to_base64(pil_image):
    """Convert PIL image to base64 string."""
    buffered = BytesIO()
    pil_image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

# 1. EXTRACT TEXT FROM SCANNED PDF (USING VISION)
def ingest_pdf(file_path):
    """Extract text from PDF using vision model."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"PDF file not found: {file_path}")
    
    print(f"Reading {file_path}...")
    try:
        # CRITICAL FIX: Add poppler_path parameter here!
        pages = convert_from_path(
            file_path, 
            dpi=150,
            poppler_path=POPPLER_PATH
        )
        print(f"✓ Loaded {len(pages)} pages from PDF")
    except Exception as e:
        print(f"✗ Error converting PDF: {e}")
        print(f"Poppler path: {POPPLER_PATH}")
        print(f"Poppler exists: {os.path.exists(POPPLER_PATH)}")
        raise
    
    vision_llm = ChatOllama(model=MODEL_VISION, temperature=0)
    documents = []

    for i, page in enumerate(pages):
        print(f"Processing Page {i+1}/{len(pages)} with vision model...")
        img_b64 = image_to_base64(page)
        
        # Ask model to transcribe the image
        msg = HumanMessage(content=[
            {"type": "text", "text": "Transcribe all text from this page exactly. Output only the text."},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
        ])
        
        try:
            response = vision_llm.invoke([msg])
            documents.append(Document(
                page_content=response.content, 
                metadata={"page": i+1, "source": file_path}
            ))
            print(f"  ✓ Page {i+1} processed")
        except Exception as e:
            print(f"  ✗ Error processing page {i+1}: {e}")
            continue
    
    print(f"\n✓ Successfully processed {len(documents)} pages")
    return documents

# 2. CREATE LOCAL VECTOR STORE
def create_rag_db(docs):
    """Create Chroma vector database from documents."""
    if not docs:
        raise ValueError("No documents to create database from")
    
    print(f"\nCreating vector database with {len(docs)} documents...")
    embeddings = OllamaEmbeddings(model=MODEL_EMBED)
    vector_db = Chroma.from_documents(
        documents=docs, 
        embedding=embeddings, 
        persist_directory=CHROMA_PATH
    )
    print(f"✓ Database created at {CHROMA_PATH}")
    return vector_db

# 3. QUERY THE RAG SYSTEM
def query_rag(query):
    """Query the RAG system with a question."""
    if not os.path.exists(CHROMA_PATH):
        raise FileNotFoundError(f"Database not found at {CHROMA_PATH}. Run ingestion first.")
    
    print(f"\n{'='*60}")
    print(f"QUERY: {query}")
    print(f"{'='*60}")
    
    embeddings = OllamaEmbeddings(model=MODEL_EMBED)
    vector_db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    
    # Retrieve top 3 relevant pages
    results = vector_db.similarity_search(query, k=3)
    
    if not results:
        print("No relevant documents found.")
        return
    
    # Show sources
    print(f"\n✓ Found {len(results)} relevant pages:")
    for i, doc in enumerate(results, 1):
        print(f"  {i}. Page {doc.metadata.get('page', 'unknown')}")
    
    context = "\n\n".join([doc.page_content for doc in results])
    
    # Final answer using LLM
    llm = ChatOllama(model=MODEL_VISION, temperature=0.3)
    prompt = f"""Based on the following context, answer the question. If the answer is not in the context, say so.

Context:
{context}

Question: {query}

Answer:"""
    
    print(f"\n{'='*60}")
    print("GENERATING ANSWER...")
    print(f"{'='*60}")
    
    final_response = llm.invoke(prompt)
    print(f"\n--- ANSWER ---")
    print(final_response.content)
    print(f"{'='*60}\n")

# --- EXECUTION ---
if __name__ == "__main__":
    print("="*60)
    print("RAG SYSTEM - PDF Analysis with Vision Model")
    print("="*60)
    
    # Verify Poppler installation
    if not os.path.exists(POPPLER_PATH):
        print(f"\n✗ WARNING: Poppler not found at {POPPLER_PATH}")
        print("Please verify the path and update POPPLER_PATH in the script")
        exit(1)
    else:
        print(f"\n✓ Poppler found at {POPPLER_PATH}")
    
    # Run ingestion only if DB doesn't exist
    if not os.path.exists(CHROMA_PATH):
        print("\n✗ Database not found. Starting ingestion...")
        try:
            extracted_docs = ingest_pdf(PDF_FILE)
            create_rag_db(extracted_docs)
            print("\n✓ Ingestion complete!\n")
        except Exception as e:
            print(f"\n✗ Ingestion failed: {e}")
            exit(1)
    else:
        print(f"\n✓ Using existing database at {CHROMA_PATH}\n")
    
    # Example queries
    query_rag("What is the main topic of this document?")
    
    # Uncomment for more queries:
    # query_rag("What are the key principles discussed?")
    # query_rag("Who is the author?")