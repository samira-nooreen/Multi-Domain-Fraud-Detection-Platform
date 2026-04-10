"""
Diagnostic script for report submission issues
Run this to check if the submit_report endpoint is working correctly
"""
import requests
import sys

def test_report_submission():
    print("=" * 70)
    print("🔍 Report Submission Diagnostic Tool")
    print("=" * 70)
    print()
    
    # Base URL
    base_url = "http://localhost:5000"
    
    print(f"📡 Testing endpoint: {base_url}/submit_report")
    print()
    
    # Test 1: Check if server is running
    print("Test 1: Checking if server is running...")
    try:
        response = requests.get(base_url)
        if response.status_code == 200:
            print("✅ Server is running")
        else:
            print(f"⚠️  Server returned status code: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to server!")
        print()
        print("📋 Solution:")
        print("   1. Start the Flask server: python app.py")
        print("   2. Wait for 'Running on http://127.0.0.1:5000' message")
        print("   3. Then try submitting a report again")
        return False
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False
    
    print()
    
    # Test 2: Try to submit report without login (should get 401)
    print("Test 2: Testing authentication requirement...")
    try:
        test_data = {
            'title': 'Test Report',
            'description': 'This is a diagnostic test report',
            'source': 'Diagnostic Tool',
            'category': 'UPI Fraud'
        }
        
        response = requests.post(f"{base_url}/submit_report", data=test_data)
        
        print(f"   Response Status: {response.status_code}")
        print(f"   Content-Type: {response.headers.get('Content-Type', 'N/A')}")
        
        if response.status_code == 401:
            print("✅ Authentication is properly required (got 401)")
        elif response.status_code == 302:
            print("⚠️  Got redirect (302) - this is normal for web requests")
        else:
            print(f"⚠️  Unexpected status code: {response.status_code}")
            
        # Check content type
        content_type = response.headers.get('Content-Type', '')
        if 'text/html' in content_type:
            print("⚠️  Response is HTML (not JSON)")
            print("   This is expected if not logged in")
        elif 'application/json' in content_type:
            print("✅ Response is JSON")
            try:
                data = response.json()
                print(f"   Response: {data}")
            except:
                print("   Could not parse JSON")
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
    
    print()
    
    # Test 3: Check email configuration
    print("Test 3: Checking email configuration...")
    try:
        from app import EMAIL_CONFIG
        print(f"   SMTP Server: {EMAIL_CONFIG['smtp_server']}")
        print(f"   SMTP Port: {EMAIL_CONFIG['smtp_port']}")
        print(f"   Sender Email: {EMAIL_CONFIG['sender_email']}")
        print(f"   Recipient Email: {EMAIL_CONFIG['recipient_email']}")
        
        if EMAIL_CONFIG['sender_email'] == 'your-email@gmail.com':
            print()
            print("⚠️  WARNING: Sender email not configured!")
            print("   Email notifications will fail until you configure it.")
            print()
            print("📋 To configure:")
            print("   1. Open app.py")
            print("   2. Find EMAIL_CONFIG (around line 735)")
            print("   3. Update sender_email and sender_password")
            print()
            print("   Reports will still be saved, but emails won't be sent.")
        else:
            print("✅ Email configuration looks good")
            
    except Exception as e:
        print(f"❌ ERROR checking email config: {str(e)}")
    
    print()
    print("=" * 70)
    print("✅ Diagnostic Complete")
    print("=" * 70)
    print()
    print("📋 Common Issues & Solutions:")
    print()
    print("Issue: 'Unexpected token <' error")
    print("Cause: Trying to parse HTML as JSON")
    print("Solution: Make sure you're logged in before submitting reports")
    print()
    print("Issue: Email not sent")
    print("Cause: Gmail credentials not configured")
    print("Solution: Update EMAIL_CONFIG in app.py with your Gmail credentials")
    print()
    print("Issue: Report not saved")
    print("Cause: Database error or user not logged in")
    print("Solution: Check console for error messages, ensure you're logged in")
    print()

if __name__ == '__main__':
    try:
        test_report_submission()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        import traceback
        traceback.print_exc()
