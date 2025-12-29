# LangChain example with Ollama
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate

try:
    # Initialize Ollama LLM
    llm = Ollama(
        model="llama3.2:3b",
        base_url="http://localhost:11434"
    )
    
    # Simple direct query
    print("Simple Query:")
    print("-" * 50)
    response = llm.invoke("What is RAG?")
    print(response)
    
    print("\n" + "=" * 50 + "\n")
    
    # Using a prompt template with LCEL (LangChain Expression Language)
    print("Using Prompt Template:")
    print("-" * 50)
    template = """You are a helpful AI assistant. Answer the following question concisely:
    
Question: {question}

Answer:"""
    
    prompt = PromptTemplate.from_template(template)
    
    # Create chain using LCEL (modern approach)
    chain = prompt | llm
    
    result = chain.invoke({"question": "What is RAG?"})
    print(result)
    
except Exception as e:
    print(f"Error: {e}")
    print(f"Error type: {type(e).__name__}")
    import traceback
    traceback.print_exc()
    print("\nMake sure:")
    print("1. Ollama is running (ollama serve)")
    print("2. Model llama3.2:3b is installed (ollama list)")
    print("3. LangChain packages are installed")

