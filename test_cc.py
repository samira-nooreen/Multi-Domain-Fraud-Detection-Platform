import sys
sys.path.insert(0, '.')
from ml_modules.credit_card.predict import CreditCardFraudDetector

d = CreditCardFraudDetector()

cases = [
    {'amount': 75000, 'location': 'Russia', 'transaction_type': 'Online', 'card_present': 0},
    {'amount': 75000, 'location': 'Mumbai', 'transaction_type': 'POS', 'card_present': 1},
    {'amount': 500000, 'location': 'Russia', 'transaction_type': 'Online', 'card_present': 0},
    {'amount': 200, 'location': 'Mumbai', 'transaction_type': 'POS', 'card_present': 1},
]

for c in cases:
    r = d.predict(c)
    print(f"Amount={c['amount']} loc={c['location']} type={c['transaction_type']} card={c['card_present']}")
    print(f"  -> prob={r['fraud_probability']} risk={r['risk_level']} rec={r['recommendation']}")
    print()
