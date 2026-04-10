import random
from datetime import datetime, timedelta

def get_latest_news(limit=10):
    """
    Simulates fetching real-time fraud news trends.
    In a production environment, this would call a real News API.
    """
    
    fraud_types = [
        "UPI Fraud", "Credit Card", "Identity Theft", "Phishing", 
        "Ransomware", "Deepfake", "SIM Swap", "Crypto Scam", 
        "Investment Fraud", "Tax Refund Scam"
    ]
    
    actions = [
        "Surge in", "New Wave of", "Warning Issued for", "Crackdown on", 
        "AI-Powered", "Massive Data Breach involving", "Police Bust", 
        "Banks Alert Customers on", "Global Syndicate Targeting"
    ]
    
    details = [
        "targeting elderly victims.", 
        "using advanced AI voice cloning.", 
        "exploiting new vulnerabilities in banking apps.", 
        "resulting in millions of dollars in losses.", 
        "spreading via WhatsApp and Telegram groups.", 
        "mimicking official government portals.", 
        "bypassing two-factor authentication.",
        "using deepfake video calls to trick executives."
    ]
    
    news_items = []
    
    # Generate some realistic-looking news items
    current_time = datetime.now()
    
    for i in range(limit):
        # Randomize time to be within last 24-48 hours
        time_offset = random.randint(30, 2880) # Minutes
        news_time = current_time - timedelta(minutes=time_offset)
        
        ftype = random.choice(fraud_types)
        action = random.choice(actions)
        detail = random.choice(details)
        
        headline = f"{action} {ftype} Attacks"
        summary = f"Security experts report a {action.lower()} {ftype.lower()} {detail} Authorities advise caution."
        
        news_items.append({
            "id": i,
            "date": news_time.strftime("%b %d, %Y"),
            "timestamp": news_time.isoformat(),
            "heading": headline,
            "summary": summary,
            "tags": [ftype, "Security Alert"]
        })
        
    # Sort by timestamp (newest first)
    news_items.sort(key=lambda x: x['timestamp'], reverse=True)
    
    return news_items
