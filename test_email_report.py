"""
Test Email Report Functionality
This script tests the email report system without running the full app.
"""
import sys
import os

# Add the app directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import email configuration and function from app
from app import EMAIL_CONFIG, send_report_email

def test_email_configuration():
    """Test if email is configured correctly"""
    print("=" * 60)
    print("📧 Email Report Configuration Test")
    print("=" * 60)
    print()
    
    # Display current configuration
    print("📋 Current Email Configuration:")
    print(f"   SMTP Server: {EMAIL_CONFIG['smtp_server']}")
    print(f"   SMTP Port: {EMAIL_CONFIG['smtp_port']}")
    print(f"   Sender Email: {EMAIL_CONFIG['sender_email']}")
    print(f"   Recipient Email: {EMAIL_CONFIG['recipient_email']}")
    print()
    
    # Check if configuration needs updating
    if EMAIL_CONFIG['sender_email'] == 'your-email@gmail.com':
        print("⚠️  WARNING: Sender email is not configured!")
        print("   Please update EMAIL_CONFIG in app.py with your Gmail credentials.")
        print()
        print("📖 Steps to configure:")
        print("   1. Open app.py")
        print("   2. Find EMAIL_CONFIG (around line 735)")
        print("   3. Replace 'your-email@gmail.com' with your Gmail")
        print("   4. Replace 'your-app-password' with your Gmail App Password")
        print()
        print("🔑 To generate Gmail App Password:")
        print("   1. Go to: https://myaccount.google.com/apppasswords")
        print("   2. Enable 2-Step Verification if not enabled")
        print("   3. Generate a new app password for Mail")
        print("   4. Copy the 16-character password (remove spaces)")
        print()
        return False
    
    if EMAIL_CONFIG['sender_password'] == 'your-app-password':
        print("⚠️  WARNING: App password is not configured!")
        print("   Please update EMAIL_CONFIG['sender_password'] in app.py")
        print()
        return False
    
    print("✅ Email configuration looks good!")
    print()
    return True


def test_send_report():
    """Test sending a sample report"""
    print("=" * 60)
    print("📤 Testing Report Email Send")
    print("=" * 60)
    print()
    
    # Sample report data
    sample_report = {
        'title': 'Test Fraud Report',
        'category': 'UPI Fraud',
        'source': 'Test System',
        'description': 'This is a test report to verify email functionality. If you receive this, the email system is working correctly!',
        'risk_score': 'High (87/100)',
        'action': 'Flagged for manual review',
        'submitted_by': 'Test User',
        'timestamp': '2026-04-10T12:00:00'
    }
    
    print("📝 Sample Report Data:")
    for key, value in sample_report.items():
        print(f"   {key}: {value}")
    print()
    
    print("📤 Attempting to send email...")
    print()
    
    try:
        success = send_report_email(sample_report)
        
        if success:
            print("✅ SUCCESS! Email sent successfully!")
            print(f"   Check inbox of: {EMAIL_CONFIG['recipient_email']}")
            print()
            print("📬 The email should contain:")
            print("   - Report title and category")
            print("   - Full description")
            print("   - Risk assessment")
            print("   - Timestamp")
        else:
            print("❌ FAILED! Email was not sent.")
            print("   Check the error messages above for details.")
            print()
            print("🔍 Common issues:")
            print("   - Incorrect Gmail credentials")
            print("   - App password not generated")
            print("   - 2-Step Verification not enabled")
            print("   - Internet connection issue")
        
        return success
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        print()
        print("🔍 Troubleshooting:")
        print("   - Verify your Gmail credentials are correct")
        print("   - Ensure 2-Step Verification is enabled")
        print("   - Generate a new App Password if needed")
        return False


if __name__ == '__main__':
    print()
    
    # Test configuration
    config_ok = test_email_configuration()
    
    if config_ok:
        # Test sending email
        test_send_report()
    else:
        print("⏭️  Skipping email send test - configuration needed first.")
        print()
        print("📖 See EMAIL_REPORT_SETUP.md for detailed setup instructions.")
    
    print()
    print("=" * 60)
    print("✅ Test Complete")
    print("=" * 60)
    print()
