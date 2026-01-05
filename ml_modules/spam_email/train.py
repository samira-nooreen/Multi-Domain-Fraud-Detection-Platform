"""
Spam/Phishing Email Detection - Multi-Model Training
Implements: BERT/RoBERTa, Naive Bayes, Random Forest + TF-IDF, LSTM
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
import joblib
import os
import warnings
warnings.filterwarnings('ignore')

# Try importing deep learning libraries
try:
    import torch
    import torch.nn as nn
    from torch.utils.data import Dataset, DataLoader
    from transformers import DistilBertTokenizer, DistilBertForSequenceClassification, Trainer, TrainingArguments
    DEEP_LEARNING_AVAILABLE = True
except ImportError:
    DEEP_LEARNING_AVAILABLE = False
    print("⚠ PyTorch/Transformers not available")

# LSTM Model Definition
class LSTMSpamClassifier(nn.Module):
    def __init__(self, vocab_size, embedding_dim=128, hidden_dim=256, output_dim=2, n_layers=2, dropout=0.3):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, num_layers=n_layers,
                           bidirectional=False, dropout=dropout, batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_dim)
        self.dropout = nn.Dropout(dropout)
        
    def forward(self, text):
        embedded = self.dropout(self.embedding(text))
        output, (hidden, cell) = self.lstm(embedded)
        hidden = self.dropout(hidden[-1])
        return self.fc(hidden)

class EmailDataset(Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

def train_naive_bayes(train_texts, val_texts, train_labels, val_labels):
    """Train Naive Bayes (classic baseline)"""
    print("\n" + "="*60)
    print("📊 Training Naive Bayes (Classic Baseline)")
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

def train_random_forest(train_texts, val_texts, train_labels, val_labels):
    """Train Random Forest + TF-IDF"""
    print("\n" + "="*60)
    print("🌲 Training Random Forest + TF-IDF")
    print("="*60)
    
    try:
        # TF-IDF Vectorization
        print("📝 Vectorizing with TF-IDF...")
        vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 3), stop_words='english')
        X_train = vectorizer.fit_transform(train_texts)
        X_val = vectorizer.transform(val_texts)
        
        # Train
        print("🚀 Training Random Forest...")
        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=20,
            random_state=42,
            n_jobs=-1
        )
        model.fit(X_train, train_labels)
        
        # Evaluate
        preds = model.predict(X_val)
        proba = model.predict_proba(X_val)[:, 1]
        
        accuracy = accuracy_score(val_labels, preds)
        auc = roc_auc_score(val_labels, proba)
        
        print(f"\n✓ Random Forest Accuracy: {accuracy:.4f}")
        print(f"✓ Random Forest AUC-ROC: {auc:.4f}")
        print("\nClassification Report:")
        print(classification_report(val_labels, preds, target_names=['HAM', 'SPAM']))
        
        # Save
        os.makedirs('./models', exist_ok=True)
        joblib.dump({'model': model, 'vectorizer': vectorizer}, './models/rf_model.pkl')
        print("✓ Model saved to ./models/rf_model.pkl")
        
        return accuracy
    except Exception as e:
        print(f"❌ Error training Random Forest: {e}")
        return None

def train_lstm(train_texts, val_texts, train_labels, val_labels):
    """Train LSTM model"""
    print("\n" + "="*60)
    print("🧠 Training LSTM")
    print("="*60)
    
    if not DEEP_LEARNING_AVAILABLE:
        print("⚠ Skipping - PyTorch not available")
        return None
    
    try:
        # Build vocabulary
        from collections import Counter
        
        all_words = ' '.join(train_texts).lower().split()
        word_counts = Counter(all_words)
        vocab = {word: i+2 for i, (word, _) in enumerate(word_counts.most_common(5000))}
        vocab['<PAD>'] = 0
        vocab['<UNK>'] = 1
        
        def text_to_sequence(text, max_len=100):
            words = text.lower().split()
            seq = [vocab.get(word, 1) for word in words]
            if len(seq) < max_len:
                seq += [0] * (max_len - len(seq))
            else:
                seq = seq[:max_len]
            return seq
        
        X_train = torch.tensor([text_to_sequence(text) for text in train_texts])
        X_val = torch.tensor([text_to_sequence(text) for text in val_texts])
        y_train = torch.tensor(train_labels)
        y_val = torch.tensor(val_labels)
        
        # Create model
        model = LSTMSpamClassifier(vocab_size=len(vocab), embedding_dim=128, hidden_dim=256)
        optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
        criterion = nn.CrossEntropyLoss()
        
        # Training
        batch_size = 32
        epochs = 5
        
        print("🚀 Training LSTM...")
        for epoch in range(epochs):
            model.train()
            total_loss = 0
            for i in range(0, len(X_train), batch_size):
                batch_X = X_train[i:i+batch_size]
                batch_y = y_train[i:i+batch_size]
                
                optimizer.zero_grad()
                outputs = model(batch_X)
                loss = criterion(outputs, batch_y)
                loss.backward()
                optimizer.step()
                total_loss += loss.item()
            
            print(f"Epoch {epoch+1}/{epochs}, Loss: {total_loss/len(X_train)*batch_size:.4f}")
        
        # Evaluate
        model.eval()
        with torch.no_grad():
            outputs = model(X_val)
            preds = torch.argmax(outputs, dim=1).numpy()
            proba = torch.softmax(outputs, dim=1)[:, 1].numpy()
        
        accuracy = accuracy_score(val_labels, preds)
        auc = roc_auc_score(val_labels, proba)
        
        print(f"\n✓ LSTM Accuracy: {accuracy:.4f}")
        print(f"✓ LSTM AUC-ROC: {auc:.4f}")
        print("\nClassification Report:")
        print(classification_report(val_labels, preds, target_names=['HAM', 'SPAM']))
        
        # Save
        os.makedirs('./models', exist_ok=True)
        torch.save({
            'model_state': model.state_dict(),
            'vocab': vocab
        }, './models/lstm_model.pth')
        print("✓ Model saved to ./models/lstm_model.pth")
        
        return accuracy
    except Exception as e:
        print(f"❌ Error training LSTM: {e}")
        import traceback
        traceback.print_exc()
        return None

def train_distilbert(train_texts, val_texts, train_labels, val_labels):
    """Train DistilBERT model (BERT variant)"""
    print("\n" + "="*60)
    print("🤖 Training DistilBERT (Transformer)")
    print("="*60)
    
    if not DEEP_LEARNING_AVAILABLE:
        print("⚠ Skipping - PyTorch/Transformers not available")
        return None
    
    try:
        tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
        
        print("📝 Tokenizing texts...")
        train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=128)
        val_encodings = tokenizer(val_texts, truncation=True, padding=True, max_length=128)
        
        train_dataset = EmailDataset(train_encodings, train_labels)
        val_dataset = EmailDataset(val_encodings, val_labels)
        
        print("🏗️  Loading pre-trained model...")
        model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased', num_labels=2)
        
        training_args = TrainingArguments(
            output_dir='./results',
            num_train_epochs=3,
            per_device_train_batch_size=16,
            per_device_eval_batch_size=32,
            warmup_steps=100,
            weight_decay=0.01,
            logging_dir='./logs',
            logging_steps=50,
            eval_strategy="epoch",
            save_strategy="epoch",
            load_best_model_at_end=True,
        )
        
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=val_dataset
        )
        
        print("🚀 Training DistilBERT...")
        trainer.train()
        
        # Evaluate
        predictions = trainer.predict(val_dataset)
        preds = np.argmax(predictions.predictions, axis=1)
        proba = torch.softmax(torch.tensor(predictions.predictions), dim=1)[:, 1].numpy()
        
        accuracy = accuracy_score(val_labels, preds)
        auc = roc_auc_score(val_labels, proba)
        
        print(f"\n✓ DistilBERT Accuracy: {accuracy:.4f}")
        print(f"✓ DistilBERT AUC-ROC: {auc:.4f}")
        print("\nClassification Report:")
        print(classification_report(val_labels, preds, target_names=['HAM', 'SPAM']))
        
        # Save
        os.makedirs('./models', exist_ok=True)
        model.save_pretrained('./models/distilbert_model')
        tokenizer.save_pretrained('./models/distilbert_model')
        print("✓ Model saved to ./models/distilbert_model")
        
        return accuracy
    except Exception as e:
        print(f"❌ Error training DistilBERT: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    print("\n" + "="*60)
    print("📧 SPAM/PHISHING EMAIL DETECTION - MULTI-MODEL TRAINING")
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
    
    # Train all models
    results = {}
    
    results['Naive Bayes'] = train_naive_bayes(train_texts, val_texts, train_labels, val_labels)
    results['Random Forest'] = train_random_forest(train_texts, val_texts, train_labels, val_labels)
    results['LSTM'] = train_lstm(train_texts, val_texts, train_labels, val_labels)
    results['DistilBERT'] = train_distilbert(train_texts, val_texts, train_labels, val_labels)
    
    # Summary
    print("\n" + "="*60)
    print("📊 TRAINING SUMMARY")
    print("="*60)
    for model_name, accuracy in results.items():
        if accuracy is not None:
            print(f"  {model_name:20s}: {accuracy:.4f} ({accuracy*100:.2f}%)")
        else:
            print(f"  {model_name:20s}: Not trained")
    
    print("\n✅ Training complete!")

if __name__ == "__main__":
    main()
