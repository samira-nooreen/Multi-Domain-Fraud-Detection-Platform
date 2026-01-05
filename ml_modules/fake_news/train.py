import pandas as pd
import numpy as np
import pickle
import os
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report

def extract_rule_features(text):
    """Extract rule-based features for fake news detection"""
    features = {}
    
    # Count excessive punctuation
    features['exclamation_count'] = text.count('!')
    features['question_count'] = text.count('?')
    features['caps_ratio'] = sum(1 for c in text if c.isupper()) / max(len(text), 1)
    
    # Check for sensational words
    sensational_words = ['shocking', 'unbelievable', 'you won\'t believe', 'secret', 'exposed', 'conspiracy']
    features['sensational_count'] = sum(1 for word in sensational_words if word in text.lower())
    
    # Check for excessive capitalization in words
    words = text.split()
    features['all_caps_words'] = sum(1 for word in words if word.isupper() and len(word) > 2)
    
    # Check for numbers (often used in fake news for false statistics)
    features['number_count'] = len(re.findall(r'\d+', text))
    
    return features

def train_model():
    print("Training Fake News Detection Model (Naive Bayes + Rule-based)...")
    
    # Define paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, '../../news_data.csv')
    model_dir = os.path.join(base_dir, 'models')
    
    os.makedirs(model_dir, exist_ok=True)
    
    # Load data
    if not os.path.exists(data_path):
        print(f"❌ Data file not found at {data_path}")
        # Create dummy data if not exists
        print("Creating dummy data for demonstration...")
        data = {
            'text': [
                'Breaking: Government announces new tax cuts for small businesses.',
                'Shocking: Aliens land in New York! Proof inside!',
                'Study shows coffee may reduce risk of heart disease.',
                'You won\'t believe this one trick to lose 50 lbs in a day!',
                'Local election results confirmed by officials.',
                'Secret society controls the weather - whistleblowers speak out!'
            ],
            'label': [0, 1, 0, 1, 0, 1]  # 0 = Real, 1 = Fake
        }
        df = pd.DataFrame(data)
    else:
        df = pd.read_csv(data_path)
        
    print(f"Loaded {len(df)} records")
    
    # Preprocessing
    # Assuming 'text' and 'label' columns exist
    if 'text' not in df.columns or 'label' not in df.columns:
        print("❌ Dataset must contain 'text' and 'label' columns")
        return
        
    X_text = df['text'].fillna('')
    y = df['label']
    
    # Extract rule-based features
    print("Extracting rule-based features...")
    rule_features = X_text.apply(extract_rule_features)
    rule_df = pd.DataFrame(rule_features.tolist())
    
    # Split data
    X_train_text, X_test_text, y_train, y_test = train_test_split(X_text, y, test_size=0.2, random_state=42)
    rule_train, rule_test = train_test_split(rule_df, test_size=0.2, random_state=42)
    
    # Vectorization
    print("Vectorizing text...")
    vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)
    X_train_vect = vectorizer.fit_transform(X_train_text)
    X_test_vect = vectorizer.transform(X_test_text)
    
    # Combine TF-IDF features with rule-based features
    print("Combining features...")
    from scipy.sparse import hstack
    X_train_combined = hstack([X_train_vect, rule_train.values])
    X_test_combined = hstack([X_test_vect, rule_test.values])
    
    # Train model
    print("Training Naive Bayes + Rule-based model...")
    clf = MultinomialNB()
    clf.fit(X_train_combined, y_train)
    
    # Evaluate
    y_pred = clf.predict(X_test_combined)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy:.2%}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save models
    print("Saving models...")
    model_data = {
        'classifier': clf,
        'vectorizer': vectorizer,
        'feature_names': rule_df.columns.tolist()
    }
    with open(os.path.join(model_dir, 'nb_model.pkl'), 'wb') as f:
        pickle.dump(model_data, f)
        
    with open(os.path.join(model_dir, 'vectorizer_model.pkl'), 'wb') as f:
        pickle.dump(vectorizer, f)
        
    print("✅ Training complete!")

if __name__ == "__main__":
    train_model()
