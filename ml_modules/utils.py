import os, joblib, numpy as np

def ensure_model(model_path: str, train_fn):
    """Load a model if it exists, otherwise train it with ``train_fn`` and save.
    ``train_fn`` must return a scikit‑learn compatible model (has ``predict``).
    """
    if os.path.exists(model_path):
        return joblib.load(model_path)
    # Train and persist the model
    model = train_fn()
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(model, model_path)
    return model
