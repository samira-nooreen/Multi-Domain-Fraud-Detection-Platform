import requests
import json

# Test data for credit card fraud detection
test_data = {
    "amount": 50000,
    "currency": "USD",
    "hour": 3,
    "distance_from_home": 150,
    "pin_entered": 0
}

# Send request to the credit card fraud detection endpoint
response = requests.post('http://127.0.0.1:5000/detect_credit', json=test_data)

print("Response status code:", response.status_code)
print("Response JSON:", response.json())