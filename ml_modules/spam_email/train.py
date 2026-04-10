"""
Spam Email Detection - Naive Bayes Training
Algorithm: Naive Bayes with TF-IDF
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
import joblib
import os
import warnings
warnings.filterwarnings('ignore')

def train_naive_bayes(train_texts, val_texts, train_labels, val_labels):
    """Train Naive Bayes (classic baseline)"""
    print("\n" + "="*60)
    print("📊 Training Naive Bayes (TF-IDF)")
    print("="*60)
    
    try:
        # TF-IDF Vectorization
        print("📝 Vectorizing with TF-IDF...")
        vectorizer = TfidfVectorizer(max_features=3000, ngram_range=(1, 2), stop_words='english')
        X_train = vectorizer.fit_transform(train_texts)
        X_val = vectorizer.transform(val_texts)
        
        # Train
        print("🚀 Training Naive Bayes...")
        model = MultinomialNB(alpha=0.1)
        model.fit(X_train, train_labels)
        
        # Evaluate
        preds = model.predict(X_val)
        proba = model.predict_proba(X_val)[:, 1]
        
        accuracy = accuracy_score(val_labels, preds)
        auc = roc_auc_score(val_labels, proba)
        
        print(f"\n✓ Naive Bayes Accuracy: {accuracy:.4f}")
        print(f"✓ Naive Bayes AUC-ROC: {auc:.4f}")
        print("\nClassification Report:")
        print(classification_report(val_labels, preds, target_names=['HAM', 'SPAM']))
        
        # Save
        os.makedirs('./models', exist_ok=True)
        joblib.dump({'model': model, 'vectorizer': vectorizer}, './models/nb_model.pkl')
        print("✓ Model saved to ./models/nb_model.pkl")
        
        return accuracy
    except Exception as e:
        print(f"❌ Error training Naive Bayes: {e}")
        return None

def main():
    print("\n" + "="*60)
    print("📧 SPAM EMAIL DETECTION - NAIVE BAYES TRAINING")
    print("="*60)
    
    # Load or generate data
    if not os.path.exists('spam_data.csv'):
        print("📦 Generating dataset...")
        from generate_data import generate_spam_data
        df = generate_spam_data(2000)
        df.to_csv('spam_data.csv', index=False)
    else:
        df = pd.read_csv('spam_data.csv')
    
    print(f"\n📊 Dataset: {len(df)} samples")
    print(f"   HAM (Legitimate): {len(df[df['label']==0])} | SPAM: {len(df[df['label']==1])}")
    
    # Split data
    train_texts, val_texts, train_labels, val_labels = train_test_split(
        df['text'].tolist(), 
        df['label'].tolist(), 
        test_size=0.2, 
        random_state=42,
        stratify=df['label']
    )
    
    print(f"   Train: {len(train_texts)} | Validation: {len(val_texts)}")
    
    # Train
    train_naive_bayes(train_texts, val_texts, train_labels, val_labels)
    
    print("\n✅ Training complete!")

if __name__ == "__main__":
    main()
