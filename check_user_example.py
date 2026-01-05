import requests
import json

text = 'Scientists Discover a Floating Continent in the Middle of the Ocean. A viral social media post falsely claimed that researchers found a floating continent in the Pacific Ocean. No scientific organization has reported anything similar, and experts confirm the image circulating online was digitally edited.'

try:
    response = requests.post('http://127.0.0.1:5000/detect_fake_news', json={'text': text})
    data = response.json()
    result = data.get('result', {})
    print(f"IS_FAKE: {result.get('is_fake')}")
    print(f"PROB: {result.get('fake_probability')}")
except Exception as e:
    print(f"Error: {e}")
