"""
Quick Demo - Spam/Phishing Email Detection
Works without PyTorch - uses Naive Bayes & Random Forest
"""
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import os

print("="*70)
print("📧 SPAM/PHISHING EMAIL DETECTION - QUICK DEMO")
print("="*70)

# Load or generate data
if not os.path.exists('spam_data.csv'):
    print("\n📦 Generating dataset...")
    from generate_data import generate_spam_data
    df = generate_spam_data(1000)
    df.to_csv('spam_data.csv', index=False)
else:
    df = pd.read_csv('spam_data.csv')

print(f"\n📊 Dataset: {len(df)} samples")
print(f"   HAM (Legitimate): {len(df[df['label']==0])} | SPAM: {len(df[df['label']==1])}")

# Split
train_texts, val_texts, train_labels, val_labels = train_test_split(
    df['text'].tolist(), df['label'].tolist(), 
    test_size=0.2, random_state=42, stratify=df['label']
)

# Vectorize
print("\n📝 Vectorizing with TF-IDF...")
vectorizer = TfidfVectorizer(max_features=3000, ngram_range=(1, 2), stop_words='english')
X_train = vectorizer.fit_transform(train_texts)
X_val = vectorizer.transform(val_texts)

# Train models
print("\n🚀 Training models...")

print("   1. Naive Bayes...", end=" ")
nb = MultinomialNB(alpha=0.1)
nb.fit(X_train, train_labels)
nb_acc = accuracy_score(val_labels, nb.predict(X_val))
print(f"✓ Accuracy: {nb_acc:.2%}")

print("   2. Random Forest...", end=" ")
rf = RandomForestClassifier(n_estimators=100, max_depth=20, random_state=42, n_jobs=-1)
rf.fit(X_train, train_labels)
rf_acc = accuracy_score(val_labels, rf.predict(X_val))
print(f"✓ Accuracy: {rf_acc:.2%}")

# Test predictions
print("\n" + "="*70)
print("🧪 TESTING PREDICTIONS")
print("="*70)

test_cases = [
    "Hi John, let's schedule a meeting to discuss the Q4 report.",
    "URGENT: Your account will be suspended! Click here to verify now!",
    "Team update: The project deadline has been moved to next Monday.",
    "Congratulations! You've won $10000! Claim your prize at bit.ly/xyz123"
]

for i, text in enumerate(test_cases, 1):
    X = vectorizer.transform([text])
    
    nb_proba = nb.predict_proba(X)[0][1]
    rf_proba = rf.predict_proba(X)[0][1]
    ensemble = (nb_proba * 0.4 + rf_proba * 0.6)  # Weighted average
    
    print(f"\n{i}. {text[:55]}...")
    print(f"   Naive Bayes: {nb_proba:.2%} | Random Forest: {rf_proba:.2%} | Ensemble: {ensemble:.2%}")
    print(f"   → {'🚨 SPAM' if ensemble > 0.5 else '✅ HAM'}")

print("\n" + "="*70)
print("✅ Demo complete!")
print("\nTo train all 4 models (including DistilBERT & LSTM):")
print("  1. Install: pip install transformers torch")
print("  2. Run: python train.py")
print("="*70)
