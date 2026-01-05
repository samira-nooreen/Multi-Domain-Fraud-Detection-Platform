import requests
import json

url = 'http://127.0.0.1:5000/detect_phishing'
data = {'url': 'http://secure-login-update.xyz'}

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print("Response:")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"Error: {e}")
