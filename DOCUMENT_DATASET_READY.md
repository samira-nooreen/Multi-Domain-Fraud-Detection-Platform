# ✅ Document Forgery Detection - Dataset Ready!

## What I Did

I created a **realistic document dataset generator** and generated 400 synthetic documents for you.

## Generated Dataset

```
✅ 200 genuine documents
✅ 200 forged documents
✅ Total: 400 documents in doc_data/
```

### Location
```
ml_modules/document_forgery/doc_data/
├── genuine/     (200 clean documents)
└── forged/      (200 altered documents)
```

## Document Features

### Genuine Documents Include:
- ✅ Official header with title
- ✅ Document ID and date
- ✅ Consistent formatting
- ✅ Proper text alignment
- ✅ Simulated signature
- ✅ Official stamp
- ✅ Clean, professional appearance

### Forged Documents Include:
- ⚠️ **Altered text** (different fonts/colors)
- ⚠️ **Copy-paste artifacts** (duplicate signatures)
- ⚠️ **Compression artifacts** (blur, noise)
- ⚠️ **Mixed fonts** (inconsistent typography)

## Forgery Techniques Simulated

1. **Text Alteration**: Overwrites with different fonts
2. **Copy-Paste**: Duplicates signatures/stamps
3. **Compression**: Adds JPEG artifacts and noise
4. **Font Mixing**: Inconsistent typography

## Next Steps

### Option 1: Use Synthetic Data (Quick Testing)
```bash
cd ml_modules/document_forgery
python train.py  # Train CNN model on synthetic data
```

### Option 2: Download Real Datasets (Production)

#### Tobacco-800 (Business Documents)
```bash
kaggle datasets download -d patrickaudriaz/tobacco800-document-image-dataset
```

#### MIDV-500 (ID Documents)
- Download: http://l3i-share.univ-lr.fr/MIDV500/midv500.html
- Best for: Passport/ID card forgery detection

#### RVL-CDIP (Large-scale, 400K images)
```python
from datasets import load_dataset
dataset = load_dataset("rvl_cdip")
```

## Real Dataset Sources Summary

| Dataset | Size | Type | Best For |
|---------|------|------|----------|
| **Synthetic** | 400 | Generated | Quick testing ✅ |
| **Tobacco-800** | 800 | Real documents | Business docs |
| **MIDV-500** | 500+ | ID documents | Passports/IDs |
| **RVL-CDIP** | 400K | Mixed | Large-scale |
| **CEDAR** | 1,000+ | Signatures | Signature verification |

## Current Status

✅ **Dataset Generated**: 400 synthetic documents
✅ **Generator Script**: `generate_data.py` (can create more)
✅ **Training Script**: `train.py` (ready to train CNN)
✅ **Prediction Script**: `predict.py` (ready to detect forgeries)

## How to Train

```bash
# Navigate to module
cd ml_modules/document_forgery

# Train CNN model
python train.py

# This will:
# 1. Load 400 images from doc_data/
# 2. Train ResNet-like CNN
# 3. Save model as forgery_model.pkl
```

## Summary

You now have:
1. ✅ **400 synthetic documents** ready to use
2. ✅ **Realistic forgery patterns** (4 different types)
3. ✅ **Complete training pipeline** ready
4. ✅ **Real dataset sources** documented for production

**You can start training immediately with the synthetic data, then upgrade to real datasets when needed!** 🚀
