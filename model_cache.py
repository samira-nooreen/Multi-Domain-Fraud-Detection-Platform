"""
ML Model Cache - Lazy Loading for Production
Loads models only when needed to save memory
"""
import joblib
import os

# Model cache dictionary
_model_cache = {}

def get_model(model_path):
    """
    Lazy load ML model - loads only once and caches
    """
    if model_path not in _model_cache:
        if os.path.exists(model_path):
            _model_cache[model_path] = joblib.load(model_path)
        else:
            raise FileNotFoundError(f"Model not found: {model_path}")
    return _model_cache[model_path]

def clear_model_cache():
    """Clear all cached models (for memory management)"""
    _model_cache.clear()

def get_cache_size():
    """Get number of cached models"""
    return len(_model_cache)
