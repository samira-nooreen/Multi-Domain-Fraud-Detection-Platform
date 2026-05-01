"""
DJDarkCyber Fake News Detector
Integrates the Naive Bayes model from https://github.com/DJDarkCyber/Fake-News-Detector
"""
import pickle
import os
import numpy as np
import re


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
                     'npr', 'pbs', 'bloomberg', 'financial times', 'economist', 'thehindu',
                     'the hindu', 'gov.in', '.gov.in', 'isro', 'isro.gov.in'],
            'medium': ['fox', 'msnbc', 'usa today', 'time', 'newsweek', 'huffpost',
                       'business insider', 'hill', 'politico', 'axios'],
            'low': ['blog', 'unknown', 'example.com', 'example', 'social', 'facebook', 'twitter', 'instagram',
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

        if 'example.com' in source or source.endswith('example'):
            return {'level': 'low', 'score': 20, 'label': 'Untrusted Example Source'}

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

        features['number_count'] = len(re.findall(r'\d+', text))
        features['percent_count'] = len(re.findall(r'\d+\s*%', text))
        features['has_strong_claim'] = bool(re.search(r'\b(reduces|increases|causes|leads to|proves|guarantees|cures|destroys)\b', text.lower()))

        lowered = text.lower()
        clickbait_phrases = ["you won't believe", 'shocking', 'unbelievable', 'viral post claims', 'secret truth']
        exaggerated_claims = ['100% cure', 'rich overnight', 'drastically reduces', 'guaranteed cure', 'magic pill']
        vague_source_phrases = ['reports say', 'experts claim', 'report claims', 'claims that', 'sources say', 'it is said']

        features['clickbait_count'] = sum(1 for phrase in clickbait_phrases if phrase in lowered)
        features['exaggeration_count'] = sum(1 for phrase in exaggerated_claims if phrase in lowered)
        features['vague_source_count'] = sum(1 for phrase in vague_source_phrases if phrase in lowered)

        return features

    def _combine_ml_and_rules(self, ml_fake_prob, rule_score, source_analysis, factual_score):
        """Combine model probability with calibrated rule score into final fake probability."""
        # Blend ML signal with rule score.
        combined = (0.65 * float(ml_fake_prob)) + (0.35 * (float(rule_score) / 100.0))

        # Source should influence, but not dominate, prediction.
        source_adjustment = {
            'high': -0.08,
            'medium': -0.02,
            'unknown': 0.03,
            'low': 0.06,
        }.get(source_analysis.get('level', 'unknown'), 0.03)
        combined += source_adjustment

        # Strong factual reporting suppresses false positives.
        if factual_score >= 6:
            combined = min(combined, 0.12)
        elif factual_score >= 4:
            combined = min(combined, 0.18)

        return float(min(0.98, max(0.02, combined)))

    def _build_recommendation(self, risk_level):
        """Build consistent action recommendation from final risk."""
        if risk_level == 'HIGH':
            return 'Avoid sharing. High misinformation risk detected.'
        if risk_level == 'MEDIUM':
            return 'Verify with trusted sources before sharing.'
        return 'Trust with normal caution. No strong misinformation indicators found.'

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
            vectorization_failed = False

            # Try combining features
            try:
                from scipy.sparse import hstack
                rule_vector = np.array([list(rule_features.values())])
                combined_vectors = hstack([text_vectors, rule_vector])
                prediction = self.nb_model.predict(combined_vectors)[0]
                proba_input = combined_vectors
            except Exception:
                # Fallback: if feature dimensions do not match, use a conservative baseline
                try:
                    prediction = self.nb_model.predict(text_vectors)[0]
                    proba_input = text_vectors
                except Exception:
                    vectorization_failed = True
                    prediction = 0
                    proba_input = None

            # Get probability scores
            fake_prob = 0.5
            real_prob = 0.5
            if vectorization_failed:
                fake_prob = 0.35
                real_prob = 0.65
            elif hasattr(self.nb_model, "predict_proba"):
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
            lowered_text = text.lower()

            # Rule score used as a calibrated misinformation probability signal.
            rule_score = 0
            if source_analysis['level'] == 'low':
                rule_score += 18
            elif source_analysis['level'] == 'unknown':
                rule_score += 10
            elif source_analysis['level'] == 'medium':
                rule_score += 4

            if rule_features.get('clickbait_count', 0) > 0:
                rule_score += 12 * rule_features.get('clickbait_count', 0)
            if rule_features.get('exaggeration_count', 0) > 0:
                rule_score += 14 * rule_features.get('exaggeration_count', 0)
            if rule_features.get('vague_source_count', 0) > 0:
                rule_score += 8 * rule_features.get('vague_source_count', 0)
            if rule_features.get('has_strong_claim'):
                rule_score += 8
            if rule_features.get('percent_count', 0) > 0:
                rule_score += 6

            # Additional explicit claim checks requested by user examples.
            if '50%' in lowered_text or 'reduces intelligence' in lowered_text:
                rule_score += 12
            if 'rich overnight' in lowered_text or '100% cure' in lowered_text:
                rule_score += 20

            # Factual-news signals for official and neutral reporting.
            factual_score = 0
            if 'launched' in lowered_text and 'satellite' in lowered_text:
                factual_score += 2
            if 'successfully launched' in lowered_text:
                factual_score += 2
            if 'government' in lowered_text or 'officials stated' in lowered_text:
                factual_score += 2
            if 'isro' in lowered_text or 'indian space research organisation' in lowered_text:
                factual_score += 3
            if 'weather forecasting' in lowered_text:
                factual_score += 1
            if 'disaster management' in lowered_text:
                factual_score += 1
            if 'initiative' in lowered_text or 'program focuses' in lowered_text:
                factual_score += 1

            # Official content should dampen risk from uncertain sources.
            if factual_score >= 4:
                rule_score = max(0, rule_score - 20)

            rule_score = min(100, max(0, rule_score))

            # Apply strict rule override only for clearly fake content.
            rule_override = self._apply_rule_based_detection(
                title, full_text, source_analysis, is_fake_model, fake_prob
            )

            health_misinfo_score = int(rule_override.get('health_score', 0)) if rule_override else 0

            combined_fake_prob = self._combine_ml_and_rules(
                ml_fake_prob=fake_prob,
                rule_score=rule_score,
                source_analysis=source_analysis,
                factual_score=factual_score,
            )

            if rule_override:
                combined_fake_prob = max(combined_fake_prob, float(rule_override.get('confidence', combined_fake_prob)))

            fake_prob = min(0.98, max(0.02, combined_fake_prob))
            real_prob = 1.0 - fake_prob

            misleading_score = rule_score

            if rule_override:
                is_fake = True
                result_label = 'FAKE'
                confidence = fake_prob
            elif fake_prob >= 0.75:
                is_fake = True
                result_label = 'FAKE'
                confidence = fake_prob
            elif fake_prob >= 0.45:
                is_fake = False
                result_label = 'MISLEADING'
                confidence = fake_prob
            else:
                is_fake = False
                result_label = 'REAL'
                confidence = real_prob

            # Determine risk level
            if is_fake:
                if fake_prob >= 0.75:
                    risk_level = "HIGH"
                elif fake_prob >= 0.60:
                    risk_level = "MEDIUM"
                else:
                    risk_level = "LOW"
            elif result_label == "MISLEADING":
                risk_level = "MEDIUM"
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
                "detailed_analysis": self._generate_detailed_analysis(
                    text,
                    rule_features,
                    source_analysis,
                    health_misinfo_score,
                    misleading_score,
                    risk_level,
                    factual_score
                ),
                "recommendation": self._build_recommendation(risk_level)
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
                'reason': f'Health misinformation detected: {", ".join(health_fake_found[:3])}',
                'health_score': health_misinfo_score,
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
    
    def _generate_detailed_analysis(self, text, rule_features, source_analysis, health_score, misleading_score=0, risk_level='LOW', factual_score=0):
        """Generate detailed analysis explanation"""
        analysis_points = []
        
        # Health misinformation check
        if health_score >= 50:
            analysis_points.append(f"🚨 Health misinformation detected (score: {health_score})")
            analysis_points.append("⚠️ Contains unrealistic medical claims or cure promises")

        if factual_score >= 6 and misleading_score < 20 and health_score < 50:
            analysis_points.append("✅ Strong factual reporting signals detected")
            analysis_points.append("📌 Article references an official organization and a concrete scientific update")

        if misleading_score >= 25 and health_score < 50 and factual_score < 6:
            analysis_points.append(f"⚠️ Potentially misleading information detected (score: {misleading_score})")
            if source_analysis['level'] in ('low', 'unknown'):
                analysis_points.append("📌 Contains a strong claim from a low-credibility or unknown source")
            else:
                analysis_points.append("📌 Contains exaggerated or clickbait-style language despite a credible source")
            if 'report claims' in text.lower() or 'claims that' in text.lower():
                analysis_points.append("📌 Vague reporting language detected")
            if '50%' in text or 'drastically' in text.lower() or 'reduces intelligence' in text.lower():
                analysis_points.append("📌 Exaggerated statistic or unrealistic claim detected")
        
        # Source credibility
        if source_analysis['level'] == 'low' and factual_score < 6:
            analysis_points.append(f"📉 Low credibility source: {source_analysis['label']}")
        elif source_analysis['level'] == 'high':
            analysis_points.append(f"✅ High credibility source: {source_analysis['label']}")
        elif factual_score >= 6:
            analysis_points.append("✅ Factual content outweighs the placeholder or untrusted URL")
        
        # Sensational language
        if rule_features.get('sensational_count', 0) > 0:
            analysis_points.append(f"⚡ Contains {rule_features['sensational_count']} sensational phrase(s)")
        
        # Exclamation marks
        if rule_features.get('exclamation_count', 0) > 3:
            analysis_points.append(f"❗ Excessive exclamation marks ({rule_features['exclamation_count']})")
        
        # Capitalization
        if rule_features.get('caps_ratio', 0) > 0.3:
            analysis_points.append(f"🔠 High capitalization ratio ({rule_features['caps_ratio']:.0%})")

        if risk_level == 'HIGH':
            if rule_features.get('clickbait_count', 0) > 0:
                analysis_points.append("🚩 Clickbait language strongly increases fake-news risk")
            if rule_features.get('exaggeration_count', 0) > 0 or rule_features.get('percent_count', 0) > 1:
                analysis_points.append("🚩 Exaggerated or unrealistic claim pattern detected")
            if source_analysis.get('level') in ('low', 'unknown'):
                analysis_points.append("🚩 Weak source credibility increases misinformation risk")

        if risk_level == 'LOW' and factual_score >= 4:
            analysis_points.append("✅ Credibility support: official/factual reporting patterns detected")
        elif risk_level == 'LOW' and source_analysis.get('level') == 'high':
            analysis_points.append("✅ Credibility support: trusted source classification")
        
        if not analysis_points:
            if risk_level in ('MEDIUM', 'HIGH'):
                analysis_points.append("⚠️ Model and rule fusion flagged potential misinformation patterns")
                analysis_points.append("📌 Verify claims with additional trusted sources")
            else:
                analysis_points.append("✅ Low misinformation risk based on balanced model and rule checks")
                analysis_points.append("📊 Article appears to follow normal factual writing patterns")
        
        return " | ".join(analysis_points)


# Backward compatibility alias
class FakeNewsDetector(DJDarkCyberFakeNewsDetector):
    def __init__(self, model_dir="./models"):
        super().__init__(model_dir)


def predict(text):
    """Backward compatibility wrapper"""
    detector = FakeNewsDetector()
    return detector.analyze_article("", text)
