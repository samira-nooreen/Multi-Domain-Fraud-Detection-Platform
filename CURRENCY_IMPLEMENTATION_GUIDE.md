# Multi-Currency Support Implementation Guide

## Overview
This document outlines the implementation of multi-currency support across the entire fraud detection platform, with **Indian Rupees (INR)** as the default currency.

---

## 1. Currency Configuration Module

**File:** `currency_config.py` ✅ Created

This module provides centralized currency management:

```python
CURRENCIES = {
    'INR': {'symbol': '₹', 'name': 'Indian Rupee'},
    'USD': {'symbol': '$', 'name': 'US Dollar'},
    'EUR': {'symbol': '€', 'name': 'Euro'},
    'GBP': {'symbol': '£', 'name': 'British Pound'}
}

DEFAULT_CURRENCY = 'INR'  # Default is Indian Rupees
```

---

## 2. HTML Templates to Update

### A. Credit Card Fraud Detection (`credit_card.html`)

**Changes Required:**

1. **Add Currency Selector** (before amount field):
```html
<div class="form-group">
    <label for="currency">Currency</label>
    <select id="currency" name="currency">
        <option value="INR" selected>₹ Indian Rupee (INR)</option>
        <option value="USD">$ US Dollar (USD)</option>
        <option value="EUR">€ Euro (EUR)</option>
        <option value="GBP">£ British Pound (GBP)</option>
    </select>
</div>
```

2. **Update Amount Label**:
```html
<label for="amount">Transaction Amount</label>
<!-- Remove the ($) from label -->
```

3. **Update JavaScript Display**:
```javascript
// Replace line 244
const currency = document.getElementById('currency').value || 'INR';
const currencySymbols = {
    'INR': '₹',
    'USD': '$',
    'EUR': '€',
    'GBP': '£'
};
const symbol = currencySymbols[currency] || '₹';
document.getElementById('transAmount').textContent = symbol + parseFloat(amount).toLocaleString('en-IN');
```

---

### B. Insurance Fraud Detection (`insurance_fraud.html`)

**Changes Required:**

1. **Add Currency Selector** (Line 48):
```html
<div class="form-group">
    <label for="currency">Currency</label>
    <select id="currency" name="currency">
        <option value="INR" selected>₹ Indian Rupee (INR)</option>
        <option value="USD">$ US Dollar (USD)</option>
        <option value="EUR">€ Euro (EUR)</option>
        <option value="GBP">£ British Pound (GBP)</option>
    </select>
</div>

<div class="form-group">
    <label for="claim_amount">Claim Amount</label>
    <input type="number" id="claim_amount" name="claim_amount" required min="0" step="0.01">
</div>
```

2. **Update JavaScript** (Line 247):
```javascript
const currency = document.getElementById('currency').value || 'INR';
const currencySymbols = {'INR': '₹', 'USD': '$', 'EUR': '€', 'GBP': '£'};
const symbol = currencySymbols[currency] || '₹';
document.getElementById('claimAmount').textContent = symbol + parseFloat(amount).toLocaleString('en-IN');
```

---

### C. Loan Default Prediction (`loan_default.html`)

**Changes Required:**

1. **Add Currency Selector** (before Line 52):
```html
<div class="form-group">
    <label for="currency">Currency</label>
    <select id="currency" name="currency">
        <option value="INR" selected>₹ Indian Rupee (INR)</option>
        <option value="USD">$ US Dollar (USD)</option>
        <option value="EUR">€ Euro (EUR)</option>
        <option value="GBP">£ British Pound (GBP)</option>
    </select>
</div>
```

2. **Update Labels**:
```html
<label for="loan_amount">Loan Amount</label>
<label for="annual_income">Annual Income</label>
```

3. **Update JavaScript** (Line 264):
```javascript
const currency = document.getElementById('currency').value || 'INR';
const currencySymbols = {'INR': '₹', 'USD': '$', 'EUR': '€', 'GBP': '£'};
const symbol = currencySymbols[currency] || '₹';
document.getElementById('loanAmount').textContent = symbol + parseFloat(amount).toLocaleString('en-IN');
```

---

## 3. Backend Integration (`app.py`)

**Add Currency Handling:**

```python
from currency_config import get_currency_symbol, format_amount

@app.route('/detect_credit', methods=['POST'])
def detect_credit():
    data = request.json
    currency = data.get('currency', 'INR')  # Default to INR
    amount = float(data.get('amount', 0))
    
    # ... existing fraud detection logic ...
    
    result['currency'] = currency
    result['formatted_amount'] = format_amount(amount, currency)
    
    return jsonify(result)
```

---

## 4. ML Module Data Generation Updates

### Spam Email (`ml_modules/spam_email/generate_data.py`)

**Update Templates** (Lines 18, 27, 30, 32, 34):

```python
spam_templates = [
    "Congratulations! You've won ₹{amount}! Claim your prize at {url}",
    "Get rich quick! Earn ₹{amount} from home. Start now: {url}",
    "BREAKING: You've inherited ₹{amount}! Claim at {url}",
    "Your tax refund of ₹{amount} is ready. Claim it at {url}",
    "You've been pre-approved for a ₹{amount} loan! Apply: {url}",
]

# Update amounts to Indian Rupees
amounts = [10000, 50000, 100000, 500000, 1000000]  # In Rupees
```

**Update Detection** (Line 121):
```python
'has_money': int('₹' in text or 'rupees' in text.lower() or 'rs' in text.lower() or 'inr' in text.lower()),
```

---

### Fake News (`ml_modules/fake_news/generate_data.py`)

**Update Template** (Line 36):
```python
"Earn ₹{number}0000 from home in ONE DAY with this simple trick!",
```

---

## 5. Icon Updates

### Dashboard (`templates/index.html`)

**Update Icon** (Line 100):
```html
<div class="card-icon"><i class="fa-solid fa-indian-rupee-sign"></i></div>
<!-- Or use: fa-money-bill-wave for generic money icon -->
```

### Loan Default (`templates/loan_default.html`)

**Update Icon** (Line 43):
```html
<h1><i class="fas fa-hand-holding-rupee"></i> Loan Default Risk Prediction</h1>
<!-- Or use: fa-hand-holding-usd for generic -->
```

---

## 6. Summary of Changes

### Files to Update:

1. ✅ **`currency_config.py`** - Created (centralized currency management)

2. **HTML Templates:**
   - `templates/credit_card.html` - Add currency selector + update JS
   - `templates/insurance_fraud.html` - Add currency selector + update JS
   - `templates/loan_default.html` - Add currency selector + update JS
   - `templates/index.html` - Update money icon

3. **ML Module Data Generators:**
   - `ml_modules/spam_email/generate_data.py` - Change $ to ₹
   - `ml_modules/spam_email/predict.py` - Update test cases
   - `ml_modules/spam_email/quick_demo.py` - Update test cases
   - `ml_modules/fake_news/generate_data.py` - Change $ to ₹
   - `ml_modules/fake_news/demo.py` - Update test cases

4. **Backend:**
   - `app.py` - Import currency_config and handle currency parameter

---

## 7. Quick Implementation Steps

### Step 1: Update All HTML Templates
Add currency selector dropdown to all financial forms (credit card, insurance, loan).

### Step 2: Update JavaScript
Modify display functions to use selected currency symbol instead of hardcoded $.

### Step 3: Update ML Data Generators
Replace all $ symbols with ₹ and adjust amounts to Indian Rupee values.

### Step 4: Update Backend
Import currency_config and handle currency parameter in API endpoints.

### Step 5: Test
- Test each module with different currencies
- Verify default is INR (₹)
- Check amount formatting

---

## 8. Currency Symbol Reference

| Currency | Symbol | HTML Entity | Unicode |
|----------|--------|-------------|---------|
| INR | ₹ | `&#8377;` | `\u20b9` |
| USD | $ | `&#36;` | `\u0024` |
| EUR | € | `&#8364;` | `\u20ac` |
| GBP | £ | `&#163;` | `\u00a3` |

---

## 9. Example Usage

### Frontend (HTML):
```html
<select id="currency">
    <option value="INR" selected>₹ Indian Rupee</option>
    <option value="USD">$ US Dollar</option>
</select>
```

### JavaScript:
```javascript
const currency = document.getElementById('currency').value || 'INR';
const symbols = {'INR': '₹', 'USD': '$', 'EUR': '€', 'GBP': '£'};
const symbol = symbols[currency] || '₹';
const formatted = symbol + amount.toLocaleString('en-IN');
```

### Python:
```python
from currency_config import format_amount
formatted = format_amount(5000, 'INR')  # Returns: ₹5,000.00
```

---

## 10. Benefits

✅ **Default INR:** Indian Rupees as default currency
✅ **Multi-Currency:** Support for USD, EUR, GBP
✅ **Centralized:** Single configuration file
✅ **Flexible:** Easy to add more currencies
✅ **Consistent:** Same currency handling across all modules
✅ **User-Friendly:** Currency selector in UI

---

**Status:** Configuration module created. HTML templates and ML modules need manual updates as outlined above.

