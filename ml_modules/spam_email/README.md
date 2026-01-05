# 📧 Spam/Phishing Email Detection Module

## Overview
Advanced spam and phishing email detection system using multiple machine learning algorithms with ensemble voting to identify malicious emails and phishing attempts.

## 🧠 Implemented Algorithms

### 1. **BERT/RoBERTa (DistilBERT)** - Best for Email Body ⭐
- **Type**: Pre-trained transformer model
- **Accuracy**: ~92-95% (expected)
- **Weight in Ensemble**: 35%
- **Strengths**: 
  - Deep contextual understanding
  - Detects subtle phishing patterns
  - Pre-trained on massive text corpus
  - Best for complex email analysis
- **Use Case**: Primary model for production

### 2. **LSTM** - Sequential Pattern Detection
- **Type**: Recurrent Neural Network
- **Accuracy**: ~88-91% (expected)
- **Weight in Ensemble**: 25%
- **Strengths**:
  - Captures sequential text patterns
  - Good for email structure analysis
  - Detects phishing language flows
- **Use Case**: Deep learning baseline

### 3. **Random Forest + TF-IDF**
- **Type**: Ensemble ML with feature engineering
- **Accuracy**: ~85-88% (expected)
- **Weight in Ensemble**: 25%
- **Strengths**:
  - Fast inference
  - Handles high-dimensional features
  - Robust to noise
- **Use Case**: Fast, reliable predictions

### 4. **Naive Bayes** - Classic Baseline
- **Type**: Probabilistic classifier
- **Accuracy**: ~80-83% (expected)
- **Weight in Ensemble**: 15%
- **Strengths**:
  - Very fast
  - Works well with limited data
  - Classic spam detection approach
- **Use Case**: Quick baseline

## 📊 Ensemble Strategy

The system uses **weighted voting** where:
- Each model contributes a probability score
- Scores are weighted by model reliability
- Final prediction is weighted average
- Confidence based on model agreement

```
Final Score = (0.35 × DistilBERT) + (0.25 × LSTM) + 
              (0.25 × RandomForest) + (0.15 × NaiveBayes)
```

## 🚀 Usage

### Training
```bash
# Install dependencies
pip install transformers torch scikit-learn pandas numpy

# Generate dataset
python generate_data.py

# Train all models
python train.py
```

### Prediction
```python
from predict import SpamDetector

detector = SpamDetector()

# Ensemble prediction (recommended)
email_text = "URGENT: Your account will be suspended! Click here to verify now!"
result = detector.predict(email_text, use_ensemble=True)

print(result)
# {
#   'is_spam': True,
#   'spam_probability': 0.92,
#   'category': 'SPAM',
#   'confidence': 'HIGH',
#   'models_used': ['DistilBERT', 'LSTM', 'RandomForest', 'NaiveBayes'],
#   'individual_predictions': {...}
# }
```

## 📁 File Structure

```
spam_email/
├── generate_data.py      # Dataset generation
├── train.py              # Multi-model training
├── predict.py            # Ensemble prediction
├── requirements.txt      # Dependencies
├── README.md             # This file
├── spam_data.csv         # Training data
└── models/               # Trained models
    ├── distilbert_model/ # DistilBERT checkpoint
    ├── lstm_model.pth    # LSTM weights
    ├── rf_model.pkl      # Random Forest
    └── nb_model.pkl      # Naive Bayes
```

## 🎯 Performance Metrics

Expected performance on validation set:

| Model | Accuracy | AUC-ROC | Speed | Use Case |
|-------|----------|---------|-------|----------|
| Naive Bayes | 80-83% | 0.82 | ⚡⚡⚡ | Quick baseline |
| Random Forest | 85-88% | 0.87 | ⚡⚡⚡ | Fast production |
| LSTM | 88-91% | 0.90 | ⚡⚡ | Deep learning |
| DistilBERT | 92-95% | 0.94 | ⚡ | Best single model |
| **Ensemble** | **93-96%** | **0.95** | ⚡ | **Production (Best)** |

## 🔍 Spam/Phishing Indicators

The models detect:

1. **Spam Keywords**
   - "free", "winner", "cash", "prize"
   - "urgent", "limited time", "act now"
   - "buy now", "click here"

2. **Phishing Patterns**
   - Suspicious URLs (bit.ly, tinyurl)
   - Account verification requests
   - Password reset scams
   - Urgent action demands

3. **Malicious Text Patterns**
   - ALL CAPS text
   - Excessive exclamation marks!!!
   - Money/financial promises
   - Threatening language

4. **Link Detection**
   - Shortened URLs
   - Suspicious domains
   - Mismatched link text

## 💡 Why These Algorithms?

### BERT/DistilBERT - Best for NLP ⭐
- **Reason**: Email classification is an NLP task
- **Advantage**: Deep contextual understanding of text
- **Performance**: 92-95% accuracy expected

### LSTM - Sequential Patterns
- **Reason**: Emails have sequential structure
- **Advantage**: Captures text flow and patterns
- **Performance**: 88-91% accuracy expected

### Random Forest + TF-IDF - Fast & Robust
- **Reason**: Handles high-dimensional text features well
- **Advantage**: Fast, interpretable, robust
- **Performance**: 85-88% accuracy expected

### Naive Bayes - Classic Baseline
- **Reason**: Traditional spam detection approach
- **Advantage**: Very fast, works with limited data
- **Performance**: 80-83% accuracy expected

## 🛠️ Customization

### Adjust Ensemble Weights

Edit `predict.py`:
```python
predictions.append((nb_pred['spam_probability'], 0.15, 'Naive Bayes'))
predictions.append((rf_pred['spam_probability'], 0.25, 'Random Forest'))
predictions.append((lstm_pred['spam_probability'], 0.25, 'LSTM'))
predictions.append((bert_pred['spam_probability'], 0.35, 'DistilBERT'))
```

### Add Custom Spam Keywords

Edit `generate_data.py` to add domain-specific spam patterns.

## 📈 Feature Importance

Key features for spam detection:

1. **Spam keywords** - Presence of common spam words
2. **URL patterns** - Suspicious or shortened links
3. **Text formatting** - ALL CAPS, excessive punctuation
4. **Urgency indicators** - "urgent", "immediate", "now"
5. **Financial terms** - Money, cash, prize mentions

## 🔗 Integration with Flask App

The module integrates with the main Flask application:
```python
# In app.py
from ml_modules.spam_email.predict import SpamDetector

detector = SpamDetector()
result = detector.predict(email_text)
```

## 📚 References

- **BERT**: [Hugging Face Transformers](https://huggingface.co/distilbert-base-uncased)
- **LSTM**: [Understanding LSTM Networks](http://colah.github.io/posts/2015-08-Understanding-LSTMs/)
- **Random Forest**: [Scikit-learn Documentation](https://scikit-learn.org/stable/modules/ensemble.html#forest)

## 📄 License

Part of the ML Fraud Detection System
