"""
Spam/Phishing Email Prediction - Ensemble Multi-Model Approach
Uses DistilBERT, LSTM, Random Forest + TF-IDF, and Naive Bayes
"""
import numpy as np
import joblib
import os
import warnings
warnings.filterwarnings('ignore')

# Try importing deep learning libraries
PYTORCH_AVAILABLE = False
LSTMSpamClassifier = None

try:
    import torch
    import torch.nn as nn
    from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
    PYTORCH_AVAILABLE = True
    
    # LSTM Model Definition (must match training)
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
            
except Exception as e:
    PYTORCH_AVAILABLE = False
    print(f"⚠ PyTorch/Transformers not available: {e}")
    print("  → Will use classical ML models (Naive Bayes, Random Forest) only")

class SpamDetector:
    def __init__(self, model_dir=None):
        if model_dir is None:
            # Look for models in the same directory as this file
            import os
            model_dir = os.path.join(os.path.dirname(__file__), 'models')
        self.model_dir = model_dir
        self.models = {}
        self.load_all_models()
        
    def load_all_models(self):
        """Load all available trained models"""
        print("🔄 Loading models...")
        
        # Load Naive Bayes
        try:
            with open(f'{self.model_dir}/nb_model.pkl', 'rb') as f:
                self.models['naive_bayes'] = joblib.load(f)
            print("  ✓ Naive Bayes loaded")
        except:
            print("  ⚠ Naive Bayes not found")
        
        # Load Random Forest
        try:
            with open(f'{self.model_dir}/rf_model.pkl', 'rb') as f:
                self.models['random_forest'] = joblib.load(f)
            print("  ✓ Random Forest loaded")
        except:
            print("  ⚠ Random Forest not found")
        
        # Load LSTM
        if PYTORCH_AVAILABLE:
            try:
                checkpoint = torch.load(f'{self.model_dir}/lstm_model.pth')
                vocab = checkpoint['vocab']
                model = LSTMSpamClassifier(vocab_size=len(vocab))
                model.load_state_dict(checkpoint['model_state'])
                model.eval()
                self.models['lstm'] = {'model': model, 'vocab': vocab}
                print("  ✓ LSTM loaded")
            except:
                print("  ⚠ LSTM not found")
            
            # Load DistilBERT
            try:
                tokenizer = DistilBertTokenizer.from_pretrained(f'{self.model_dir}/distilbert_model')
                model = DistilBertForSequenceClassification.from_pretrained(f'{self.model_dir}/distilbert_model')
                model.eval()
                self.models['distilbert'] = {'model': model, 'tokenizer': tokenizer}
                print("  ✓ DistilBERT loaded")
            except:
                print("  ⚠ DistilBERT not found")
        
        if not self.models:
            print("  ⚠ No models loaded - using fallback heuristics")
    
    def predict_naive_bayes(self, text):
        """Predict using Naive Bayes"""
        if 'naive_bayes' not in self.models:
            return None
        
        try:
            model_data = self.models['naive_bayes']
            vectorizer = model_data['vectorizer']
            model = model_data['model']
            
            X = vectorizer.transform([text])
            proba = model.predict_proba(X)[0]
            
            return {
                'spam_probability': float(proba[1]),
                'model': 'Naive Bayes'
            }
        except Exception as e:
            print(f"Error in Naive Bayes: {e}")
            return None
    
    def predict_random_forest(self, text):
        """Predict using Random Forest"""
        if 'random_forest' not in self.models:
            return None
        
        try:
            model_data = self.models['random_forest']
            vectorizer = model_data['vectorizer']
            model = model_data['model']
            
            X = vectorizer.transform([text])
            proba = model.predict_proba(X)[0]
            
            return {
                'spam_probability': float(proba[1]),
                'model': 'Random Forest'
            }
        except Exception as e:
            print(f"Error in Random Forest: {e}")
            return None
    
    def predict_lstm(self, text):
        """Predict using LSTM"""
        if 'lstm' not in self.models or not PYTORCH_AVAILABLE:
            return None
        
        try:
            model_data = self.models['lstm']
            model = model_data['model']
            vocab = model_data['vocab']
            
            # Tokenize
            def text_to_sequence(text, max_len=100):
                words = text.lower().split()
                seq = [vocab.get(word, 1) for word in words]
                if len(seq) < max_len:
                    seq += [0] * (max_len - len(seq))
                else:
                    seq = seq[:max_len]
                return seq
            
            X = torch.tensor([text_to_sequence(text)])
            
            with torch.no_grad():
                outputs = model(X)
                proba = torch.softmax(outputs, dim=1)[0]
            
            return {
                'spam_probability': float(proba[1]),
                'model': 'LSTM'
            }
        except Exception as e:
            print(f"Error in LSTM: {e}")
            return None
    
    def predict_distilbert(self, text):
        """Predict using DistilBERT"""
        if 'distilbert' not in self.models or not PYTORCH_AVAILABLE:
            return None
        
        try:
            model_data = self.models['distilbert']
            model = model_data['model']
            tokenizer = model_data['tokenizer']
            
            inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128)
            
            with torch.no_grad():
                outputs = model(**inputs)
            
            logits = outputs.logits
            proba = torch.softmax(logits, dim=1)[0]
            
            return {
                'spam_probability': float(proba[1]),
                'model': 'DistilBERT'
            }
        except Exception as e:
            print(f"Error in DistilBERT: {e}")
            return None
    
    def predict_ensemble(self, text, method='weighted'):
        """
        Ensemble prediction using all available models
        
        Args:
            text: Email text to classify
            method: 'weighted' or 'voting'
        """
        predictions = []
        
        # Get predictions from all models
        nb_pred = self.predict_naive_bayes(text)
        if nb_pred:
            predictions.append((nb_pred['spam_probability'], 0.15, 'Naive Bayes'))
        
        rf_pred = self.predict_random_forest(text)
        if rf_pred:
            predictions.append((rf_pred['spam_probability'], 0.25, 'Random Forest'))
        
        lstm_pred = self.predict_lstm(text)
        if lstm_pred:
            predictions.append((lstm_pred['spam_probability'], 0.25, 'LSTM'))
        
        bert_pred = self.predict_distilbert(text)
        if bert_pred:
            predictions.append((bert_pred['spam_probability'], 0.35, 'DistilBERT'))
        
        if not predictions:
            return self._mock_predict(text)
        
        # Weighted average
        if method == 'weighted':
            total_weight = sum(weight for _, weight, _ in predictions)
            weighted_prob = sum(prob * weight for prob, weight, _ in predictions) / total_weight
        else:
            # Simple average
            weighted_prob = sum(prob for prob, _, _ in predictions) / len(predictions)
        
        # Determine confidence based on agreement
        probs = [prob for prob, _, _ in predictions]
        std_dev = (sum((p - weighted_prob)**2 for p in probs) / len(probs)) ** 0.5
        
        if std_dev < 0.1:
            confidence = 'HIGH'
        elif std_dev < 0.2:
            confidence = 'MEDIUM'
        else:
            confidence = 'LOW'
        
        return {
            'is_spam': bool(weighted_prob > 0.5),
            'spam_probability': float(weighted_prob),
            'category': 'SPAM' if weighted_prob > 0.5 else 'HAM',
            'confidence': confidence,
            'models_used': [name for _, _, name in predictions],
            'individual_predictions': {
                name: {'probability': float(prob), 'weight': weight} 
                for prob, weight, name in predictions
            }
        }
    
    def _process_minimal_inputs(self, data):
        """Convert minimal user inputs to full email text"""
        # Extract minimal inputs
        sender_email = data.get('sender_email', '')
        email_content = data.get('email_content', '')
        
        # Combine into a single text for analysis
        # In a real implementation, we might extract more features from sender_email
        full_text = f"From: {sender_email}\n\n{email_content}"
        return full_text
    
    def predict(self, text, use_ensemble=True):
        """
        Main prediction method
        
        Args:
            text: Email text to classify
            use_ensemble: If True, use ensemble; otherwise use best single model
        """
        if use_ensemble:
            return self.predict_ensemble(text)
        
        # Try models in order of preference
        for predict_fn in [self.predict_distilbert, self.predict_lstm, 
                          self.predict_random_forest, self.predict_naive_bayes]:
            result = predict_fn(text)
            if result:
                spam_prob = result['spam_probability']
                return {
                    'is_spam': bool(spam_prob > 0.5),
                    'spam_probability': float(spam_prob),
                    'category': 'SPAM' if spam_prob > 0.5 else 'HAM',
                    'confidence': 'HIGH' if abs(spam_prob - 0.5) > 0.3 else 'MEDIUM',
                    'model_used': result['model']
                }
        
        # Fallback
        return self._mock_predict(text)
    
    def _mock_predict(self, text):
        """Fallback heuristic-based prediction"""
        spam_keywords = [
            'free', 'winner', 'urgent', 'click here', 'buy now', 'limited time',
            'offer', 'money', 'cash', 'prize', 'congratulations', 'claim',
            'verify', 'suspended', 'account', 'password', 'reset', 'confirm'
        ]
        
        phishing_indicators = [
            'http://', 'https://', 'bit.ly', 'tinyurl', '.com', 'click',
            'verify', 'urgent', 'suspended', 'locked'
        ]
        
        text_lower = text.lower()
        
        score = 0
        
        # Check for spam keywords
        for word in spam_keywords:
            if word in text_lower:
                score += 0.1
        
        # Check for phishing indicators
        for indicator in phishing_indicators:
            if indicator in text_lower:
                score += 0.15
        
        # Check for all caps (spam indicator)
        if sum(1 for c in text if c.isupper()) / max(len(text), 1) > 0.3:
            score += 0.2
        
        # Check for excessive exclamation marks
        if text.count('!') > 2:
            score += 0.15
        
        spam_prob = min(0.95, score)
        
        return {
            'is_spam': bool(spam_prob > 0.5),
            'spam_probability': float(spam_prob),
            'category': 'SPAM' if spam_prob > 0.5 else 'HAM',
            'confidence': 'LOW',
            'model_used': 'Heuristic Fallback'
        }

if __name__ == "__main__":
    # Test the detector
    detector = SpamDetector()
    
    test_cases = [
        "Hi John, let's schedule a meeting to discuss the Q4 report.",
        "URGENT: Your account will be suspended! Click here to verify now!",
        "Team update: The project deadline has been moved to next Monday.",
        "Congratulations! You've won $10000! Claim your prize at bit.ly/xyz123"
    ]
    
    print("\n" + "="*60)
    print("🧪 Testing Spam/Phishing Detector")
    print("="*60)
    
    for text in test_cases:
        print(f"\n📧 Email: {text[:60]}...")
        result = detector.predict(text, use_ensemble=True)
        print(f"   Result: {'🚨 SPAM' if result['is_spam'] else '✅ HAM'}")
        print(f"   Probability: {result['spam_probability']:.2%}")
        print(f"   Confidence: {result['confidence']}")
        if 'models_used' in result:
            print(f"   Models: {', '.join(result['models_used'])}")
