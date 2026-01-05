"""
Test script to verify all ML modules are working properly
"""
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_upi_fraud():
    """Test UPI Fraud Detection Module"""
    print("Testing UPI Fraud Detection Module...")
    try:
        from ml_modules.upi_fraud.predict import UPIFraudDetector
        detector = UPIFraudDetector()
        test_data = {
            'amount': 5000,
            'hour': 2,
            'day_of_week': 1,
            'transaction_frequency': 5,
            'avg_transaction_amount': 2000,
            'account_age_days': 30,
            'device_change': 1,
            'location_change': 1,
            'transactions_last_hour': 10,
            'transactions_last_day': 20,
            'merchant_risk_score': 0.8,
            'new_merchant': 1,
            'failed_attempts': 2
        }
        result = detector.predict(test_data)
        print(f"  Result: {result['risk_level']} - {result['recommendation']}")
        return True
    except Exception as e:
        print(f"  Error: {str(e)}")
        return False

def test_credit_card():
    """Test Credit Card Fraud Detection Module"""
    print("Testing Credit Card Fraud Detection Module...")
    try:
        from ml_modules.credit_card.predict import CreditCardFraudDetector
        detector = CreditCardFraudDetector()
        # Test data for credit card fraud detection
        test_data = {
            'distance_from_home': 100,
            'ratio_to_median_purchase_price': 2.5,
            'repeat_retailer': 0,
            'used_chip': 1,
            'used_pin_number': 0,
            'online_order': 1,
            'amount': 150.50,
            'hour': 3,
            'day_of_week': 2
        }
        result = detector.predict(test_data)
        print(f"  Result: {result['risk_level']} - {result['recommendation']}")
        return True
    except Exception as e:
        print(f"  Error: {str(e)}")
        return False

def test_loan_default():
    """Test Loan Default Detection Module"""
    print("Testing Loan Default Detection Module...")
    try:
        from ml_modules.loan_default.predict import LoanDefaultPredictor
        predictor = LoanDefaultPredictor()
        # Test data for loan default prediction
        test_data = {
            'loan_amnt': 15000,
            'term': 36,
            'int_rate': 12.5,
            'installment': 450.0,
            'grade': 'B',
            'emp_length': 5,
            'annual_inc': 60000,
            'home_ownership': 'RENT',
            'purpose': 'debt_consolidation',
            'addr_state': 'CA',
            'dti': 15.2,
            'delinq_2yrs': 0,
            'inq_last_6mths': 1,
            'open_acc': 8,
            'pub_rec': 0,
            'revol_bal': 12000,
            'revol_util': 65.5,
            'total_acc': 15,
            'mort_acc': 1,
            'pub_rec_bankruptcies': 0
        }
        result = predictor.predict(test_data)
        print(f"  Result: {result['risk_level']} - Probability: {result['default_probability']:.2%}")
        return True
    except Exception as e:
        print(f"  Error: {str(e)}")
        return False

def test_insurance_fraud():
    """Test Insurance Fraud Detection Module"""
    print("Testing Insurance Fraud Detection Module...")
    try:
        from ml_modules.insurance_fraud.predict import InsuranceFraudDetector
        detector = InsuranceFraudDetector()
        # Test data for insurance fraud detection
        test_data = {
            'months_as_customer': 24,
            'age': 45,
            'policy_csl': '250/500',
            'policy_deductable': 1000,
            'policy_state': 'OH',
            'insured_sex': 'MALE',
            'insured_education_level': 'MD',
            'insured_occupation': 'exec-managerial',
            'insured_hobbies': 'chess',
            'insured_relationship': 'husband',
            'capital_gains': 0,
            'capital_loss': 0,
            'incident_type': 'Single Vehicle Collision',
            'collision_type': 'Front Collision',
            'incident_severity': 'Major Damage',
            'authorities_contacted': 'Police',
            'incident_state': 'NY',
            'incident_city': 'New York',
            'incident_hour_of_the_day': 14,
            'number_of_vehicles_involved': 1,
            'property_damage': 'NO',
            'bodily_injuries': 1,
            'witnesses': 2,
            'police_report_available': 'YES',
            'total_claim_amount': 50000,
            'injury_claim': 25000,
            'property_claim': 15000,
            'vehicle_claim': 10000,
            'auto_make': 'Honda',
            'auto_model': 'Accord',
            'auto_year': 2015
        }
        result = detector.predict(test_data)
        print(f"  Result: {result['risk_level']} - Anomaly Score: {result['anomaly_score']:.4f}")
        return True
    except Exception as e:
        print(f"  Error: {str(e)}")
        return False

def test_click_fraud():
    """Test Click Fraud Detection Module"""
    print("Testing Click Fraud Detection Module...")
    try:
        from ml_modules.click_fraud.predict import ClickFraudDetector
        detector = ClickFraudDetector()
        # Test data for click fraud detection
        test_data = {
            'ip_address': '192.168.1.100',
            'user_agent': 'Mozilla/5.0',
            'timestamp': '2023-01-01 12:00:00',
            'referrer': 'https://google.com',
            'landing_page': '/product',
            'session_duration': 120,
            'pages_visited': 3,
            'clicks_per_minute': 5.5,
            'mouse_movement': 1200,
            'click_patterns': 'normal'
        }
        result = detector.predict(test_data)
        print(f"  Result: {result['risk_level']} - Fraud Probability: {result['fraud_probability']:.2%}")
        return True
    except Exception as e:
        print(f"  Error: {str(e)}")
        return False

def test_fake_news():
    """Test Fake News Detection Module"""
    print("Testing Fake News Detection Module...")
    try:
        from ml_modules.fake_news.predict import DJDarkCyberFakeNewsDetector as FakeNewsDetector
        detector = FakeNewsDetector()
        # Test data for fake news detection
        test_data = {
            'text': "Scientists discover breakthrough treatment for Alzheimer's disease. New study shows promising results in early trials."
        }
        result = detector.predict(test_data['text'])
        print(f"  Result: {result['prediction']} - Confidence: {result['confidence']:.2%}")
        return True
    except Exception as e:
        print(f"  Error: {str(e)}")
        return False

def test_spam_email():
    """Test Spam Email Detection Module"""
    print("Testing Spam Email Detection Module...")
    try:
        from ml_modules.spam_email.predict import SpamDetector as SpamEmailDetector
        detector = SpamEmailDetector()
        # Test data for spam email detection
        test_data = {
            'subject': "Congratulations! You've won $1000000",
            'body': "Click here now to claim your prize! Limited time offer! Act now!"
        }
        result = detector.predict(test_data)
        print(f"  Result: {result['prediction']} - Spam Probability: {result['spam_probability']:.2%}")
        return True
    except Exception as e:
        print(f"  Error: {str(e)}")
        return False

def test_phishing_url():
    """Test Phishing URL Detection Module"""
    print("Testing Phishing URL Detection Module...")
    try:
        from ml_modules.phishing_url.predict import PhishingDetector as PhishingURLDetector
        detector = PhishingURLDetector()
        # Test data for phishing URL detection
        test_data = {
            'url': "https://secure-login.bankofamerica.com.verify-account-information.login-page.suspicious-domain.com"
        }
        result = detector.predict(test_data['url'])
        print(f"  Result: {result['prediction']} - Phishing Probability: {result['phishing_probability']:.2%}")
        return True
    except Exception as e:
        print(f"  Error: {str(e)}")
        return False

def main():
    """Main function to test all modules"""
    print("=" * 60)
    print("Testing All ML Fraud Detection Modules")
    print("=" * 60)
    
    modules = [
        ("UPI Fraud", test_upi_fraud),
        ("Credit Card Fraud", test_credit_card),
        ("Loan Default", test_loan_default),
        ("Insurance Fraud", test_insurance_fraud),
        ("Click Fraud", test_click_fraud),
        ("Fake News", test_fake_news),
        ("Spam Email", test_spam_email),
        ("Phishing URL", test_phishing_url)
    ]
    
    successful_modules = []
    failed_modules = []
    
    for module_name, test_function in modules:
        try:
            if test_function():
                successful_modules.append(module_name)
            else:
                failed_modules.append(module_name)
        except Exception as e:
            print(f"Module {module_name} failed with exception: {str(e)}")
            failed_modules.append(module_name)
        print()
    
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Successful Modules ({len(successful_modules)}): {', '.join(successful_modules)}")
    if failed_modules:
        print(f"Failed Modules ({len(failed_modules)}): {', '.join(failed_modules)}")
    else:
        print("All modules are working properly!")
    
    return len(failed_modules) == 0

if __name__ == "__main__":
    main()