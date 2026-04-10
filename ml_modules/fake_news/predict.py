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
                # vectorizer may be inside nb_model.pkl or separate
                if 'vectorizer' in model_data:
                    self.vectorizer = model_data['vectorizer']
                self.feature_names = model_data.get('feature_names', [])

            with open(vect_path, "rb") as f:
                self.vectorizer = pickle.load(f)

            print("DJDarkCyber models loaded successfully")
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
        features['exclamation_count'] = text.count('!')
        features['question_count'] = text.count('?')
        features['caps_ratio'] = sum(1 for c in text if c.isupper()) / max(len(text), 1)

        sensational_words = ['shocking', 'unbelievable', "you won't believe", 'secret',
                             'exposed', 'conspiracy']
        features['sensational_count'] = sum(1 for word in sensational_words if word in text.lower())

        words = text.split()
        features['all_caps_words'] = sum(1 for word in words if word.isupper() and len(word) > 2)

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

            # Try combining features
            try:
                from scipy.sparse import hstack
                rule_vector = np.array([list(rule_features.values())])
                combined_vectors = hstack([text_vectors, rule_vector])
                prediction = self.nb_model.predict(combined_vectors)[0]
                proba_input = combined_vectors
            except Exception:
                # Fallback: use only text vector
                prediction = self.nb_model.predict(text_vectors)[0]
                proba_input = text_vectors

            # Get probability scores
            fake_prob = 0.5
            real_prob = 0.5
            if hasattr(self.nb_model, "predict_proba"):
                try:
                    proba = self.nb_model.predict_proba(proba_input)[0]
                    # Determine which class index is "fake"
                    classes = list(self.nb_model.classes_)
                    if 1 in classes:
                        fake_idx = classes.index(1)
                    elif 'FAKE' in classes:
                        fake_idx = classes.index('FAKE')
                    else:
                        fake_idx = 1 if len(classes) > 1 else 0
                    fake_prob = float(proba[fake_idx])
                    real_prob = 1.0 - fake_prob
                except Exception:
                    pass

            # Interpret the raw model prediction
            is_fake_model = False
            if isinstance(prediction, (int, np.integer)):
                is_fake_model = (prediction == 1)
            elif isinstance(prediction, str):
                is_fake_model = ('FAKE' in str(prediction).upper())

            # Source analysis
            source_analysis = self.analyze_source(publisher)

            # Apply rule-based override ONLY for clearly fake articles
            rule_override = self._apply_rule_based_detection(
                title, full_text, source_analysis, is_fake_model, fake_prob
            )

            if rule_override:
                is_fake = rule_override['is_fake']
                result_label = rule_override['label']
                confidence = rule_override['confidence']
                # Update fake probability based on rule override
                fake_prob = max(fake_prob, confidence)
                real_prob = 1.0 - fake_prob
            else:
                is_fake = is_fake_model
                result_label = "FAKE" if is_fake else "REAL"
                confidence = fake_prob if is_fake else real_prob

            # HIGH CREDIBILITY SOURCE OVERRIDE: Never flag high-credibility sources as fake
            # unless model is extremely confident AND multiple rule flags
            if source_analysis['level'] == 'high' and not rule_override:
                if is_fake and fake_prob < 0.85:
                    # Override: high credibility source, not overwhelmingly fake
                    is_fake = False
                    result_label = "REAL"
                    confidence = real_prob

            # Determine risk level
            if is_fake:
                if confidence > 0.8:
                    risk_level = "HIGH"
                elif confidence > 0.6:
                    risk_level = "MEDIUM"
                else:
                    risk_level = "LOW"
            else:
                risk_level = "LOW"
            
            # Calculate credibility score (0-100)
            credibility_score = max(0, 100 - (fake_prob * 100))
            
            # Calculate confidence percentage
            confidence_percent = min(100, max(0, confidence * 100))

            return {
                "prediction": result_label,
                "confidence": f"{confidence:.2%}",
                "confidence_percent": round(confidence_percent, 2),
                "is_fake": bool(is_fake),
                "fake_probability": round(fake_prob, 4),
                "real_probability": round(real_prob, 4),
                "credibility_score": round(credibility_score, 2),
                "risk_level": risk_level,
                "raw_prediction": str(prediction),
                "source_analysis": source_analysis,
                "model_used": "DJDarkCyber Naive Bayes + Rule-Based Enhancement",
                "detailed_analysis": self._generate_detailed_analysis(text, rule_features, source_analysis, health_misinfo_score if 'health_misinfo_score' in locals() else 0)
            }

        except Exception as e:
            return {"error": str(e), "is_fake": False}

    def _apply_rule_based_detection(self, title, content, source_analysis, model_is_fake, model_confidence):
        """Apply rule-based detection to catch obvious fake news"""
        text = (str(title) + " " + str(content)).lower()
        
        # HEALTH MISINFORMATION - Strongest signal
        health_fake_keywords = [
            'cure cancer', 'miracle cure', 'hidden cure', 'secret cure',
            'completely cure', '100% effective', 'guaranteed cure',
            'pharmaceutical companies hide', 'doctors hate this',
            'big pharma doesn\'t want', 'natural cure', 'miracle treatment',
            'cures all', 'heals everything', 'magic pill'
        ]
        
        # Check for health misinformation with unrealistic claims
        health_misinfo_score = 0
        health_fake_found = []
        for kw in health_fake_keywords:
            if kw in text:
                health_misinfo_score += 30
                health_fake_found.append(kw)
        
        # Extraordinary medical claims
        import re
        if ('cancer' in text and 'cure' in text):
            health_misinfo_score += 40
            health_fake_found.append('cancer cure claim')
        
        if re.search(r'\d+\s*(liters|hours|days|weeks)', text):
            if 'cure' in text or 'heal' in text or 'treat' in text:
                health_misinfo_score += 25
                health_fake_found.append('specific timeframe claim')
        
        # If health misinformation score is high, immediately flag as fake
        if health_misinfo_score >= 50:
            confidence = min(0.95, 0.5 + (health_misinfo_score / 200))
            return {
                'is_fake': True, 
                'label': 'FAKE', 
                'confidence': confidence,
                'reason': f'Health misinformation detected: {", ".join(health_fake_found[:3])}'
            }

        conspiracy_keywords = [
            'microchip', 'implant', 'tracking device', 'mind control', 'new world order',
            'illuminati', 'deep state', 'secret government', 'cover-up',
            "they don't want you to know", 'wake up', 'sheeple', 'mainstream media lies',
            'fake news media', 'censored', 'big pharma', 'chemtrails', 'flat earth',
            'lizard people', 'crisis actors', 'hidden', 'secret'
        ]

        sensational_phrases = [
            'shocking truth', "what they don't tell you", 'doctors hate this',
            'this one trick', "you won't believe", 'viral post claims',
            'unnamed sources', 'anonymous insider', 'shocking', 'unbelievable',
            'exposed', 'conspiracy'
        ]

        lack_of_evidence = [
            'no official', 'no credible', 'unverified', 'unconfirmed',
            'without evidence', 'no proof', 'no documentation', 'no statement'
        ]

        conspiracy_count = sum(1 for kw in conspiracy_keywords if kw in text)
        sensational_count = sum(1 for ph in sensational_phrases if ph in text)
        evidence_lack_count = sum(1 for ph in lack_of_evidence if ph in text)

        # Rule 1: Low credibility + conspiracy + no evidence
        if (source_analysis['level'] == 'low' and
                conspiracy_count >= 2 and
                evidence_lack_count >= 1):
            return {'is_fake': True, 'label': 'FAKE', 'confidence': 0.85}

        # Rule 2: Multiple strong conspiracy keywords (3+)
        if conspiracy_count >= 3:
            return {'is_fake': True, 'label': 'FAKE', 'confidence': 0.80}

        # Rule 3: Sensational + low credibility (2 sensational phrases required)
        if source_analysis['level'] == 'low' and sensational_count >= 2:
            return {'is_fake': True, 'label': 'FAKE', 'confidence': 0.75}

        # Rule 4: Model says real but strong indicators suggest fake
        if (not model_is_fake and
                source_analysis['level'] == 'low' and
                conspiracy_count >= 2 and sensational_count >= 1):
            return {'is_fake': True, 'label': 'FAKE', 'confidence': 0.70}

        # No rule triggered
        return None
    
    def _generate_detailed_analysis(self, text, rule_features, source_analysis, health_score):
        """Generate detailed analysis explanation"""
        analysis_points = []
        
        # Health misinformation check
        if health_score >= 50:
            analysis_points.append(f"🚨 Health misinformation detected (score: {health_score})")
            analysis_points.append("⚠️ Contains unrealistic medical claims or cure promises")
        
        # Source credibility
        if source_analysis['level'] == 'low':
            analysis_points.append(f"📉 Low credibility source: {source_analysis['label']}")
        elif source_analysis['level'] == 'high':
            analysis_points.append(f"✅ High credibility source: {source_analysis['label']}")
        
        # Sensational language
        if rule_features.get('sensational_count', 0) > 0:
            analysis_points.append(f"⚡ Contains {rule_features['sensational_count']} sensational phrase(s)")
        
        # Exclamation marks
        if rule_features.get('exclamation_count', 0) > 3:
            analysis_points.append(f"❗ Excessive exclamation marks ({rule_features['exclamation_count']})")
        
        # Capitalization
        if rule_features.get('caps_ratio', 0) > 0.3:
            analysis_points.append(f"🔠 High capitalization ratio ({rule_features['caps_ratio']:.0%})")
        
        if not analysis_points:
            analysis_points.append("✅ No obvious fake news indicators detected")
            analysis_points.append("📊 Article appears to follow normal news writing patterns")
        
        return " | ".join(analysis_points)


# Backward compatibility alias
class FakeNewsDetector(DJDarkCyberFakeNewsDetector):
    def __init__(self, model_dir="./models"):
        super().__init__(model_dir)


def predict(text):
    """Backward compatibility wrapper"""
    detector = FakeNewsDetector()
    return detector.analyze_article("", text)
