"""
Click Fraud Detection - LSTM Training
Algorithm: Long Short-Term Memory (LSTM)
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
import joblib
import os
import warnings
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

warnings.filterwarnings('ignore')

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

# --- TRAINING FUNCTIONS ---

def train_lstm(X_seq, y):
    print("\nTraining LSTM for Click Fraud Detection...")
        
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
    
    epochs = 20
    batch_size = 64
    
    for epoch in range(epochs):
        model.train()
        total_loss = 0
        for i in range(0, len(X_train_t), batch_size):
            batch_X = X_train_t[i:i+batch_size]
            batch_y = y_train_t[i:i+batch_size]
            
            optimizer.zero_grad()
            out = model(batch_X)
            loss = criterion(out, batch_y)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
            
        if (epoch+1) % 5 == 0:
            print(f"Epoch {epoch+1}/{epochs}, Loss: {total_loss:.4f}")
            
    model.eval()
    with torch.no_grad():
        y_prob = model(X_test_t)
        y_pred = (y_prob > 0.5).float().numpy()
        y_prob = y_prob.numpy()
        
    acc = accuracy_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_prob)
    
    print(f"\nModel Evaluation:")
    print(f"Accuracy: {acc:.4f}")
    print(f"ROC-AUC: {auc:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Legitimate', 'Fraud']))
    
    # Save model
    os.makedirs('./models', exist_ok=True)
    torch.save(model.state_dict(), './models/lstm_model.pth')
    print("LSTM model saved to ./models/lstm_model.pth")
    return acc

def main():
    # 1. Load/Generate Data
    if not os.path.exists('click_X_sequential.npy') or not os.path.exists('click_y.npy'):
        print("Generating data...")
        from generate_data import generate_click_data
        X_seq, y_seq = generate_click_data(2000)
        np.save('click_X_sequential.npy', X_seq)
        np.save('click_y.npy', y_seq)
    
    # Load Sequential
    X_seq = np.load('click_X_sequential.npy')
    y_seq = np.load('click_y.npy')
    
    print(f"Loaded data with shape: {X_seq.shape}")
    
    # Train
    train_lstm(X_seq, y_seq)
    
    print("\nTraining complete!")

if __name__ == "__main__":
    main()
