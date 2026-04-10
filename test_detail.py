
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
from ml_modules.phishing_url.predict import PhishingDetector
d = PhishingDetector(model_path='ml_modules/phishing_url/phishing_model.pkl')
print('google:', d.predict('https://google.com'))
print('short:', d.predict('http://paypal.tk/verify'))
print('legit bank:', d.predict('https://www.sbi.co.in/login'))
print('phishing long:', d.predict('http://paypal-secure-login.verify-account-update.tk/confirm'))
print('click:', d.predict('https://click.fraud.xyz/tracker'))

from ml_modules.click_fraud.predict import ClickFraudDetector
cf = ClickFraudDetector(model_dir='ml_modules/click_fraud')
normal = [[2.5, 100, 200, 0, 0, 10, 0, 5] for _ in range(10)]
bot = [[0.05, 100, 200, 0, 0, 10, 0, 5] for _ in range(50)]
print('click normal:', cf.predict(normal))
print('click bot:', cf.predict(bot))
