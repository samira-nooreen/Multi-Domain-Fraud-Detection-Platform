"""
Test Insurance Fraud Detection Endpoint
"""
import requests

# Test the endpoint
url = "http://127.0.0.1:5000/detect_insurance"

# Test data
test_data = {
    "claim_amount": 200000,
    "claim_type": "Accident",
    "incident_description": "Minor scratch but claiming full damage. Urgent settlement needed.",
    "previous_claim_count": 5
}

print("Testing Insurance Fraud Detection Endpoint...")
print("=" * 60)
print(f"URL: {url}")
print(f"Data: {test_data}")
print("=" * 60)

try:
    response = requests.post(url, json=test_data)
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 200:
        result = response.json()
        if result.get('status') == 'success':
            print("\n✅ Endpoint is working correctly!")
            print(f"Fraud Probability: {result['result']['fraud_probability']:.2%}")
            print(f"Risk Level: {result['result']['risk_level']}")
            print(f"Recommendation: {result['result']['recommendation']}")
        else:
            print(f"\n❌ Error: {result.get('message')}")
    elif response.status_code == 401:
        print("\n⚠️  AUTHENTICATION REQUIRED!")
        print("You need to be logged in to use this endpoint.")
        print("Please login first at: http://127.0.0.1:5000/login")
    else:
        print(f"\n❌ Request failed with status {response.status_code}")
        
except requests.exceptions.ConnectionError:
    print("\n❌ Could not connect to server. Is it running?")
except Exception as e:
    print(f"\n❌ Error: {e}")
