import requests
import json

# First, let's log in with our test user
login_data = {
    'email': 'test@example.com',
    'password': 'test123'
}

# Create a session to maintain cookies
session = requests.Session()

# Log in
login_response = session.post('http://127.0.0.1:5000/login', data=login_data)

print("Login status code:", login_response.status_code)
print("Session cookies:", session.cookies)

if login_response.status_code == 200:
    print("Login successful!")
    
    # Check if we're redirected to the index page
    print("Login response URL:", login_response.url)
    print("Login response history:", login_response.history)
    
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
    if response.status_code == 200:
        print("Fraud detection response:", response.json())
    else:
        print("Fraud detection failed:", response.text[:500])
else:
    print("Login failed. Status code:", login_response.status_code)
    print("Response:", login_response.text[:500])  # Print first 500 chars