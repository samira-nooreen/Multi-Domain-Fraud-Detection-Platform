import requests
import json

try:
    response = requests.post('http://127.0.0.1:5000/detect_fake_news', json={'text': 'SHOCKING: Lemon juice cures all cancer! Doctors HATE this!'})
    data = response.json()
    print(f"IS_FAKE_RESULT: {data.get('result', {}).get('is_fake')}")
except Exception as e:
    print(f"Error: {e}")
