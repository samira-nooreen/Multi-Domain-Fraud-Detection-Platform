"""
Automated server restart - kills old server and starts new one
"""
import subprocess
import time
import sys

print("=" * 70)
print("🔄 Automatic Server Restart")
print("=" * 70)
print()

# Step 1: Kill all Python processes
print("🛑 Step 1: Stopping all Python processes...")
try:
    result = subprocess.run(
        ['taskkill', '/F', '/IM', 'python.exe'],
        capture_output=True,
        text=True,
        creationflags=subprocess.CREATE_NO_WINDOW
    )
    
    if result.returncode == 0:
        print("✅ Successfully stopped Python processes")
    else:
        if "not found" in result.stdout.lower():
            print("✅ No Python processes were running")
        else:
            print(f"⚠️  {result.stdout}")
except Exception as e:
    print(f"⚠️  Could not stop processes: {e}")

print()
time.sleep(2)

# Step 2: Start the server
print("🚀 Step 2: Starting Flask server...")
print()
print("The server will open in a new window.")
print("Wait for 'Running on http://127.0.0.1:5000' message.")
print()

try:
    # Start server in new window
    subprocess.Popen(
        [sys.executable, 'app.py'],
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )
    
    print("✅ Server starting in new window...")
    print()
    time.sleep(3)
    
    # Step 3: Test the endpoint
    print("🧪 Step 3: Testing the endpoint...")
    print()
    
    import requests
    try:
        resp = requests.post(
            'http://localhost:5000/submit_report',
            data={'title': 'Test', 'description': 'Test'},
            allow_redirects=False,
            timeout=5
        )
        
        if resp.status_code in [302, 401, 405]:
            print("✅ SUCCESS! Route is working!")
            print(f"   Status: {resp.status_code}")
            print()
            print("🎉 The server has been restarted successfully!")
            print()
            print("Next steps:")
            print("  1. Open browser: http://localhost:5000")
            print("  2. LOGIN to your account")
            print("  3. Submit a report - it should work now!")
        elif resp.status_code == 404:
            print("⚠️  Route still not found")
            print("   The server might still be starting up")
            print("   Wait 10 more seconds and try again")
        else:
            print(f"⚠️  Unexpected status: {resp.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("⏳ Server is still starting...")
        print("   Wait a few seconds and refresh your browser")
    except Exception as e:
        print(f"⚠️  Test error: {e}")
        
except Exception as e:
    print(f"❌ Error starting server: {e}")
    print()
    print("Please start manually:")
    print("  python app.py")

print()
print("=" * 70)
input("\nPress Enter to exit...")
