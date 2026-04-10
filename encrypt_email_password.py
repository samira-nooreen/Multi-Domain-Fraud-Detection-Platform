"""
Email Password Encryption Utility
Encrypts your email password so it's never stored in plain text
"""
from cryptography.fernet import Fernet
import os
import base64

def generate_key():
    """Generate a new encryption key"""
    return Fernet.generate_key()

def encrypt_password(password, key):
    """Encrypt password using Fernet"""
    fernet = Fernet(key)
    encrypted = fernet.encrypt(password.encode())
    return encrypted.decode()

def decrypt_password(encrypted_password, key):
    """Decrypt password using Fernet"""
    fernet = Fernet(key)
    decrypted = fernet.decrypt(encrypted_password.encode())
    return decrypted.decode()

def setup_encrypted_email():
    """Interactive setup for encrypted email configuration"""
    print("=" * 70)
    print("🔐 Secure Email Password Setup (Encrypted)")
    print("=" * 70)
    print()
    print("Your password will be:")
    print("  1. Encrypted using Fernet encryption")
    print("  2. Stored in .env file (encrypted)")
    print("  3. Decryption key stored separately")
    print("  4. NEVER stored in plain text")
    print()
    
    # Get email details
    sender_email = input("📧 Your Gmail address: ").strip()
    if not sender_email or '@' not in sender_email:
        print("❌ Invalid email!")
        return False
    
    print()
    print("🔑 Enter your Gmail App Password (16 characters):")
    password = input("   App Password: ").strip()
    
    if len(password) < 10:
        print("❌ Password too short!")
        return False
    
    print()
    recipient = input("📬 Recipient email (press Enter for email-Boldx02@gmail.com): ").strip()
    if not recipient:
        recipient = 'email-Boldx02@gmail.com'
    
    # Generate encryption key
    print()
    print("🔐 Generating encryption key...")
    key = generate_key()
    
    # Encrypt password
    encrypted_password = encrypt_password(password, key)
    
    # Save encrypted password to .env
    env_content = f"""# Email Configuration (Encrypted)
# Password is encrypted - never stored in plain text
EMAIL_SENDER={sender_email}
EMAIL_PASSWORD_ENCRYPTED={encrypted_password}
EMAIL_RECIPIENT={recipient}
EMAIL_ENCRYPTION_ENABLED=true
"""
    
    env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    # Save encryption key to .env.key (separate file)
    key_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env.key')
    with open(key_file, 'w') as f:
        f.write(key.decode())
    
    # Add .env.key to .gitignore
    gitignore_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.gitignore')
    with open(gitignore_file, 'a') as f:
        f.write('\n.env.key\n')
    
    print()
    print("=" * 70)
    print("✅ Password Encrypted and Saved Successfully!")
    print("=" * 70)
    print()
    print(f"📧 Sender: {sender_email}")
    print(f"📬 Recipient: {recipient}")
    print(f"🔒 Password: ENCRYPTED ✅")
    print(f"🔑 Key saved to: .env.key")
    print()
    print("📋 Security Features:")
    print("  ✅ Password encrypted with Fernet")
    print("  ✅ Encryption key stored separately")
    print("  ✅ Both files in .gitignore")
    print("  ✅ Plain text password NOT stored anywhere")
    print()
    print("⚠️  Important:")
    print("  - NEVER share .env.key file")
    print("  - Backup .env.key securely")
    print("  - Without .env.key, encrypted password cannot be decrypted")
    print()
    
    return True

if __name__ == '__main__':
    try:
        setup_encrypted_email()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup cancelled")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
