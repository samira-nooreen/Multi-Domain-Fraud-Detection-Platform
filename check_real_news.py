import requests
import json

text = 'Officials report 3.5% increase in economic growth this year. The Federal Reserve announced new policy measures to address inflation concerns.'

try:
    response = requests.post('http://127.0.0.1:5000/detect_fake_news', json={'text': text})
    data = response.json()
    result = data.get('result', {})
    print(f"IS_FAKE: {result.get('is_fake')}")
    print(f"PROB: {result.get('fake_probability')}")
except Exception as e:
    print(f"Error: {e}")
