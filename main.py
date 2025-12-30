# Python test - works now!
import requests
import json

try:
    # Use the correct Ollama API endpoint
    response = requests.post('http://localhost:11434/api/chat', json={
        'model': 'gemma3:12b',
        'messages': [
            {
                'role': 'user',
                'content': 'What is RAG?'
            }
        ],
        'stream': False
    })
    
    # Check if request was successful
    response.raise_for_status()
    
    # Parse the response
    result = response.json()
    
    # Debug: print the entire response to see structure
    print("Full response:")
    print(json.dumps(result, indent=2))
    
    # Get the response content
    if 'message' in result and 'content' in result['message']:
        print("\nAnswer:")
        print(result['message']['content'])
    else:
        print("\nAvailable keys in response:", list(result.keys()))
        
except requests.exceptions.ConnectionError:
    print("Error: Could not connect to Ollama. Make sure Ollama is running on localhost:11434")
except requests.exceptions.RequestException as e:
    print(f"Request error: {e}")
except KeyError as e:
    print(f"KeyError: {e}")
    print("Response structure:", result)
except Exception as e:
    print(f"Unexpected error: {e}")
