from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# 1. Load the PDF
pdf_path = "policy doc.pdf"  # Replace with your file name
print("Loading PDF...")
loader = PyPDFLoader(pdf_path)
data = loader.load()
print(f"Loaded {len(data)} pages")

# 2. Split text into manageable chunks
print("Splitting text into chunks...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
chunks = text_splitter.split_documents(data)
print(f"Created {len(chunks)} chunks")

# 3. Create Local Vector Database (Embeddings)
# This stays 100% on your machine
print("Creating embeddings and vector database...")
embeddings = OllamaEmbeddings(model="mxbai-embed-large:latest")
vector_db = Chroma.from_documents(documents=chunks, embedding=embeddings)
print("Vector database created")

# 4. Initialize Gemma via Ollama
print("Initializing LLM...")
llm = ChatOllama(model="gemma3:12b")

# 5. Setup the Retrieval Chain (Modern LCEL approach)
print("Setting up retrieval chain...")
retriever = vector_db.as_retriever()

# Create a prompt template
prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

Context: {context}

Question: {question}

Answer:""")

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

# 6. Interactive Query Loop
print("\n" + "="*60)
print("RAG Chat Interface - Ask questions about your document")
print("Type 'q' or 'quit' to exit")
print("="*60 + "\n")

while True:
    # Get user input
    question = input("\n🤔 Your question: ").strip()
    
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
        print("\n🔍 Searching document and generating answer...")
        response = rag_chain.invoke(question)
        
        print(f"\n💡 Answer:\n{response}")
        print("\n" + "-"*60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Please try again with a different question.")


