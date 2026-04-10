import requests

print("Testing /submit_report endpoint...")
print()

try:
    # Test without authentication
    resp = requests.post(
        'http://localhost:5000/submit_report',
        data={
            'title': 'Test Report',
            'description': 'Testing',
            'category': 'UPI Fraud'
        },
        allow_redirects=False
    )
    
    print(f"Status Code: {resp.status_code}")
    print(f"Content-Type: {resp.headers.get('Content-Type', 'N/A')}")
    print()
    
    if resp.status_code == 302 or resp.status_code == 301:
        print(f"Redirect Location: {resp.headers.get('Location', 'N/A')}")
        print("⚠️  Server is redirecting (likely to login page)")
        print()
        print("This means:")
        print("  1. You need to be logged in")
        print("  2. The route EXISTS and is working")
        print("  3. Just login and try again!")
    elif resp.status_code == 401:
        print("✅ Authentication required (this is correct)")
        print("Route is working, just need to login")
    elif resp.status_code == 404:
        print("❌ Route not found - server needs restart")
    elif resp.status_code == 500:
        print("❌ Server error - check console for details")
        print(f"Response: {resp.text[:300]}")
    else:
        print(f"Response: {resp.text[:300]}")
        
except requests.exceptions.ConnectionError:
    print("❌ Cannot connect to server!")
    print()
    print("Is the server running?")
    print("  Run: python app.py")
except Exception as e:
    print(f"❌ Error: {e}")
