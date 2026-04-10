"""
Secure Email Configuration Setup
This script helps you configure email without saving password in code
"""
import os

print("=" * 70)
print("🔐 Secure Email Configuration Setup")
print("=" * 70)
print()
print("Your password will be saved in .env file (NOT in the code)")
print("The .env file is protected and won't be saved to Git")
print()

# Get email details
print("📧 Enter your email details:")
print()

sender_email = input("Your Gmail address (e.g., john@gmail.com): ").strip()

if not sender_email or '@' not in sender_email:
    print("❌ Invalid email address!")
    exit(1)

print()
print("🔑 Enter your Gmail App Password:")
print("   (16 characters, no spaces)")
print("   If you don't have one, visit: https://myaccount.google.com/apppasswords")
print()

sender_password = input("App Password: ").strip()

if not sender_password or len(sender_password) < 10:
    print("❌ Invalid password!")
    print("   Must be a 16-character Gmail App Password")
    exit(1)

print()
recipient_email = input("Recipient email (press Enter for email-Boldx02@gmail.com): ").strip()
if not recipient_email:
    recipient_email = 'email-Boldx02@gmail.com'

# Create .env file content
env_content = f"""# Email Configuration
# This file is private and should NOT be committed to version control
EMAIL_SENDER={sender_email}
EMAIL_PASSWORD={sender_password}
EMAIL_RECIPIENT={recipient_email}
"""

# Write to .env file
env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')

try:
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    print()
    print("=" * 70)
    print("✅ Configuration Saved Successfully!")
    print("=" * 70)
    print()
    print(f"📧 Sender Email: {sender_email}")
    print(f"📧 Recipient: {recipient_email}")
    print(f"🔒 Password saved securely in: .env")
    print()
    print("📋 Next Steps:")
    print("  1. Restart your Flask server (Ctrl+C, then python app.py)")
    print("  2. Test email: python test_email_report.py")
    print("  3. Submit a report on the website")
    print()
    print("⚠️  Important:")
    print("  - Never share your .env file")
    print("  - Never commit .env to Git (it's already in .gitignore)")
    print("  - Your password is NOT in the code files")
    print()
    
except Exception as e:
    print()
    print(f"❌ Error saving configuration: {e}")
    print("   Please try again or manually edit the .env file")
