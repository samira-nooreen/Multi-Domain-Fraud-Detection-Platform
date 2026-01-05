"""
Brand Abuse Detection - Training Module
"""
import pandas as pd
import numpy as np
from collections import Counter
import math
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

def get_entropy(text):
    """Calculate Shannon entropy of text"""
    if not text: return 0
    counts = Counter(text)
    length = len(text)
    entropy = 0
    for count in counts.values():
        p = count / length
        entropy -= p * math.log2(p)
    return entropy

def generate_brand_abuse_data():
    """Generate synthetic brand abuse data for training based on the 7-step detection process"""
    print("Generating synthetic brand abuse dataset...")
    
    # Sample legitimate brands with more variety
    brands = ['google', 'amazon', 'facebook', 'apple', 'microsoft', 'netflix', 'paypal', 'ebay', 'tesla', 'spotify']
    
    # Generate legitimate URLs (Step 1: Legitimate digital ecosystem)
    legitimate_urls = []
    for brand in brands:
        legitimate_urls.extend([
            f"https://www.{brand}.com",
            f"https://{brand}.com",
            f"https://support.{brand}.com",
            f"https://help.{brand}.com",
            f"https://blog.{brand}.com",
            f"https://shop.{brand}.com",
            f"https://secure.{brand}.com",
            f"https://{brand}-official.com",
            f"https://community.{brand}.com",
            f"https://developer.{brand}.com",
            f"https://careers.{brand}.com",
            f"https://news.{brand}.com",
        ])
    
    # Generate abusive URLs (Step 2-3: Brand impersonation and fraud patterns)
    abusive_urls = []
    for brand in brands:
        # Typosquatting (common brand abuse pattern)
        abusive_urls.extend([
            f"https://www.{brand.replace('o', '0')}.com",  # google -> g00gle
            f"https://www.{brand.replace('a', '4')}.com",  # amazon -> 4m4z0n
            f"https://www.{brand.replace('e', '3')}.com",  # tesla -> t3sla
            f"https://{brand}support.com",
            f"https://{brand}-login.com",
            f"https://secure-{brand}.com",
            f"https://{brand}official.com",
            f"https://{brand}-account.com",
            f"https://my-{brand}.com",
            f"https://{brand}service.com",
            f"https://{brand}help.com",
            f"https://signin.{brand}.com",  # Might look legitimate but isn't
            f"https://{brand}verification.com",
            f"https://{brand}security.com",
            f"https://{brand}update.com",
            f"https://{brand}free.com",
            f"https://{brand}promo.com",
            f"https://{brand}deals.com",
            f"https://get-{brand}.com",
            f"https://free-{brand}.com",
        ])
        
        # Sophisticated abusive patterns (Step 3: Advanced fraud patterns)
        abusive_urls.extend([
            f"https://www.{brand}-free-offer.com",
            f"https://{brand}-promo-special.com",
            f"https://official-{brand}-deal.com",
            f"https://{brand}-login-secure.com",
            f"https://{brand}-support-help.com",
            f"https://{brand}-verification-account.com",
            f"https://{brand}-customer-service.com",
            f"https://{brand}-rewards-program.com",
            f"https://{brand}-discount-offer.com",
            f"https://secure.{brand}-login.com",
            f"https://{brand}-support-center.com",
            f"https://{brand}-account-verification.com",
        ])
        
        # Suspicious TLDs (Step 4: Risk scoring factors)
        suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.ru', '.cn']
        for tld in suspicious_tlds:
            abusive_urls.append(f"https://{brand}-official.{tld}")
            abusive_urls.append(f"https://secure-{brand}.{tld}")
    
    # Create DataFrame
    data = []
    
    # Add legitimate samples (Step 7: Baseline for analytics)
    for url in legitimate_urls:
        data.append({
            'url': url,
            'is_brand_abuse': 0,
            'brand': url.split('.')[1] if '.' in url else 'unknown'
        })
    
    # Add abusive samples (Step 7: Fraud patterns for detection)
    for url in abusive_urls:
        # Extract brand name from URL
        brand = 'unknown'
        for b in brands:
            if b in url:
                brand = b
                break
        data.append({
            'url': url,
            'is_brand_abuse': 1,
            'brand': brand
        })
    
    # Add some random noise (Step 1: Real-world digital ecosystem)
    for i in range(100):
        data.append({
            'url': f"https://random-site-{i}.com",
            'is_brand_abuse': 0,
            'brand': 'random'
        })
        
    for i in range(50):
        data.append({
            'url': f"https://fake-{brands[i % len(brands)]}-{i}.com",
            'is_brand_abuse': 1,
            'brand': brands[i % len(brands)]
        })
    
    df = pd.DataFrame(data)
    return df

def extract_domain_features(df):
    """Extract domain-based features aligned with the 7-step detection process"""
    print("Extracting domain features...")
    
    # Extract domain (Step 1: Digital ecosystem scanning)
    df['domain'] = df['url'].apply(lambda x: x.split('//')[-1].split('/')[0].split(':')[0])
    
    # Domain length (Step 2: Brand asset matching - domain analysis)
    df['domain_length'] = df['domain'].apply(len)
    
    # Number of dots (Step 2: Domain structure analysis)
    df['dot_count'] = df['domain'].apply(lambda x: x.count('.'))
    
    # Number of hyphens (Step 2: Brand impersonation indicators)
    df['hyphen_count'] = df['domain'].apply(lambda x: x.count('-'))
    
    # Number of digits (Step 2: Typosquatting detection)
    df['digit_count'] = df['domain'].apply(lambda x: sum(1 for c in x if c.isdigit()))
    
    # Number of special characters (Step 2: Unusual domain patterns)
    df['special_char_count'] = df['domain'].apply(lambda x: sum(1 for c in x if not c.isalnum() and c != '.' and c != '-'))
    
    # Entropy (randomness) (Step 3: Fraud pattern detection)
    df['entropy'] = df['domain'].apply(get_entropy)
    
    # Brand similarity features (Step 2: Brand asset matching)
    df['contains_brand'] = df.apply(lambda row: 1 if row['brand'] in row['domain'] else 0, axis=1)
    
    # Suspicious patterns (Step 3: Fraud pattern detection)
    suspicious_patterns = ['free', 'login', 'secure', 'account', 'support', 'help', 'promo', 'offer', 'deal', 'discount', 'win', 'prize']
    df['suspicious_patterns'] = df['domain'].apply(
        lambda x: sum(1 for pattern in suspicious_patterns if pattern in x.lower())
    )
    
    # Suspicious TLDs (Step 4: Risk scoring)
    suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.ru', '.cn']
    df['suspicious_tld'] = df['domain'].apply(lambda x: 1 if any(x.endswith(tld) for tld in suspicious_tlds) else 0)
    
    # Subdomain count (Step 3: Complex fraud patterns)
    df['subdomain_count'] = df['domain'].apply(lambda x: max(0, x.count('.') - 1))
    
    return df

def train_model():
    print("🚀 Starting Brand Abuse Detection Training...")
    
    # Get the directory of the current script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, 'brand_abuse_data.csv')
    model_path = os.path.join(base_dir, 'brand_abuse_model.pkl')
    
    # Generate or load data
    if not os.path.exists(data_path):
        print("⚠️ Dataset not found. Generating synthetic data...")
        df = generate_brand_abuse_data()
        df.to_csv(data_path, index=False)
    else:
        df = pd.read_csv(data_path)
    
    print(f"📊 Loaded {len(df)} samples")
    
    # Feature Engineering
    print("🛠️ Extracting features...")
    df = extract_domain_features(df)
    
    # Features to use (aligned with 7-step process)
    feature_cols = [
        'domain_length', 'dot_count', 'hyphen_count', 'digit_count', 
        'special_char_count', 'entropy', 'contains_brand', 'suspicious_patterns',
        'suspicious_tld', 'subdomain_count'
    ]
    
    X = df[feature_cols]
    y = df['is_brand_abuse']
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train Random Forest (good for this type of classification)
    print("⚡ Training Random Forest Classifier...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42
    )
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"✅ Accuracy: {acc:.2%}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save Model
    model_data = {
        'model': model,
        'feature_cols': feature_cols
    }
    joblib.dump(model_data, model_path)
    print(f"💾 Model saved to {model_path}")

if __name__ == "__main__":
    train_model()