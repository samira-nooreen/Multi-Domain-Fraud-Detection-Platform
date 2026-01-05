import requests
import json

# First, let's log in
login_data = {
    'email': 'samiranooreen02@gmail.com',
    'password': 'password123'
}

# Create a session to maintain cookies
session = requests.Session()

# Log in
login_response = session.post('http://127.0.0.1:5000/login', data=login_data)

print("Login status code:", login_response.status_code)
print("Login response:", login_response.text)

# Test data for credit card fraud detection
test_data = {
    "amount": 50000,
    "currency": "USD",
    "hour": 3,
    "distance_from_home": 150,
    "pin_entered": 0
}

# Send request to the credit card fraud detection endpoint
response = session.post('http://127.0.0.1:5000/detect_credit', json=test_data)

print("\nFraud detection status code:", response.status_code)
print("Fraud detection response:", response.json())