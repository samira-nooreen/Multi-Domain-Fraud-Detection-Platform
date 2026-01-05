# Click Fraud Prediction - Ensemble Multi-Model Approach
# Algorithms: CatBoost, Logistic Regression, Autoencoder, Wide & Deep, LSTM, Isolation Forest

import numpy as np
import joblib
import os
import warnings
warnings.filterwarnings('ignore')
# Try importing deep learning libraries (guard against DLL errors)
try:
    import torch
    import torch.nn as nn
    PYTORCH_AVAILABLE = True
except Exception as e:
    torch = None
    nn = None
    PYTORCH_AVAILABLE = False
    print(f"⚠ PyTorch not available: {e}")

# ---------------------------------------------------------------------------
# Model definitions (must match training)
# ---------------------------------------------------------------------------
if PYTORCH_AVAILABLE:
    class ClickAutoencoder(nn.Module):
        def __init__(self, input_dim=15, encoding_dim=8):
            super().__init__()
            self.encoder = nn.Sequential(
                nn.Linear(input_dim, 32),
                nn.ReLU(),
                nn.Dropout(0.2),
                nn.Linear(32, 16),
                nn.ReLU(),
                nn.Linear(16, encoding_dim),
                nn.ReLU()
            )
            self.decoder = nn.Sequential(
                nn.Linear(encoding_dim, 16),
                nn.ReLU(),
                nn.Linear(16, 32),
                nn.ReLU(),
                nn.Dropout(0.2),
                nn.Linear(32, input_dim)
            )
        def forward(self, x):
            encoded = self.encoder(x)
            decoded = self.decoder(encoded)
            return decoded

    class WideDeepModel(nn.Module):
        def __init__(self, input_dim=15):
            super().__init__()
            self.wide = nn.Linear(input_dim, 1)
            self.deep = nn.Sequential(
                nn.Linear(input_dim, 64),
                nn.ReLU(),
                nn.BatchNorm1d(64),
                nn.Dropout(0.3),
                nn.Linear(64, 32),
                nn.ReLU(),
                nn.BatchNorm1d(32),
                nn.Dropout(0.2),
                nn.Linear(32, 16),
                nn.ReLU(),
                nn.Linear(16, 1)
            )
        def forward(self, x):
            wide_out = self.wide(x)
            deep_out = self.deep(x)
            return torch.sigmoid(wide_out + deep_out)

    class ClickLSTM(nn.Module):
        def __init__(self, input_dim=8, hidden_dim=64, num_layers=2):
            super().__init__()
            self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True, dropout=0.2)
            self.fc = nn.Sequential(
                nn.Linear(hidden_dim, 32),
                nn.ReLU(),
                nn.Linear(32, 1)
            )
        def forward(self, x):
            lstm_out, _ = self.lstm(x)
            last_step = lstm_out[:, -1, :]
            out = torch.sigmoid(self.fc(last_step))
            return out
else:
    ClickAutoencoder = None
    WideDeepModel = None
    ClickLSTM = None

# ---------------------------------------------------------------------------
# Detector class
# ---------------------------------------------------------------------------
class ClickFraudDetector:
    def __init__(self, model_dir='./models'):
        self.model_dir = model_dir
        self.models = {}
        self.load_all_models()

    def load_all_models(self):
        """Load all trained models (CatBoost, Logistic Regression, Autoencoder, Wide & Deep, LSTM, Isolation Forest)."""
        print("🔄 Loading models...")
        # Logistic Regression (saved as logreg_model.pkl)
        try:
            with open(os.path.join(self.model_dir, 'logreg_model.pkl'), 'rb') as f:
                self.models['logistic_regression'] = joblib.load(f)
            print("  ✓ Logistic Regression loaded")
        except Exception:
            print("  ⚠ Logistic Regression not found")
        # CatBoost
        try:
            self.models['catboost'] = joblib.load(os.path.join(self.model_dir, 'catboost_model.pkl'))
            print("  ✓ CatBoost loaded")
        except Exception:
            print("  ⚠ CatBoost not found")
        # Autoencoder
        if PYTORCH_AVAILABLE:
            try:
                checkpoint = torch.load(os.path.join(self.model_dir, 'autoencoder_model.pth'))
                model = ClickAutoencoder()
                model.load_state_dict(checkpoint['model_state'])
                model.eval()
                self.models['autoencoder'] = {
                    'model': model,
                    'threshold': checkpoint['threshold'],
                    'scaler': checkpoint['scaler']
                }
                print("  ✓ Autoencoder loaded")
            except Exception:
                print("  ⚠ Autoencoder not found")
            # Wide & Deep
            try:
                checkpoint = torch.load(os.path.join(self.model_dir, 'widedeep_model.pth'))
                model = WideDeepModel()
                model.load_state_dict(checkpoint['model_state'])
                model.eval()
                self.models['widedeep'] = {
                    'model': model,
                    'scaler': checkpoint['scaler']
                }
                print("  ✓ Wide & Deep loaded")
            except Exception:
                print("  ⚠ Wide & Deep not found")
            # LSTM
            try:
                checkpoint = torch.load(os.path.join(self.model_dir, 'lstm_model.pth'))
                model = ClickLSTM()
                model.load_state_dict(checkpoint)
                model.eval()
                self.models['lstm'] = model
                print("  ✓ LSTM loaded")
            except Exception:
                print("  ⚠ LSTM not found")
        # Isolation Forest (tabular)
        try:
            self.models['isolation_forest'] = joblib.load(os.path.join(self.model_dir, 'isolation_forest.pkl'))
            print("  ✓ Isolation Forest loaded")
        except Exception:
            print("  ⚠ Isolation Forest not found")
        if not self.models:
            print("  ⚠ No models loaded – fallback heuristics will be used")

    # ---------------------------------------------------------------------
    # Feature engineering – aggregate sequential click data into a fixed vector
    # ---------------------------------------------------------------------
    def aggregate_sequence_features(self, sequence_data):
        """Convert raw click sequence into a 15‑dimensional feature vector.
        Expected sequence_data format: list of lists/tuples where each element
        contains at least [time_diff, x, y, ip_change, ua_change, hour, weekend, velocity].
        """
        if not sequence_data:
            return np.zeros(15)
        seq = np.array(sequence_data)
        if seq.shape[1] >= 8:
            feats = [
                np.mean(seq[:, 0]), np.std(seq[:, 0]), np.min(seq[:, 0]), np.max(seq[:, 0]),
                np.mean(seq[:, 1]), np.std(seq[:, 1]),
                np.mean(seq[:, 2]), np.std(seq[:, 2]),
                np.sum(seq[:, 3]), np.sum(seq[:, 4]),
                np.mean(seq[:, 5]), np.mean(seq[:, 6]),
                np.mean(seq[:, 7]), np.std(seq[:, 7]),
                len(sequence_data)
            ]
        else:
            # fallback for shorter feature sets
            feats = [
                np.mean(seq[:, 0]), np.std(seq[:, 0]), np.min(seq[:, 0]), np.max(seq[:, 0]),
                np.mean(seq[:, 1]), np.std(seq[:, 1]),
                np.mean(seq[:, 2]), np.std(seq[:, 2]),
                np.sum(seq[:, 3]) if seq.shape[1] > 3 else 0,
                0, 12, 0, 10, 5, len(sequence_data)
            ]
        return np.array(feats)

    # ---------------------------------------------------------------------
    # Individual model prediction helpers
    # ---------------------------------------------------------------------
    def predict_logistic_regression(self, features):
        if 'logistic_regression' not in self.models:
            return None
        try:
            model_data = self.models['logistic_regression']
            scaler = model_data['scaler']
            model = model_data['model']
            X = scaler.transform([features])
            proba = model.predict_proba(X)[0][1]
            return {'fraud_probability': float(proba), 'model': 'Logistic Regression'}
        except Exception as e:
            print(f"Error in Logistic Regression: {e}")
            return None

    def predict_catboost(self, features):
        if 'catboost' not in self.models:
            return None
        try:
            model = self.models['catboost']
            proba = model.predict_proba([features])[0][1]
            return {'fraud_probability': float(proba), 'model': 'CatBoost'}
        except Exception as e:
            print(f"Error in CatBoost: {e}")
            return None

    def predict_autoencoder(self, features):
        if 'autoencoder' not in self.models or not PYTORCH_AVAILABLE:
            return None
        try:
            data = self.models['autoencoder']
            model = data['model']
            scaler = data['scaler']
            threshold = data['threshold']
            X = scaler.transform([features])
            X_tensor = torch.FloatTensor(X)
            with torch.no_grad():
                recon = model(X_tensor)
                error = torch.mean((X_tensor - recon) ** 2).item()
            proba = min(1.0, error / (threshold * 2))
            return {'fraud_probability': float(proba), 'model': 'Autoencoder', 'reconstruction_error': error}
        except Exception as e:
            print(f"Error in Autoencoder: {e}")
            return None

    def predict_widedeep(self, features):
        if 'widedeep' not in self.models or not PYTORCH_AVAILABLE:
            return None
        try:
            data = self.models['widedeep']
            model = data['model']
            scaler = data['scaler']
            X = scaler.transform([features])
            X_tensor = torch.FloatTensor(X)
            with torch.no_grad():
                proba = model(X_tensor).item()
            return {'fraud_probability': float(proba), 'model': 'Wide & Deep'}
        except Exception as e:
            print(f"Error in Wide & Deep: {e}")
            return None

    def predict_lstm(self, sequence_data):
        if 'lstm' not in self.models or not PYTORCH_AVAILABLE:
            return None
        try:
            model = self.models['lstm']
            seq = np.array(sequence_data)
            # Ensure shape (1, timesteps, features)
            if seq.ndim == 2:
                seq = seq[np.newaxis, :, :]
            X_tensor = torch.FloatTensor(seq)
            with torch.no_grad():
                prob = model(X_tensor).item()
            return {'fraud_probability': float(prob), 'model': 'LSTM'}
        except Exception as e:
            print(f"Error in LSTM: {e}")
            return None

    def predict_isolation_forest(self, features):
        if 'isolation_forest' not in self.models:
            return None
        try:
            model = self.models['isolation_forest']
            # IsolationForest returns 1 for normal, -1 for outlier
            pred = model.predict([features])[0]
            prob = 0.0 if pred == 1 else 1.0
            return {'fraud_probability': float(prob), 'model': 'Isolation Forest'}
        except Exception as e:
            print(f"Error in Isolation Forest: {e}")
            return None

    # ---------------------------------------------------------------------
    # Ensemble prediction
    # ---------------------------------------------------------------------
    def predict_ensemble(self, sequence_data, method='weighted'):
        """Combine predictions from all available models.
        `method` can be 'weighted' (default) or 'voting'.
        """
        # Feature vector for tabular models
        features = self.aggregate_sequence_features(sequence_data)
        predictions = []
        # Tabular models
        lr = self.predict_logistic_regression(features)
        if lr:
            predictions.append((lr['fraud_probability'], 0.20, lr['model']))
        cb = self.predict_catboost(features)
        if cb:
            predictions.append((cb['fraud_probability'], 0.35, cb['model']))
        ae = self.predict_autoencoder(features)
        if ae:
            predictions.append((ae['fraud_probability'], 0.15, ae['model']))
        wd = self.predict_widedeep(features)
        if wd:
            predictions.append((wd['fraud_probability'], 0.15, wd['model']))
        iso = self.predict_isolation_forest(features)
        if iso:
            predictions.append((iso['fraud_probability'], 0.10, iso['model']))
        # Sequence model
        lstm = self.predict_lstm(sequence_data)
        if lstm:
            predictions.append((lstm['fraud_probability'], 0.30, lstm['model']))
        
        # Rule-based override for obvious fraud patterns (e.g. high click count, low time)
        # This catches cases where models might be undertrained or data is synthetic
        heuristic_result = self._mock_predict(sequence_data)
        if heuristic_result['fraud_probability'] > 0.8:
             # If heuristic is very confident it's fraud, force it to be the result
             # This bypasses weak models that might be predicting 0.0
             return heuristic_result

        if not predictions:
            return heuristic_result
        if method == 'weighted':
            total_w = sum(w for _, w, _ in predictions)
            weighted_prob = sum(p * w for p, w, _ in predictions) / total_w
        else:  # simple voting (average)
            weighted_prob = sum(p for p, _, _ in predictions) / len(predictions)
        # Confidence based on agreement
        probs = [p for p, _, _ in predictions]
        std_dev = (sum((p - weighted_prob) ** 2 for p in probs) / len(probs)) ** 0.5
        confidence = 'HIGH' if std_dev < 0.1 else 'MEDIUM' if std_dev < 0.2 else 'LOW'
        # Risk level
        if weighted_prob > 0.7:
            risk = 'HIGH'
        elif weighted_prob > 0.4:
            risk = 'MEDIUM'
        else:
            risk = 'LOW'
        return {
            'is_fraud': bool(weighted_prob > 0.5),
            'fraud_probability': float(weighted_prob),
            'risk_level': risk,
            'confidence': confidence,
            'models_used': [name for _, _, name in predictions],
            'individual_predictions': {name: {'probability': float(p), 'weight': w} for p, w, name in predictions}
        }

    # ---------------------------------------------------------------------
    # Public API
    # ---------------------------------------------------------------------
    def predict(self, sequence_data, use_ensemble=True):
        """Main entry point – either ensemble or best single model."""
        if use_ensemble:
            return self.predict_ensemble(sequence_data)
        # fallback to best available single model
        features = self.aggregate_sequence_features(sequence_data)
        for fn in [self.predict_catboost, self.predict_widedeep, self.predict_logistic_regression,
                   self.predict_autoencoder, self.predict_lstm, self.predict_isolation_forest]:
            res = fn(features if fn.__name__ != 'predict_lstm' else sequence_data)
            if res:
                prob = res['fraud_probability']
                return {
                    'is_fraud': bool(prob > 0.5),
                    'fraud_probability': float(prob),
                    'risk_level': 'HIGH' if prob > 0.7 else 'MEDIUM' if prob > 0.4 else 'LOW',
                    'model_used': res['model']
                }
        return self._mock_predict(sequence_data)

    # ---------------------------------------------------------------------
    # Heuristic fallback
    # ---------------------------------------------------------------------
    def _mock_predict(self, sequence_data):
        """Robust heuristic fallback when ML models are unavailable."""
        if not sequence_data:
            return {'is_fraud': False, 'fraud_probability': 0.1, 'risk_level': 'LOW', 'model_used': 'Heuristic'}
        
        arr = np.array(sequence_data)
        click_count = len(arr)
        
        # Calculate key metrics
        avg_time_diff = np.mean(arr[:, 0]) if arr.shape[1] > 0 else 1.0
        std_time_diff = np.std(arr[:, 0]) if arr.shape[1] > 0 else 0.5
        
        # Base probability
        prob = 0.1
        reasons = []

        # 1. High frequency / Low time difference (Bot-like speed)
        if avg_time_diff < 0.5:
            prob += 0.4
            reasons.append("Abnormally fast clicking speed")
        elif avg_time_diff < 1.0:
            prob += 0.2
            
        # 2. Robotic precision (Low standard deviation in timing)
        if std_time_diff < 0.05:
            prob += 0.3
            reasons.append("Robotic timing precision")
        elif std_time_diff < 0.2:
            prob += 0.15

        # 3. High click volume in short session
        if click_count > 50:
            prob += 0.4
            reasons.append("Excessive click volume")
        elif click_count > 20:
            prob += 0.2

        # Cap probability
        prob = min(0.99, prob)
        
        return {
            'is_fraud': bool(prob > 0.5),
            'fraud_probability': float(prob),
            'risk_level': 'HIGH' if prob > 0.7 else 'MEDIUM' if prob > 0.4 else 'LOW',
            'model_used': 'Heuristic (Enhanced)',
            'reasons': reasons
        }

if __name__ == "__main__":
    detector = ClickFraudDetector()
    # simple demo (can be removed)
    demo_seq = [
        [0.1, 500, 300, 0, 0, 14, 0, 50],
        [0.12, 502, 301, 0, 0, 14, 0, 52],
        [0.11, 501, 299, 0, 0, 14, 0, 51],
        [0.13, 503, 302, 0, 0, 14, 0, 49]
    ]
    print(detector.predict(demo_seq))

