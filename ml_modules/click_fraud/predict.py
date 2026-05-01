# Click Fraud Prediction - LSTM / Heuristic
# Algorithm: LSTM (primary) with heuristic fallback

import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')


class ClickFraudDetector:
    def __init__(self, model_dir='./models'):
        self.model_dir = model_dir
        self.lstm_model = None
        self.use_torch = False
        self._load_lstm()

    def _load_lstm(self):
        """Try to load PyTorch LSTM model."""
        lstm_path = os.path.join(self.model_dir, 'lstm_model.pth')
        if not os.path.exists(lstm_path):
            return

        try:
            import torch
            import torch.nn as nn

            class ClickLSTM(nn.Module):
                def __init__(self, input_dim=9, hidden_dim=64, num_layers=2):
                    super().__init__()
                    self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers,
                                        batch_first=True, dropout=0.2)
                    self.fc = nn.Sequential(
                        nn.Linear(hidden_dim, 32),
                        nn.ReLU(),
                        nn.Linear(32, 1)
                    )
                def forward(self, x):
                    out, _ = self.lstm(x)
                    return torch.sigmoid(self.fc(out[:, -1, :]))

            m = ClickLSTM(input_dim=9)
            m.load_state_dict(torch.load(lstm_path, map_location='cpu'))
            m.eval()
            self.lstm_model = m
            self.use_torch = True
            print("  Click LSTM model loaded")
        except Exception as e:
            print(f"  LSTM load failed: {e}")

    def predict(self, sequence_data):
        """
        Predict click fraud.

        sequence_data: list of lists.
          Each inner list represents one click event with features:
          [time_diff, click_x, click_y, ip_change, user_agent_change,
           hour_of_day, is_weekend, click_velocity, referrer_entropy]

        Returns dict with fraud probability and risk level.
        """
        if not sequence_data:
            return self._format_result(0.05, 'Heuristic')

        arr = np.array(sequence_data, dtype=np.float64)
        if arr.ndim == 1:
            arr = arr.reshape(1, -1)

        # Try LSTM first
        if self.use_torch and self.lstm_model is not None:
            try:
                import torch
                seq = arr.astype(np.float32)
                # Ensure 9 features
                if seq.shape[1] < 9:
                    pad = np.zeros((seq.shape[0], 9 - seq.shape[1]))
                    seq = np.hstack([seq, pad])
                elif seq.shape[1] > 9:
                    seq = seq[:, :9]
                X = torch.FloatTensor(seq).unsqueeze(0)
                with torch.no_grad():
                    prob = float(self.lstm_model(X).item())
                return self._format_result(prob, 'LSTM')
            except Exception as e:
                print(f"  LSTM predict failed: {e}")

        # Heuristic analysis (reliable, domain-driven)
        return self._heuristic_predict(arr)

    def _heuristic_predict(self, arr):
        """
        Rule-based heuristic click fraud detection.
        Based on the feature definitions from generate_data.py:
          col0: time_diff     (human: avg ~2.5s, bot: avg ~0.15s)
          col1: click_x
          col2: click_y
          col3: ip_change
          col4: user_agent_change
          col5: hour_of_day
          col6: is_weekend
          col7: click_velocity (human: 2-15/min, bot: 30-60/min)
          col8: referrer_entropy (human: 1.5-3.0, bot: 0-0.5)
        """
        n_clicks = arr.shape[0]
        score = 0.0
        indicators = []

        # --- TIME DIFF (col 0) ---
        if arr.shape[1] > 0:
            time_diffs = arr[:, 0]
            avg_time = float(np.mean(time_diffs))
            std_time = float(np.std(time_diffs))

            if avg_time < 0.2:
                score += 0.50
                indicators.append(f"Extremely fast clicks (avg {avg_time:.2f}s)")
            elif avg_time < 0.5:
                score += 0.35
                indicators.append(f"Very fast clicks (avg {avg_time:.2f}s)")
            elif avg_time < 1.0:
                score += 0.15
                indicators.append(f"Fast clicks (avg {avg_time:.2f}s)")
            elif avg_time < 2.0:
                score += 0.08
                indicators.append(f"Moderate click speed")
            elif avg_time < 3.0:
                score += 0.03

            # Very consistent timing = bot
            if avg_time > 0 and std_time / (avg_time + 1e-9) < 0.1:
                score += 0.25
                indicators.append("Unnaturally consistent click timing")
            elif avg_time > 0 and std_time / (avg_time + 1e-9) < 0.2:
                score += 0.15
                indicators.append("Suspiciously consistent timing")
            elif avg_time > 0 and std_time / (avg_time + 1e-9) < 0.3:
                score += 0.05

        # --- CLICK POSITION VARIANCE (cols 1,2) ---
        # Suspicious patterns have concentrated clicks
        if arr.shape[1] > 2:
            x_std = float(np.std(arr[:, 1]))
            y_std = float(np.std(arr[:, 2]))
            if x_std < 20 and y_std < 20:
                score += 0.25
                indicators.append("Clicks concentrated in tiny area (bot pattern)")
            elif x_std < 50 and y_std < 50:
                score += 0.12
                indicators.append("Limited click position variation (suspicious)")
            elif x_std < 100 and y_std < 100:
                score += 0.08
                indicators.append("Moderate click position variation")

        # --- CLICK VELOCITY (col 7) ---
        if arr.shape[1] > 7:
            avg_velocity = float(np.mean(arr[:, 7]))
            if avg_velocity > 60:
                score += 0.30
                indicators.append(f"Extremely high click velocity ({avg_velocity:.0f}/min)")
            elif avg_velocity > 40:
                score += 0.25
                indicators.append(f"Very high click velocity ({avg_velocity:.0f}/min)")
            elif avg_velocity > 20:
                score += 0.10
                indicators.append(f"High click velocity ({avg_velocity:.0f}/min)")
            elif avg_velocity > 10:
                score += 0.03

        # --- REFERRER ENTROPY (col 8) ---
        # This is a KEY pattern indicator - suspicious patterns have low entropy
        if arr.shape[1] > 8:
            avg_entropy = float(np.mean(arr[:, 8]))
            if avg_entropy < 0.3:
                score += 0.20
                indicators.append("Very low referrer entropy (bot pattern)")
            elif avg_entropy < 0.7:
                score += 0.15
                indicators.append("Low referrer entropy (suspicious pattern)")
            elif avg_entropy < 1.0:
                score += 0.10
                indicators.append("Below-average referrer entropy")
            elif avg_entropy < 1.5:
                score += 0.03

        # --- IP CHANGES (col 3) ---
        if arr.shape[1] > 3:
            ip_changes = int(np.sum(arr[:, 3]))
            if ip_changes > 2:
                score += 0.30
                indicators.append(f"Multiple IP changes detected ({ip_changes})")
            elif ip_changes > 0:
                score += 0.15
                indicators.append(f"IP address changed ({ip_changes} time(s))")

        # --- USER AGENT CHANGES (col 4) ---
        if arr.shape[1] > 4:
            ua_changes = int(np.sum(arr[:, 4]))
            if ua_changes > 5:
                score += 0.20
                indicators.append(f"Frequent user agent changes ({ua_changes} time(s))")
            elif ua_changes > 1:
                score += 0.10
                indicators.append(f"Multiple user agent changes ({ua_changes} time(s))")
            elif ua_changes > 0:
                score += 0.05
                indicators.append("Single user agent change detected")

        # --- VOLUME ---
        if n_clicks > 100:
            score += 0.15
            indicators.append(f"High click volume ({n_clicks} clicks)")
        elif n_clicks > 50:
            score += 0.08

        # --- SPEED ANALYSIS (clicks per second) ---
        # Fast interaction is a strong fraud signal
        if n_clicks > 0 and arr.shape[1] > 0:
            avg_time = float(np.mean(arr[:, 0]))
            clicks_per_second = n_clicks / (n_clicks * avg_time + 1e-9)
            
            # Very fast clicking (bot-like)
            if n_clicks > 20 and avg_time < 1.0:
                score += 0.20
                indicators.append(f"Rapid clicking ({n_clicks} clicks at {avg_time:.2f}s intervals)")
            # Fast clicking with suspicious pattern
            elif n_clicks > 5 and avg_time < 3.0:
                score += 0.10
                indicators.append(f"Fast interaction speed ({avg_time:.2f}s per click)")
            # Moderate speed
            elif n_clicks > 10 and avg_time < 5.0:
                score += 0.05
                indicators.append(f"Elevated clicking activity")

        # Guardrail: suspicious traffic should not be auto-marked CRITICAL unless it shows
        # clear bot-level characteristics across multiple strong indicators.
        avg_time_for_guard = float(np.mean(arr[:, 0])) if arr.shape[1] > 0 else 0.0
        avg_velocity_for_guard = float(np.mean(arr[:, 7])) if arr.shape[1] > 7 else 0.0
        ip_changes_for_guard = int(np.sum(arr[:, 3])) if arr.shape[1] > 3 else 0
        ua_changes_for_guard = int(np.sum(arr[:, 4])) if arr.shape[1] > 4 else 0
        avg_entropy_for_guard = float(np.mean(arr[:, 8])) if arr.shape[1] > 8 else 2.0
        x_std_for_guard = float(np.std(arr[:, 1])) if arr.shape[1] > 1 else 0.0
        y_std_for_guard = float(np.std(arr[:, 2])) if arr.shape[1] > 2 else 0.0

        if (
            30 <= n_clicks <= 150 and
            avg_time_for_guard >= 0.45 and
            avg_velocity_for_guard <= 100 and
            ip_changes_for_guard <= 4 and
            ua_changes_for_guard <= 2 and
            avg_entropy_for_guard >= 0.0 and
            (x_std_for_guard > 20 or y_std_for_guard > 20)
        ):
            if score > 0.48:
                score = 0.48
                indicators.append("Suspicious traffic pattern, but not strong enough for critical bot classification")

        # Cap and return
        prob = min(0.95, score)
        result = self._format_result(prob, 'Heuristic')
        if indicators:
            result['indicators'] = indicators
        return result

    def _format_result(self, prob, model_used):
        if prob > 0.75:
            risk_level = 'CRITICAL'
            is_fraud = True
            recommendation = 'BLOCK - Automated bot activity detected'
        elif prob > 0.5:
            risk_level = 'HIGH'
            is_fraud = True
            recommendation = 'STEP-UP VERIFICATION - High fraud probability detected'
        elif prob > 0.3:
            risk_level = 'MEDIUM'
            is_fraud = False
            recommendation = 'MONITOR - Unusual click behavior'
        elif prob > 0.15:
            risk_level = 'LOW'
            is_fraud = False
            recommendation = 'MONITOR - Some irregular patterns detected'
        else:
            risk_level = 'LOW'
            is_fraud = False
            recommendation = 'ALLOW - Normal click behavior'

        return {
            'is_fraud': bool(is_fraud),
            'fraud_probability': round(float(prob), 4),
            'risk_level': risk_level,
            'model_used': model_used,
            'recommendation': recommendation
        }
