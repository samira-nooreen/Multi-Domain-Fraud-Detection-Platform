"""
Document Forgery - Simple Scikit‑Learn Training

This script provides a lightweight alternative to the TensorFlow CNN model.
It extracts very basic image features (flattened pixel values) and trains a
RandomForest classifier. The model is saved as ``forgery_model.pkl`` and can be
used by ``ml_modules/document_forgery/predict.py`` as a fallback when the
TensorFlow model is unavailable.
"""

import os
import numpy as np
from PIL import Image
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib

DATA_DIR = "doc_data"
MODEL_PATH = "forgery_model.pkl"

def load_images_and_labels():
    """Load images from ``doc_data/genuine`` and ``doc_data/forged``.
    Returns:
        X (np.ndarray): Flattened image arrays (n_samples, n_features)
        y (np.ndarray): Labels (0 = genuine, 1 = forged)
    """
    X = []
    y = []
    for label, subdir in [(0, "genuine"), (1, "forged")]:
        folder = os.path.join(DATA_DIR, subdir)
        if not os.path.isdir(folder):
            continue
        for fname in os.listdir(folder):
            if not fname.lower().endswith((".png", ".jpg", ".jpeg")):
                continue
            path = os.path.join(folder, fname)
            img = Image.open(path).convert("RGB").resize((64, 64))
            arr = np.asarray(img).astype(np.float32) / 255.0
            X.append(arr.flatten())
            y.append(label)
    return np.array(X), np.array(y)

def train():
    if not os.path.isdir(DATA_DIR):
        raise RuntimeError(f"Data directory '{DATA_DIR}' not found. Run the synthetic data generator first.")

    X, y = load_images_and_labels()
    if X.shape[0] == 0:
        raise RuntimeError("No images found in the data directory.")

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    clf = RandomForestClassifier(n_estimators=150, max_depth=12, random_state=42, n_jobs=-1)
    clf.fit(X_train, y_train)

    # Evaluation
    y_pred = clf.predict(X_val)
    acc = accuracy_score(y_val, y_pred)
    print(f"Validation Accuracy: {acc:.4f}")
    print(classification_report(y_val, y_pred, target_names=["genuine", "forged"]))

    # Save model
    joblib.dump(clf, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    train()
