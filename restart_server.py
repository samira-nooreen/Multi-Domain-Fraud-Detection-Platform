"""
Quick fix script - Restart the Flask server to apply changes
"""
import subprocess
import time
import sys
import os

print("=" * 70)
print("🔄 Flask Server Restart Helper")
print("=" * 70)
print()

print("⚠️  IMPORTANT: The server needs to be restarted!")
print()
print("The 'Server error' you're seeing is because:")
print("  1. The server is running OLD code")
print("  2. New fixes haven't been loaded yet")
print()
print("📋 Steps to fix:")
print()
print("Step 1: Stop the current server")
print("  - Go to the terminal where app.py is running")
print("  - Press Ctrl + C")
print("  - Wait for it to stop")
print()
print("Step 2: Restart the server")
print("  - Run: python app.py")
print("  - Wait for: 'Running on http://127.0.0.1:5000'")
print()
print("Step 3: Test the report submission")
print("  - Open browser: http://localhost:5000")
print("  - Make sure you're LOGGED IN")
print("  - Fill out report form")
print("  - Click 'Submit Report'")
print()
print("=" * 70)
print()

# Check if we can restart automatically
answer = input("Do you want me to try stopping and restarting the server? (y/n): ")

if answer.lower() == 'y':
    print()
    print("🛑 Attempting to stop existing Python processes...")
    print()
    
    # Try to stop Python processes running app.py
    try:
        # Get all python processes
        result = subprocess.run(
            ['tasklist', '/FI', 'IMAGENAME eq python.exe'],
            capture_output=True,
            text=True
        )
        
        if 'python.exe' in result.stdout:
            print("⚠️  Found Python processes running.")
            print()
            print("Please manually stop the server:")
            print("  1. Find the terminal running app.py")
            print("  2. Press Ctrl + C")
            print("  3. Then run: python app.py")
            print()
        else:
            print("✅ No Python processes found.")
            print()
            print("Starting server now...")
            print()
            
            # Start the server
            server_process = subprocess.Popen(
                [sys.executable, 'app.py'],
                cwd=os.getcwd(),
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            
            print(f"✅ Server started with PID: {server_process.pid}")
            print()
            print("Waiting 5 seconds for server to start...")
            time.sleep(5)
            print()
            print("🌐 Open your browser to: http://localhost:5000")
            print("🔐 Make sure to LOG IN before submitting reports!")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print()
        print("Please restart the server manually:")
        print("  1. Stop current server (Ctrl + C)")
        print("  2. Run: python app.py")

else:
    print()
    print("👍 No problem! Please restart the server manually:")
    print()
    print("  1. Stop current server: Ctrl + C")
    print("  2. Start server: python app.py")
    print("  3. Open browser: http://localhost:5000")
    print("  4. Login and test report submission")

print()
print("=" * 70)
