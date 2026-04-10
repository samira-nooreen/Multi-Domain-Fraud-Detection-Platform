
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
import joblib, pandas as pd, numpy as np
from collections import Counter
import math

data = joblib.load('ml_modules/phishing_url/phishing_model.pkl')
print('model type:', type(data))
if isinstance(data, dict):
    print('keys:', list(data.keys()))
    model = data.get('model')
    scaler = data.get('scaler')
    fcols = data.get('feature_cols', [])
    print('model:', type(model))
    print('feature_cols:', fcols)
    if hasattr(model, 'classes_'):
        print('classes:', model.classes_)
    # Try predict on google
    def get_entropy(text):
        if not text: return 0
        counts = Counter(text)
        length = len(text)
        entropy = 0
        for count in counts.values():
            p = count / length
            entropy -= p * math.log2(p)
        return entropy
    def get_special(text):
        return sum(1 for c in text if not c.isalnum())
    def whois_age(url):
        domain = url.split('//')[-1].split('/')[0]
        if len(domain) < 10: return 2000
        elif len(domain) < 20: return 500
        else: return 10
    
    for url in ['https://google.com', 'http://paypal.tk/verify', 'http://x.yz/abc?q=1&p=2']:
        features = {'length': len(url), 'special_chars': get_special(url), 'whois_age': whois_age(url), 'token_entropy': get_entropy(url)}
        print(f'URL: {url}')
        print(f'  features: {features}')
        if fcols:
            df = pd.DataFrame([{col: features.get(col, 0) for col in fcols}])
        else:
            df = pd.DataFrame([features])
        if scaler:
            X = scaler.transform(df)
        else:
            X = df.values
        print(f'  X_scaled: {X}')
        if hasattr(model, 'predict_proba'):
            print(f'  proba: {model.predict_proba(X)[0]}')
        print(f'  predict: {model.predict(X)[0]}')
else:
    print('direct model:', type(data))
    if hasattr(data, 'classes_'):
        print('classes:', data.classes_)
