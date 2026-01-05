import requests
import json

# Test the fake profile endpoint
url = "http://127.0.0.1:5000/detect_bot"

# Your profile data
data = {
    'followers': 390,
    'following': 566,
    'posts': 0,
    'bio_length': 5,
    'has_profile_pic': 1
}

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {response.headers.get('Content-Type')}")
    print(f"\nResponse Text (first 500 chars):")
    print(response.text[:500])
    
    if response.headers.get('Content-Type') == 'application/json':
        result = response.json()
        print(f"\nJSON Response:")
        print(json.dumps(result, indent=2))
    else:
        print("\n⚠️ Response is not JSON - likely an HTML error page")
        
except Exception as e:
    print(f"Error: {e}")
