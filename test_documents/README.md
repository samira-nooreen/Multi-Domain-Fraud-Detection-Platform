# 📄 Test Documents for Document Forgery Detection

## Created Test Documents

I've generated **2 test documents** for you:

### 1. **sample_certificate.png** (Genuine)
- ✅ Official certificate
- ✅ Clean formatting
- ✅ Consistent fonts
- ✅ Proper alignment
- ✅ Official stamp and signature

**Location**: `test_documents/sample_certificate.png`

### 2. **forged_certificate.png** (Forged)
- ⚠️ Altered issue date
- ⚠️ Different font size
- ⚠️ Slight color mismatch
- ⚠️ Forgery indicators present

**Location**: `test_documents/forged_certificate.png`

## How to Test

### Option 1: Using Flask Web Interface

1. **Navigate to Document Forgery Detection**:
   - Open browser: `http://127.0.0.1:5000/detect_forgery`
   - Log in if required

2. **Upload Test Document**:
   - Click "Choose File"
   - Select `test_documents/sample_certificate.png` or `forged_certificate.png`
   - Click "Analyze Document"

3. **View Results**:
   - Genuine document: Should show "GENUINE" with low forgery probability
   - Forged document: Should show "FORGED" with high forgery probability

### Option 2: Using Python Script

```python
from ml_modules.document_forgery.predict import ForgeryDetector

detector = ForgeryDetector()

# Test genuine document
result1 = detector.predict('test_documents/sample_certificate.png')
print("Genuine:", result1)

# Test forged document
result2 = detector.predict('test_documents/forged_certificate.png')
print("Forged:", result2)
```

### Option 3: Command Line

```bash
cd ml_modules/document_forgery
python predict.py ../../test_documents/sample_certificate.png
python predict.py ../../test_documents/forged_certificate.png
```

## What to Look For

### Genuine Document Should Show:
- ✅ Forgery Probability: **< 30%**
- ✅ Classification: **GENUINE**
- ✅ Confidence: **HIGH**

### Forged Document Should Show:
- ⚠️ Forgery Probability: **> 70%**
- ⚠️ Classification: **FORGED**
- ⚠️ Confidence: **HIGH**
- ⚠️ Indicators: "Altered text detected", "Font inconsistency"

## Document Details

### Sample Certificate (Genuine)
```
Certificate ID: CERT-12345
Issue Date: 15/11/2024
Issued To: John Doe
Valid for: 2 years
```

### Forged Certificate (Altered)
```
Certificate ID: CERT-12345
Issue Date: 25/12/2024  ← ALTERED (was 15/11/2024)
Issued To: John Doe
Valid for: 2 years
```

**Forgery Type**: Date alteration with different font

## Create More Test Documents

To generate additional test documents:

```bash
python create_test_document.py
```

This will create fresh copies in the `test_documents/` folder.

## Training the Model

If you want to train the model on the full dataset:

```bash
cd ml_modules/document_forgery
python train.py
```

This trains on the 400 synthetic documents in `doc_data/`.

## Summary

✅ **2 test documents created**
✅ **1 genuine, 1 forged**
✅ **Ready to test immediately**
✅ **Multiple testing methods available**

**Just upload the documents to the web interface or use the Python scripts!** 🚀
