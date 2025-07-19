#!/usr/bin/env python3

import requests
import json

BASE_URL = "http://localhost:8000"

def test_chat_completion():
    """Test the chat completions endpoint"""
    print("Testing chat completions...")
    
    payload = {
        "model": "google-gla:gemini-1.5-flash",
        "messages": [
            {"role": "user", "content": "Hello! Can you tell me a short joke?"}
        ],
        "temperature": 0.7
    }
    
    response = requests.post(f"{BASE_URL}/v1/chat/completions", json=payload)
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Chat completion successful!")
        print(f"Response: {result['choices'][0]['message']['content']}")
        print(f"Usage: {result['usage']}")
    else:
        print(f"❌ Chat completion failed: {response.status_code}")
        print(response.text)

def test_streaming():
    """Test streaming chat completions"""
    print("\nTesting streaming...")
    
    payload = {
        "model": "google-gla:gemini-1.5-flash",
        "messages": [
            {"role": "user", "content": "Count from 1 to 5"}
        ],
        "stream": True
    }
    
    response = requests.post(f"{BASE_URL}/v1/chat/completions", json=payload, stream=True)
    
    if response.status_code == 200:
        print("✅ Streaming response:")
        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                if line_str.startswith('data: '):
                    data = line_str[6:]
                    if data != '[DONE]':
                        try:
                            chunk = json.loads(data)
                            if 'choices' in chunk and chunk['choices']:
                                delta = chunk['choices'][0].get('delta', {})
                                if 'content' in delta:
                                    print(delta['content'], end='', flush=True)
                        except json.JSONDecodeError:
                            pass
        print("\n")
    else:
        print(f"❌ Streaming failed: {response.status_code}")

def test_models():
    """Test the models endpoint"""
    print("Testing models endpoint...")
    
    response = requests.get(f"{BASE_URL}/v1/models")
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Models endpoint successful!")
        print(f"Available models: {[model['id'] for model in result['data']]}")
    else:
        print(f"❌ Models endpoint failed: {response.status_code}")

if __name__ == "__main__":
    print("OpenAI Compatibility Layer Test")
    print("=" * 40)
    print("Make sure the server is running with: uv run python openai_compat.py")
    print()
    
    try:
        test_models()
        test_chat_completion()
        test_streaming()
        print("\n🎉 All tests completed!")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure it's running on localhost:8000")