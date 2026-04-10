# Email Report Configuration Guide

## ✅ Email Recipient Configured
All fraud reports will now be automatically sent to: **email-Boldx02@gmail.com**

## 🔧 Required Setup Steps

### Step 1: Configure Sender Email
You need to update the sender email credentials in `app.py`:

1. Open `app.py`
2. Find the `EMAIL_CONFIG` section (around line 735)
3. Update these values:
   ```python
   EMAIL_CONFIG = {
       'smtp_server': 'smtp.gmail.com',
       'smtp_port': 587,
       'sender_email': 'YOUR_GMAIL@gmail.com',  # Replace with your Gmail
       'sender_password': 'YOUR_APP_PASSWORD',   # Replace with App Password
       'recipient_email': 'email-Boldx02@gmail.com'
   }
   ```

### Step 2: Generate Gmail App Password
Since Gmail requires app-specific passwords:

1. Go to your Google Account: https://myaccount.google.com/
2. Select **Security** from the left menu
3. Enable **2-Step Verification** (if not already enabled)
4. Go to **App passwords** (search for it in the search bar)
5. Select **Mail** and your device
6. Click **Generate**
7. Copy the 16-character password (e.g., `abcd efgh ijkl mnop`)
8. Use this password in `sender_password` (remove spaces: `abcdefghijklmn op`)

### Step 3: Test the Configuration
Run the application and submit a test report:
```bash
python app.py
```

## 📧 How It Works

When a user clicks **"Submit Report"** on the fraud detection platform:

1. ✅ Report data is collected (title, description, category, evidence files)
2. ✅ Report is saved to the database
3. ✅ Email notification is automatically sent to **email-Boldx02@gmail.com**
4. ✅ User receives confirmation of successful submission

## 📊 Email Contents

Each report email includes:
- 🚨 Report title and category
- 📝 Full description of the suspicious activity
- 📅 Timestamp of submission
- 📎 Evidence file information (if attached)
- ⚠️ Risk assessment score
- 👤 User ID who submitted the report

## 🔒 Security Notes

- Never commit your actual Gmail password to version control
- Use app-specific passwords, not your main Gmail password
- Keep your `app.py` file secure and private
- Consider using environment variables for production deployments

## 🆘 Troubleshooting

### Common Issues:

**"Authentication failed" error:**
- Verify your app password is correct
- Ensure 2-Step Verification is enabled
- Check that less secure app access is allowed

**"Connection refused" error:**
- Verify SMTP server: `smtp.gmail.com`
- Verify SMTP port: `587`
- Check your internet connection

**Email not received:**
- Check spam/junk folder
- Verify recipient email is correct
- Check console for error messages

## 📝 Example Report Email

When a report is submitted, **email-Boldx02@gmail.com** will receive an HTML email with:
- Professional formatting
- Complete report details
- Risk assessment information
- File attachment details (if any)

---

**Status:** ✅ Recipient email configured successfully!
**Next Step:** Configure your sender Gmail credentials to enable email sending.
