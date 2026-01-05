# Document Forgery Detection - Dataset Sources

## Overview
Document forgery detection requires image datasets of genuine and forged documents. The module uses **CNN (ResNet)** for image analysis and **OCR** for text extraction.

## Recommended Datasets

### 1. **Tobacco-800 Document Image Dataset** (Recommended)
- **Source**: [Tobacco-800 on Kaggle](https://www.kaggle.com/datasets/patrickaudriaz/tobacco800-document-image-dataset)
- **Description**: 800 document images across 10 categories
- **Format**: Images (JPEG/PNG)
- **Use Case**: Document classification and forgery detection
- **Download**:
  ```bash
  kaggle datasets download -d patrickaudriaz/tobacco800-document-image-dataset
  ```

### 2. **RVL-CDIP Dataset**
- **Source**: [RVL-CDIP on Hugging Face](https://huggingface.co/datasets/rvl_cdip)
- **Description**: 400,000 grayscale images in 16 classes
- **Size**: ~40GB
- **Classes**: Letter, form, email, handwritten, advertisement, etc.
- **Use Case**: Large-scale document classification

### 3. **MIDV-500/MIDV-2019** (ID Documents)
- **Source**: [MIDV-500 Dataset](http://l3i-share.univ-lr.fr/MIDV500/midv500.html)
- **Description**: 500 video clips of 50 different identity documents
- **Format**: Video frames (can extract images)
- **Use Case**: ID card/passport forgery detection
- **Features**: Multiple lighting conditions, angles

### 4. **Synthetic Document Dataset** (For Training)
- **Create your own** using document templates
- **Tools**:
  - [DocumentAI](https://cloud.google.com/document-ai)
  - [Faker](https://faker.readthedocs.io/) for fake data
  - [Pillow](https://pillow.readthedocs.io/) for image manipulation

### 5. **Signature Verification Datasets**
- **CEDAR Signature Database**: [Link](http://www.cedar.buffalo.edu/NIJ/data/)
- **GPDS Signature Database**: 4,000 signatures
- **Use Case**: Signature forgery detection

## Quick Start: Generate Synthetic Dataset

I can create a script to generate a synthetic document dataset for testing:

```python
# generate_document_dataset.py
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import random

def generate_document_images(n_genuine=500, n_forged=500):
    """
    Generate synthetic document images
    - Genuine: Clean, consistent formatting
    - Forged: Altered text, inconsistent fonts, artifacts
    """
    os.makedirs('document_dataset/genuine', exist_ok=True)
    os.makedirs('document_dataset/forged', exist_ok=True)
    
    # Generate genuine documents
    for i in range(n_genuine):
        img = create_genuine_document()
        img.save(f'document_dataset/genuine/doc_{i}.png')
    
    # Generate forged documents
    for i in range(n_forged):
        img = create_forged_document()
        img.save(f'document_dataset/forged/doc_{i}.png')

def create_genuine_document():
    # Create clean document with consistent formatting
    img = Image.new('RGB', (800, 1000), 'white')
    draw = ImageDraw.Draw(img)
    # Add text, lines, etc.
    return img

def create_forged_document():
    # Create document with forgery indicators
    img = Image.new('RGB', (800, 1000), 'white')
    draw = ImageDraw.Draw(img)
    # Add altered text, inconsistent fonts, etc.
    return img
```

## Current Implementation Status

Let me check what's currently in the document_forgery module:
