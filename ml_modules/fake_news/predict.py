"""
DJDarkCyber Fake News Detector
Integrates the Naive Bayes model from https://github.com/DJDarkCyber/Fake-News-Detector
"""
import pickle
import os
import numpy as np


class DJDarkCyberFakeNewsDetector:
    def __init__(self, model_dir=None):
        if model_dir is None:
            # Look for models in the same directory as this file
            import os
            model_dir = os.path.join(os.path.dirname(__file__), 'models')
        self.model_dir = model_dir
        self.nb_model = None
        self.vectorizer = None
        self.load_models()
        
        # Source credibility database
        self.source_credibility = {
            'high': ['reuters', 'associated press', 'ap', 'bbc', 'cnn', 'nbc', 'abc', 'cbs', 
                     'new york times', 'washington post', 'wall street journal', 'guardian',
                     'npr', 'pbs', 'bloomberg', 'financial times', 'economist'],
            'medium': ['fox', 'msnbc', 'usa today', 'time', 'newsweek', 'huffpost', 
                       'business insider', 'hill', 'politico', 'axios'],
            'low': ['blog', 'unknown', 'social', 'facebook', 'twitter', 'instagram',
                    'tiktok', 'reddit', 'forum', 'personal']
        }

    def load_models(self):
        """Load the Naive Bayes model and vectorizer"""
        nb_path = os.path.join(self.model_dir, "nb_model.pkl")
        vect_path = os.path.join(self.model_dir, "vectorizer_model.pkl")
        
        if not os.path.exists(nb_path) or not os.path.exists(vect_path):
            raise FileNotFoundError(f"Models not found in {self.model_dir}")

        try:
            with open(nb_path, "rb") as f:
                model_data = pickle.load(f)
                self.nb_model = model_data['classifier']
                self.vectorizer = model_data['vectorizer']
                self.feature_names = model_data.get('feature_names', [])
                
            with open(vect_path, "rb") as f:
                self.vectorizer = pickle.load(f)
            
            print("✅ DJDarkCyber models loaded successfully")
        except Exception as e:
            raise RuntimeError(f"Failed to load models: {str(e)}")

    def analyze_source(self, source):
        """Analyze the credibility of a news source"""
        if not source:
            return {'level': 'unknown', 'score': 50, 'label': 'Unknown Source'}
            
        source = source.lower().strip()
        
        for s in self.source_credibility['high']:
            if s in source:
                return {'level': 'high', 'score': 85, 'label': 'High Credibility'}
                
        for s in self.source_credibility['medium']:
            if s in source:
                return {'level': 'medium', 'score': 65, 'label': 'Medium Credibility'}
                
        for s in self.source_credibility['low']:
            if s in source:
                return {'level': 'low', 'score': 30, 'label': 'Low Credibility'}
                
        return {'level': 'unknown', 'score': 50, 'label': 'Unknown Source'}

    def _extract_rule_features(self, text):
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
        import re
        features['number_count'] = len(re.findall(r'\d+', text))
        
        return features
        
    def analyze_article(self, title, full_text, publisher=None, timestamp=None):
        """Analyze a news article for fake news detection with hybrid approach"""
        text = (str(title) + " " + str(full_text)).strip()
        
        if not text:
            return {"error": "No text provided"}
            
        try:
            # Extract rule-based features
            rule_features = self._extract_rule_features(text)
            
            # Vectorize the text
            text_vectors = self.vectorizer.transform([text])
            
            # Combine features
            from scipy.sparse import hstack
            import numpy as np
            rule_vector = np.array([list(rule_features.values())])
            combined_vectors = hstack([text_vectors, rule_vector])
            
            # Predict using Naive Bayes + Rule-based
            prediction = self.nb_model.predict(combined_vectors)[0]
            
            # Get probability scores
            confidence = 0.0
            if hasattr(self.nb_model, "predict_proba"):
                proba = self.nb_model.predict_proba(combined_vectors)[0]
                confidence = float(max(proba))
            
            # Interpret the prediction
            # The model typically outputs: 1 = Fake, 0 = Real
            is_fake = False
            result_label = str(prediction)
            
            if isinstance(prediction, (int, np.integer)):
                if prediction == 1:
                    is_fake = True
                    result_label = "FAKE"
                else:
                    is_fake = False
                    result_label = "REAL"
            elif isinstance(prediction, str):
                result_label = prediction.upper()
                if "FAKE" in result_label:
                    is_fake = True
            
            # Analyze source credibility
            source_analysis = self.analyze_source(publisher)
            
            # HYBRID ENHANCEMENT: Apply rule-based detection
            rule_based_result = self._apply_rule_based_detection(
                title, full_text, source_analysis, is_fake, confidence
            )
            
            if rule_based_result:
                is_fake = rule_based_result['is_fake']
                result_label = rule_based_result['label']
                confidence = rule_based_result['confidence']
            
            return {
                "prediction": result_label,
                "confidence": f"{confidence:.2%}",
                "is_fake": is_fake,
                "raw_prediction": str(prediction),
                "source_analysis": source_analysis,
                "model_used": "DJDarkCyber Naive Bayes + Rule-Based Enhancement"
            }
            
        except Exception as e:
            return {"error": str(e)}

    def _apply_rule_based_detection(self, title, content, source_analysis, model_is_fake, model_confidence):
        """Apply rule-based detection to catch obvious fake news"""
        text = (title + " " + content).lower()
        
        # Fake news indicators
        conspiracy_keywords = [
            'microchip', 'implant', 'tracking device', 'mind control', 'new world order',
            'illuminati', 'deep state', 'secret government', 'cover-up', 'they don\'t want you to know',
            'wake up', 'sheeple', 'mainstream media lies', 'fake news media', 'censored',
            'big pharma', 'chemtrails', 'flat earth', 'lizard people', 'crisis actors'
        ]
        
        sensational_phrases = [
            'shocking truth', 'what they don\'t tell you', 'doctors hate this',
            'this one trick', 'you won\'t believe', 'breaking:', 'urgent:',
            'viral post claims', 'unnamed sources', 'anonymous insider'
        ]
        
        lack_of_evidence = [
            'no official', 'no credible', 'unverified', 'unconfirmed',
            'without evidence', 'no proof', 'no documentation', 'no statement'
        ]
        
        # Count indicators
        conspiracy_count = sum(1 for keyword in conspiracy_keywords if keyword in text)
        sensational_count = sum(1 for phrase in sensational_phrases if phrase in text)
        evidence_lack_count = sum(1 for phrase in lack_of_evidence if phrase in text)
        
        # Rule 1: Low credibility source + conspiracy keywords + lack of evidence
        if (source_analysis['level'] == 'low' and 
            conspiracy_count >= 1 and 
            evidence_lack_count >= 1):
            return {
                'is_fake': True,
                'label': 'FAKE',
                'confidence': 0.85  # High confidence in fake detection
            }
        
        # Rule 2: Multiple conspiracy keywords regardless of source
        if conspiracy_count >= 3:
            return {
                'is_fake': True,
                'label': 'FAKE',
                'confidence': 0.80
            }
        
        # Rule 3: Sensational language + low credibility source
        if source_analysis['level'] == 'low' and sensational_count >= 2:
            return {
                'is_fake': True,
                'label': 'FAKE',
                'confidence': 0.75
            }
        
        # Rule 4: Model says real but source is low and has conspiracy indicators
        if (not model_is_fake and 
            source_analysis['level'] == 'low' and 
            (conspiracy_count >= 1 or sensational_count >= 2)):
            return {
                'is_fake': True,
                'label': 'FAKE',
                'confidence': 0.70
            }
        
        # No rule triggered, use model prediction
        return None


# Create alias for backward compatibility
class FakeNewsDetector(DJDarkCyberFakeNewsDetector):
    def __init__(self, model_dir="./models"):
        super().__init__(model_dir)


def predict(text):
    """Backward compatibility wrapper"""
    detector = FakeNewsDetector()
    return detector.analyze_article("", text)