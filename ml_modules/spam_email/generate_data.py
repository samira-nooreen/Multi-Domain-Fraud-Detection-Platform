"""
Spam/Phishing Email Detection - Enhanced Dataset Generator
Generates realistic spam and legitimate emails with phishing patterns
"""
import pandas as pd
import numpy as np
import random

np.random.seed(42)
random.seed(42)

def generate_spam_data(n_samples=2000):
    """Generate synthetic spam/phishing and legitimate emails"""
    
    # Spam/Phishing templates (using Rupees by default)
    spam_templates = [
        "URGENT: Your account will be suspended! Click here: {url} to verify now!",
        "Congratulations! You've won ₹{amount}! Claim your prize at {url}",
        "FINAL NOTICE: Payment required immediately. Pay now at {url}",
        "You are a WINNER! Click {url} to claim your {prize}!",
        "Limited time offer! Get {product} for FREE! Visit {url}",
        "Your {service} account has been compromised. Reset password at {url}",
        "URGENT ACTION REQUIRED: Verify your identity at {url} within 24 hours",
        "Congratulations! You've been selected for a special offer. Click {url}",
        "Your package is waiting! Track it here: {url}",
        "ALERT: Suspicious activity detected. Secure your account at {url}",
        "Get rich quick! Earn ₹{amount} from home. Start now: {url}",
        "You have {num} unread messages. View them at {url}",
        "Your {service} subscription is expiring. Renew at {url}",
        "BREAKING: You've inherited ₹{amount}! Claim at {url}",
        "Lose weight FAST with this ONE trick! Learn more: {url}",
        "Your tax refund of ₹{amount} is ready. Claim it at {url}",
        "URGENT: Your payment failed. Update billing info at {url}",
        "You've been pre-approved for a ₹{amount} loan! Apply: {url}",
        "Click here to unsubscribe: {url} (DO NOT IGNORE)",
        "Your account has been locked. Unlock it at {url} immediately!"
    ]
    
    # Legitimate email templates
    ham_templates = [
        "Hi {name}, let's schedule a meeting to discuss the {project} project.",
        "Team update: The {project} deadline has been moved to next {day}.",
        "Hi {name}, please review the attached {document} when you get a chance.",
        "Meeting reminder: {project} discussion tomorrow at {time}.",
        "Hi team, great work on the {project} presentation!",
        "Hi {name}, can you send me the {document} by end of day?",
        "Quick question about the {project} - do you have a moment to chat?",
        "Hi {name}, thanks for your help with the {project}. Much appreciated!",
        "Reminder: {project} status meeting on {day} at {time}.",
        "Hi {name}, I've shared the {document} with you. Let me know if you have questions.",
        "Team lunch on {day} at {time}. Hope you can join!",
        "Hi {name}, the {project} report looks good. Just a few minor edits needed.",
        "Can we reschedule our {project} meeting to {day}?",
        "Hi team, please complete the {project} survey by {day}.",
        "Hi {name}, I'll be out of office next {day}. {name2} will cover for me.",
        "Great job on the {project} demo today, {name}!",
        "Hi {name}, let's catch up about {project} over coffee this {day}.",
        "Reminder: Submit your {document} by {day} EOD.",
        "Hi team, {project} kickoff meeting scheduled for {day} at {time}.",
        "Hi {name}, I've updated the {document}. Please review when convenient."
    ]
    
    # Data pools
    names = ["John", "Sarah", "Mike", "Emily", "David", "Lisa", "Tom", "Anna"]
    projects = ["Q4 report", "website redesign", "marketing campaign", "budget review", "client presentation"]
    documents = ["spreadsheet", "proposal", "contract", "invoice", "report"]
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    times = ["10am", "2pm", "3pm", "11am", "4pm"]
    services = ["PayPal", "Amazon", "Netflix", "Bank", "Gmail"]
    products = ["iPhone", "laptop", "gift card", "vacation", "cash"]
    prizes = ["million dollars", "new car", "luxury vacation", "cash prize"]
    amounts = [1000, 5000, 10000, 50000, 100000]
    
    # Phishing URLs
    phishing_urls = [
        "bit.ly/xyz123", "tinyurl.com/abc456", "suspicious-link.com",
        "verify-account-now.net", "claim-prize-here.org", "urgent-action.biz"
    ]
    
    data = []
    
    for _ in range(n_samples):
        # 50% spam, 50% ham
        is_spam = random.choice([0, 1])
        
        if is_spam:
            # Generate spam/phishing email
            template = random.choice(spam_templates)
            text = template.format(
                url=random.choice(phishing_urls),
                amount=random.choice(amounts),
                prize=random.choice(prizes),
                product=random.choice(products),
                service=random.choice(services),
                num=random.randint(5, 99)
            )
            
            # Add spam indicators
            if random.random() < 0.3:
                text = text.upper()  # All caps
            if random.random() < 0.4:
                text += " ACT NOW!!!"  # Multiple exclamation marks
                
        else:
            # Generate legitimate email
            template = random.choice(ham_templates)
            text = template.format(
                name=random.choice(names),
                name2=random.choice(names),
                project=random.choice(projects),
                document=random.choice(documents),
                day=random.choice(days),
                time=random.choice(times)
            )
        
        data.append({
            'text': text,
            'label': is_spam,
            'length': len(text),
            'has_url': int('http' in text.lower() or 'www' in text.lower() or '.com' in text.lower()),
            'has_money': int('$' in text or '₹' in text or 'money' in text.lower() or 'cash' in text.lower()),
            'all_caps_ratio': sum(1 for c in text if c.isupper()) / max(len(text), 1),
            'exclamation_count': text.count('!')
        })
    
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    print("Generating spam/phishing email dataset...")
    df = generate_spam_data(2000)
    df.to_csv('spam_data.csv', index=False)
    
    print(f"✓ Generated {len(df)} email samples")
    print(f"  - Legitimate (HAM): {len(df[df['label']==0])} ({len(df[df['label']==0])/len(df)*100:.1f}%)")
    print(f"  - Spam/Phishing: {len(df[df['label']==1])} ({len(df[df['label']==1])/len(df)*100:.1f}%)")
    print("✓ Saved to spam_data.csv")
