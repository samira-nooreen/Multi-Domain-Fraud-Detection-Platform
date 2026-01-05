"""
Phishing URL Detection - Dataset Generator
Generates synthetic URLs for Random Forest training
"""
import pandas as pd
import numpy as np
import random
import string

def generate_url_data(n_samples=5000):
    """Generate synthetic phishing/legitimate URLs"""
    
    legit_domains = ['google.com', 'facebook.com', 'amazon.com', 'wikipedia.org', 'twitter.com', 'linkedin.com']
    phishing_keywords = ['login', 'secure', 'account', 'update', 'verify', 'banking', 'free-gift']
    tlds = ['.com', '.net', '.org', '.xyz', '.tk', '.info']
    
    data = []
    
    for _ in range(n_samples):
        is_phishing = random.choice([0, 1])
        
        if is_phishing:
            # Generate phishing URL
            subdomain = random.choice(phishing_keywords)
            domain = ''.join(random.choices(string.ascii_lowercase, k=random.randint(5, 15)))
            tld = random.choice(tlds)
            path = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(10, 30)))
            
            # Features of phishing
            if random.random() > 0.5:
                url = f"http://{subdomain}-{domain}{tld}/{path}"
            else:
                url = f"http://{domain}{tld}/{subdomain}/{path}"
                
            # Add suspicious chars
            if random.random() > 0.7:
                url = url.replace('.', '-')
                
        else:
            # Generate legitimate URL
            domain = random.choice(legit_domains)
            path = ''.join(random.choices(string.ascii_lowercase, k=random.randint(5, 10)))
            url = f"https://www.{domain}/{path}"
            
        # Feature extraction (simplified for generation)
        length = len(url)
        has_ip = 1 if any(c.isdigit() for c in url.split('/')[2]) else 0
        num_dots = url.count('.')
        has_at = 1 if '@' in url else 0
        
        data.append({
            'url': url,
            'length': length,
            'num_dots': num_dots,
            'has_ip': has_ip,
            'has_at': has_at,
            'is_phishing': is_phishing
        })
        
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    df = generate_url_data()
    df.to_csv('phishing_data.csv', index=False)
    print("Saved phishing_data.csv")
