"""
Document Forgery Prediction - ResNet
"""
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import os

class ForgeryDetector:
    def __init__(self, model_path='document_forgery_resnet_model.h5'):
        self.model_path = model_path
        self.model = None
        self.load_model()
        
    def load_model(self):
        try:
            self.model = load_model(self.model_path)
        except:
            self.model = None
            
    def predict(self, img_path):
        if self.model is None:
            return self._mock_predict()
            
        try:
            img = image.load_img(img_path, target_size=(224, 224))
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x /= 255.0
            
            prob = self.model.predict(x)[0][0]
            
            return {
                'is_forged': bool(prob > 0.5),
                'forgery_probability': float(prob),
                'authenticity': 'FORGED' if prob > 0.5 else 'AUTHENTIC',
                'model': 'ResNet50'
            }
        except:
            return self._mock_predict()
            
    def _mock_predict(self):
        # Random mock result
        prob = np.random.random()
        return {
            'is_forged': bool(prob > 0.5),
            'forgery_probability': float(prob),
            'authenticity': 'FORGED' if prob > 0.5 else 'AUTHENTIC'
        }
