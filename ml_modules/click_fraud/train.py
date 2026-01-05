"""
Click Fraud Detection - Multi-Model Training
Implements: CatBoost, LSTM (Sequential), Autoencoder, Isolation Forest
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
import joblib
import os
import warnings
warnings.filterwarnings('ignore')

# Try importing deep learning libraries
try:
    from catboost import CatBoostClassifier
    CATBOOST_AVAILABLE = True
except ImportError:
    CATBOOST_AVAILABLE = False
    print("⚠ CatBoost not available")

try:
    import torch
    import torch.nn as nn
    from torch.utils.data import Dataset, DataLoader, TensorDataset
    PYTORCH_AVAILABLE = True
except ImportError:
    PYTORCH_AVAILABLE = False
    print("⚠ PyTorch not available")

# --- MODELS ---

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
        # x shape: (batch, seq_len, features)
        lstm_out, _ = self.lstm(x)
        # Take last time step
        last_step = lstm_out[:, -1, :]
        out = self.fc(last_step)
        return torch.sigmoid(out)

class ClickAutoencoder(nn.Module):
    def __init__(self, input_dim=16, encoding_dim=8):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 32),
            nn.ReLU(),
            nn.Linear(32, encoding_dim),
            nn.ReLU()
        )
        self.decoder = nn.Sequential(
            nn.Linear(encoding_dim, 32),
            nn.ReLU(),
            nn.Linear(32, input_dim)
        )
    
    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded

# --- TRAINING FUNCTIONS ---

def train_catboost(X_train, X_test, y_train, y_test):
    print("\n🚀 Training CatBoost...")
    if not CATBOOST_AVAILABLE:
        print("⚠ CatBoost not available")
        return None
    
    model = CatBoostClassifier(iterations=100, depth=6, learning_rate=0.1, verbose=0, random_state=42)
    model.fit(X_train, y_train)
    
    acc = accuracy_score(y_test, model.predict(X_test))
    print(f"✓ CatBoost Accuracy: {acc:.4f}")
    
    os.makedirs('./models', exist_ok=True)
    joblib.dump(model, './models/catboost_model.pkl')
    return acc

def train_isolation_forest(X_train, y_train, X_test, y_test):
    print("\n🌲 Training Isolation Forest...")
    # Train on normal data only usually, or mixed. IF is unsupervised.
    # We'll train on all train data but it assumes outliers are rare.
    # Since our dataset is 30% fraud, we should probably train on normal data only for anomaly detection logic
    # or let it find the 30% outliers.
    
    model = IsolationForest(contamination=0.3, random_state=42)
    model.fit(X_train)
    
    # Predict (1=normal, -1=outlier)
    y_pred_raw = model.predict(X_test)
    y_pred = np.where(y_pred_raw == -1, 1, 0) # Convert to 0=normal, 1=fraud
    
    acc = accuracy_score(y_test, y_pred)
    print(f"✓ Isolation Forest Accuracy: {acc:.4f}")
    
    joblib.dump(model, './models/isolation_forest.pkl')
    return acc

def train_lstm(X_seq, y):
    print("\n🔄 Training LSTM (Sequential)...")
    if not PYTORCH_AVAILABLE:
        print("⚠ PyTorch not available")
        return None
        
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X_seq, y, test_size=0.2, random_state=42)
    
    # Convert to tensors
    X_train_t = torch.FloatTensor(X_train)
    y_train_t = torch.FloatTensor(y_train).unsqueeze(1)
    X_test_t = torch.FloatTensor(X_test)
    y_test_t = torch.FloatTensor(y_test).unsqueeze(1)
    
    model = ClickLSTM(input_dim=X_train.shape[2])
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.BCELoss()
    
    epochs = 10 # Short training for demo
    batch_size = 64
    
    for epoch in range(epochs):
        model.train()
        for i in range(0, len(X_train_t), batch_size):
            batch_X = X_train_t[i:i+batch_size]
            batch_y = y_train_t[i:i+batch_size]
            
            optimizer.zero_grad()
            out = model(batch_X)
            loss = criterion(out, batch_y)
            loss.backward()
            optimizer.step()
            
    model.eval()
    with torch.no_grad():
        y_pred = (model(X_test_t) > 0.5).float().numpy()
        
    acc = accuracy_score(y_test, y_pred)
    print(f"✓ LSTM Accuracy: {acc:.4f}")
    
    torch.save(model.state_dict(), './models/lstm_model.pth')
    return acc

def train_autoencoder(X_train, X_test, y_train, y_test):
    print("\n🔮 Training Autoencoder...")
    if not PYTORCH_AVAILABLE: return None
    
    # Scale
    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)
    
    # Train on normal only
    X_normal = X_train_s[y_train == 0]
    X_normal_t = torch.FloatTensor(X_normal)
    
    model = ClickAutoencoder(input_dim=X_train.shape[1])
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.MSELoss()
    
    for epoch in range(10):
        model.train()
        optimizer.zero_grad()
        out = model(X_normal_t)
        loss = criterion(out, X_normal_t)
        loss.backward()
        optimizer.step()
        
    # Threshold
    model.eval()
    with torch.no_grad():
        rec = model(X_normal_t)
        mse = torch.mean((X_normal_t - rec)**2, dim=1)
        threshold = torch.quantile(mse, 0.95).item()
        
        # Test
        X_test_t = torch.FloatTensor(X_test_s)
        rec_test = model(X_test_t)
        mse_test = torch.mean((X_test_t - rec_test)**2, dim=1).numpy()
        y_pred = (mse_test > threshold).astype(int)
        
    acc = accuracy_score(y_test, y_pred)
    print(f"✓ Autoencoder Accuracy: {acc:.4f}")
    
    torch.save({'model_state': model.state_dict(), 'threshold': threshold, 'scaler': scaler}, './models/autoencoder_model.pth')
    return acc

def main():
    # 1. Load/Generate Data
    if not os.path.exists('click_data.csv') or not os.path.exists('click_X_sequential.npy'):
        print("Generating data...")
        from generate_data import generate_tabular_data, generate_click_data
        # Sequential
        X_seq, y_seq = generate_click_data(2000)
        np.save('click_X_sequential.npy', X_seq)
        np.save('click_y.npy', y_seq)
        # Tabular
        X_tab, y_tab = generate_tabular_data(2000)
        df = pd.DataFrame(X_tab)
        df['is_fraud'] = y_tab
        df.to_csv('click_data.csv', index=False)
    
    # Load Tabular
    df = pd.read_csv('click_data.csv')
    X_tab = df.drop('is_fraud', axis=1).values
    y_tab = df['is_fraud'].values
    X_train, X_test, y_train, y_test = train_test_split(X_tab, y_tab, test_size=0.2, random_state=42)
    
    # Load Sequential
    X_seq = np.load('click_X_sequential.npy')
    y_seq = np.load('click_y.npy')
    
    # Train
    results = {}
    results['CatBoost'] = train_catboost(X_train, X_test, y_train, y_test)
    results['Isolation Forest'] = train_isolation_forest(X_train, y_train, X_test, y_test)
    results['Autoencoder'] = train_autoencoder(X_train, X_test, y_train, y_test)
    results['LSTM'] = train_lstm(X_seq, y_seq)
    
    print("\nSummary:")
    print(results)

if __name__ == "__main__":
    main()
