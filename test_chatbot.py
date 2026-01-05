import requests
import json

# Test the chatbot endpoint
url = "http://127.0.0.1:5000/api/chat"

test_messages = [
    "hello",
    "help",
    "tell me about UPI fraud",
    "what is fake news detection",
    "how does bot detection work"
]

print("Testing MDFDP Bot API...\n")

for message in test_messages:
    print(f"User: {message}")
    
    try:
        response = requests.post(url, json={"message": message})
        data = response.json()
        
        if data.get('status') == 'success':
            print(f"Bot: {data.get('response')}")
        else:
            print(f"Error: {data.get('message', 'Unknown error')}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("-" * 60)
