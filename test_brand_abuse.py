"""
Test script for brand abuse detection feature
"""
import sys
import os

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ml_modules.brand_abuse.predict import BrandAbuseDetector

def test_brand_abuse_detection():
    """Test the brand abuse detection functionality"""
    print("Testing Brand Abuse Detection...")
    
    # Initialize the detector
    detector = BrandAbuseDetector(model_path='ml_modules/brand_abuse/brand_abuse_model.pkl')
    
    # Test cases
    test_cases = [
        {
            'url': 'https://www.google.com',
            'brand_keywords': ['google'],
            'content_text': 'Official Google website',
            'expected': 'legitimate'
        },
        {
            'url': 'https://www.g00gle.com',
            'brand_keywords': ['google'],
            'content_text': 'Google services',
            'expected': 'abuse'
        },
        {
            'url': 'https://secure-amazon.com',
            'brand_keywords': ['amazon'],
            'content_text': 'Amazon account login',
            'expected': 'abuse'
        },
        {
            'url': 'https://www.microsoft.com',
            'brand_keywords': ['microsoft'],
            'content_text': 'Microsoft official site',
            'expected': 'legitimate'
        }
    ]
    
    for i, test_case in enumerate(test_cases):
        print(f"\nTest Case {i+1}: {test_case['url']}")
        result = detector.predict(test_case)
        
        print(f"  Expected: {test_case['expected']}")
        print(f"  Detected as brand abuse: {result['is_brand_abuse']}")
        print(f"  Abuse probability: {result['abuse_probability']:.2f}")
        print(f"  Risk level: {result['risk_level']}")
        print(f"  Confidence: {result['confidence']:.2f}")
        if 'process_steps' in result:
            print(f"  Process steps: {len(result['process_steps'])} steps")
        
        # Check if the result matches expectation
        if test_case['expected'] == 'abuse' and result['is_brand_abuse']:
            print("  ✓ Test PASSED")
        elif test_case['expected'] == 'legitimate' and not result['is_brand_abuse']:
            print("  ✓ Test PASSED")
        else:
            print("  ✗ Test FAILED")

if __name__ == "__main__":
    test_brand_abuse_detection()