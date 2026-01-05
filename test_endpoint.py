import requests
import json

# Test the fake news endpoint
url = 'http://127.0.0.1:5000/detect_fake_news'
headers = {
    'Content-Type': 'application/json',
    'X-Requested-With': 'XMLHttpRequest'
}
data = {
    'text': 'This is a test article about breaking news'
}

try:
    response = requests.post(url, headers=headers, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 401:
        print("\n✅ Authentication required (expected - you need to log in first)")
    elif response.status_code == 200:
        result = response.json()
        print(f"\n✅ Success! Result: {result}")
except Exception as e:
    print(f"❌ Error: {e}")
