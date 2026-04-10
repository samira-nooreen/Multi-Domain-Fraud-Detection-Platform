from ml_modules.phishing_url.predict import PhishingDetector

d = PhishingDetector()

test_urls = [
    ('http://win-1crore-now.click', 'EXTREME PHISHING'),
    ('https://www.bbc.com/news', 'SAFE'),
    ('http://paytm-secure-login.xyz', 'PHISHING'),
    ('http://amaz0n-offers.com', 'PHISHING (brand spoof)'),
]

print("="*80)
for url, expected in test_urls:
    r = d.predict(url)
    print(f"\nURL: {url}")
    print(f"Expected: {expected}")
    print(f"Phishing: {r['is_phishing']}")
    print(f"Probability: {r['phishing_probability']*100:.1f}%")
    print(f"Risk: {r['risk_level']}")
    print(f"Confidence: {r['confidence_percent']}%")
    print(f"Features: {r['url_features'][:80]}...")
    print("="*80)
