import requests
import time
import sys

BASE_URL = "http://127.0.0.1:5000"

def wait_for_server():
    print("Waiting for server to start...")
    for i in range(10):
        try:
            response = requests.get(f"{BASE_URL}/login")
            if response.status_code == 200:
                print("Server is up!")
                return True
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(2)
    print("Server failed to start.")
    return False

def test_endpoints():
    endpoints = [
        "/login",
        "/signup",
        "/api/status",
        "/chatbot-test",
        "/neon-demo"
    ]
    
    failed = []
    for endpoint in endpoints:
        try:
            url = f"{BASE_URL}{endpoint}"
            print(f"Testing {url}...", end=" ")
            response = requests.get(url)
            if response.status_code == 200:
                print("✅ OK")
            else:
                print(f"❌ Failed (Status: {response.status_code})")
                failed.append(endpoint)
        except Exception as e:
            print(f"❌ Error: {e}")
            failed.append(endpoint)
            
    return failed

if __name__ == "__main__":
    if wait_for_server():
        failed = test_endpoints()
        if failed:
            print(f"\nFailed endpoints: {failed}")
            sys.exit(1)
        else:
            print("\nAll basic endpoints are accessible.")
            sys.exit(0)
    else:
        sys.exit(1)
