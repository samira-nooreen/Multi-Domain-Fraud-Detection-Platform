from ml_modules.phishing_url.predict import PhishingDetector
import os

# Ensure we are in the right directory or handle paths
# The predict.py expects phishing_model.pkl in the same dir or specified path
# In app.py, it is passed as 'ml_modules/phishing_url/phishing_model.pkl'

base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, 'ml_modules', 'phishing_url', 'phishing_model.pkl')

print(f"Testing model at: {model_path}")

detector = PhishingDetector(model_path=model_path)

test_urls = [
    "https://www.google.com",
    "http://secure-login-update.xyz/account/verify",
    "https://www.amazon.com/product/123",
    "http://paypal-secure-check.info"
]

for url in test_urls:
    result = detector.predict(url)
    print(f"\nURL: {url}")
    print(f"Prediction: {result}")
