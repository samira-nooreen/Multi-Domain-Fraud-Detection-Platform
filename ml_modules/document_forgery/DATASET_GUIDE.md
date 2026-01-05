# Document Forgery Detection - Complete Dataset Guide

## Quick Answer

**You have 3 options:**

### Option 1: Generate Synthetic Dataset (Easiest - Already Done!)
I've created a script that generates realistic document images:

```bash
cd ml_modules/document_forgery
python generate_data.py
```

This creates:
- **200 genuine documents** in `doc_data/genuine/`
- **200 forged documents** in `doc_data/forged/`

**Features of generated documents:**
- Genuine: Clean formatting, consistent fonts, proper alignment
- Forged: Altered text, compression artifacts, mixed fonts, copy-paste signs

### Option 2: Download Real Datasets (Best for Production)

#### A. Tobacco-800 (Recommended for Document Classification)
```bash
# Install Kaggle CLI
pip install kaggle

# Download dataset
kaggle datasets download -d patrickaudriaz/tobacco800-document-image-dataset
unzip tobacco800-document-image-dataset.zip -d ml_modules/document_forgery/tobacco800/
```

#### B. RVL-CDIP (Large-scale, 400K images)
```bash
# Using Hugging Face datasets
pip install datasets
```

```python
from datasets import load_dataset
dataset = load_dataset("rvl_cdip")
```

#### C. MIDV-500 (ID Documents)
- Download from: http://l3i-share.univ-lr.fr/MIDV500/midv500.html
- Contains: 500 video clips of 50 ID documents
- Extract frames for training

### Option 3: Create Custom Dataset

Scan/photograph real documents and create your own dataset:

```
doc_data/
├── genuine/
│   ├── passport_001.jpg
│   ├── id_card_001.jpg
│   └── ...
└── forged/
    ├── altered_passport_001.jpg
    ├── fake_id_001.jpg
    └── ...
```

## Current Implementation

### What's Already Set Up

1. ✅ **Dataset Generator** (`generate_data.py`)
   - Creates 400 synthetic documents
   - Simulates forgery techniques
   - Ready to use immediately

2. ✅ **Training Script** (`train.py`)
   - Uses CNN (ResNet-like architecture)
   - Trains on generated images
   - Saves model as `forgery_model.pkl`

3. ✅ **Prediction Script** (`predict.py`)
   - Loads trained model
   - Analyzes document images
   - Returns forgery probability

### How to Use

#### Step 1: Generate Dataset
```bash
cd ml_modules/document_forgery
python generate_data.py
```

Output:
```
Generating 200 genuine + 200 forged documents...
✓ Generated 200 genuine documents
✓ Generated 200 forged documents
✅ Total: 400 documents in doc_data/
```

#### Step 2: Train Model
```bash
python train.py
```

This will:
- Load images from `doc_data/`
- Train CNN model
- Save to `forgery_model.pkl`

#### Step 3: Test Prediction
```bash
python predict.py
```

## Forgery Detection Techniques Implemented

### 1. **Altered Text Detection**
- Inconsistent font sizes
- Color variations
- Misaligned text

### 2. **Copy-Paste Detection**
- Duplicate signatures
- Cloned regions
- Pattern repetition

### 3. **Compression Artifacts**
- JPEG artifacts
- Noise patterns
- Quality inconsistencies

### 4. **Mixed Fonts**
- Inconsistent typography
- Font family changes
- Size variations

## Real-World Dataset Recommendations

### For ID Documents (Passports, Driver's Licenses)
1. **MIDV-500**: 50 different ID types
2. **MIDV-2019**: Extended version with 1000+ samples

### For General Documents
1. **Tobacco-800**: Business documents
2. **RVL-CDIP**: 400K document images, 16 categories

### For Signatures
1. **CEDAR**: Signature verification
2. **GPDS**: 4,000 signatures with forgeries

## Dataset Structure

```
ml_modules/document_forgery/
├── doc_data/
│   ├── genuine/
│   │   ├── doc_0000.png
│   │   ├── doc_0001.png
│   │   └── ... (200 files)
│   └── forged/
│       ├── doc_0000.png
│       ├── doc_0001.png
│       └── ... (200 files)
├── generate_data.py      # ✅ Creates synthetic dataset
├── train.py              # ✅ Trains CNN model
├── predict.py            # ✅ Makes predictions
└── forgery_model.pkl     # Trained model
```

## Next Steps

### For Quick Testing (Recommended)
```bash
# 1. Generate synthetic data
cd ml_modules/document_forgery
python generate_data.py

# 2. Train model
python train.py

# 3. Test
python predict.py
```

### For Production Use
1. Download **Tobacco-800** or **MIDV-500**
2. Organize into `genuine/` and `forged/` folders
3. Update `train.py` to point to new dataset
4. Retrain model

## Summary

✅ **Synthetic dataset generator** - Ready to use
✅ **Training pipeline** - Already implemented
✅ **Real dataset sources** - Documented above

**You can start testing immediately with the synthetic data, then upgrade to real datasets for production!**
