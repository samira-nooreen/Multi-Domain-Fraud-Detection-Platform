"""
Risk-Based Authentication Engine
Calculates risk scores and determines authentication requirements
"""

import datetime
import hashlib
import json
from typing import Dict, Tuple, Optional
from security_config import RISK_LEVELS, RISK_WEIGHTS, GEO_CONFIG, FEATURE_FLAGS
import math


class RiskCalculator:
    """Calculate risk scores for authentication attempts"""
    
    def __init__(self):
        self.risk_weights = RISK_WEIGHTS
        self.risk_levels = RISK_LEVELS
        
    def calculate_risk_score(self, context: Dict) -> Tuple[int, str, Dict]:
        """
        Calculate overall risk score based on multiple factors
        
        Args:
            context: Dictionary containing authentication context
            
        Returns:
            Tuple of (risk_score, risk_level, risk_factors)
        """
        risk_score = 0
        risk_factors = {}
        
        # Check for new device
        if context.get('is_new_device', False):
            risk_score += self.risk_weights['new_device']
            risk_factors['new_device'] = True
            
        # Check for new location
        if context.get('is_new_location', False):
            risk_score += self.risk_weights['new_location']
            risk_factors['new_location'] = True
            
        # Check for impossible travel
        if self._detect_impossible_travel(context):
            risk_score += self.risk_weights['impossible_travel']
            risk_factors['impossible_travel'] = True
            
        # Check IP reputation
        ip_risk = self._check_ip_reputation(context.get('ip_address'))
        if ip_risk > 0:
            risk_score += ip_risk
            risk_factors['suspicious_ip'] = True
            
        # Check for unusual login time
        if self._is_unusual_time(context.get('timestamp'), context.get('user_timezone')):
            risk_score += self.risk_weights['unusual_time']
            risk_factors['unusual_time'] = True
            
        # Check failed attempts
        failed_attempts = context.get('recent_failed_attempts', 0)
        if failed_attempts > 0:
            risk_score += min(failed_attempts * 5, self.risk_weights['failed_attempts'])
            risk_factors['failed_attempts'] = failed_attempts
            
        # Check for TOR/VPN
        if context.get('is_tor', False) or context.get('is_vpn', False):
            risk_score += self.risk_weights['tor_vpn']
            risk_factors['tor_vpn'] = True
            
        # Check for high-risk country
        if self._is_high_risk_country(context.get('country_code')):
            risk_score += self.risk_weights['high_risk_country']
            risk_factors['high_risk_country'] = True
            
        # Check behavioral anomaly
        if context.get('behavioral_anomaly_score', 0) > 0.7:
            risk_score += self.risk_weights['behavioral_anomaly']
            risk_factors['behavioral_anomaly'] = True
            
        # Check for credential stuffing patterns
        if context.get('credential_stuffing_detected', False):
            risk_score += self.risk_weights['credential_stuffing']
            risk_factors['credential_stuffing'] = True
            
        # Cap at 100
        risk_score = min(risk_score, 100)
        
        # Determine risk level
        risk_level = self._get_risk_level(risk_score)
        
        return risk_score, risk_level, risk_factors
    
    def _detect_impossible_travel(self, context: Dict) -> bool:
        """Detect if user traveled impossibly fast between locations"""
        if not FEATURE_FLAGS.get('IMPOSSIBLE_TRAVEL', False):
            return False
            
        last_location = context.get('last_location')
        current_location = context.get('current_location')
        last_login_time = context.get('last_login_time')
        current_time = context.get('timestamp', datetime.datetime.now())
        
        if not all([last_location, current_location, last_login_time]):
            return False
            
        # Calculate distance between locations
        distance_km = self._calculate_distance(
            last_location.get('lat'), last_location.get('lon'),
            current_location.get('lat'), current_location.get('lon')
        )
        
        # Calculate time difference in hours
        time_diff = (current_time - last_login_time).total_seconds() / 3600
        
        if time_diff == 0:
            return distance_km > 0
            
        # Calculate required speed
        required_speed = distance_km / time_diff
        
        # Check if speed exceeds maximum realistic travel speed
        max_speed = GEO_CONFIG.get('MAX_TRAVEL_SPEED_KMH', 800)
        
        return required_speed > max_speed
    
    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two coordinates using Haversine formula"""
        if not all([lat1, lon1, lat2, lon2]):
            return 0
            
        # Earth radius in kilometers
        R = 6371
        
        # Convert to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        return R * c
    
    def _check_ip_reputation(self, ip_address: Optional[str]) -> int:
        """Check IP address reputation and return risk score"""
        if not ip_address:
            return 0
            
        risk_score = 0
        
        # Check if IP is in known malicious ranges
        # In production, integrate with threat intelligence feeds
        
        # Placeholder: Check for private/local IPs (low risk)
        if ip_address.startswith(('127.', '192.168.', '10.', '172.')):
            return 0
            
        # In production, check against:
        # - Threat intelligence feeds
        # - Known proxy/VPN IP ranges
        # - Tor exit nodes
        # - Previously flagged IPs
        
        return risk_score
    
    def _is_unusual_time(self, timestamp: Optional[datetime.datetime], user_timezone: Optional[str]) -> bool:
        """Check if login time is unusual for the user"""
        if not timestamp:
            return False
            
        # Get hour of day
        hour = timestamp.hour
        
        # Consider 2 AM - 6 AM as unusual (can be customized per user)
        return 2 <= hour < 6
    
    def _is_high_risk_country(self, country_code: Optional[str]) -> bool:
        """Check if country is in high-risk list"""
        if not country_code:
            return False
            
        high_risk_countries = GEO_CONFIG.get('HIGH_RISK_COUNTRIES', [])
        return country_code in high_risk_countries
    
    def _get_risk_level(self, risk_score: int) -> str:
        """Determine risk level based on score"""
        for level, config in self.risk_levels.items():
            min_score, max_score = config['score_range']
            if min_score <= risk_score <= max_score:
                return level
        return 'CRITICAL'
    
    def get_required_auth_action(self, risk_level: str) -> Dict:
        """Get required authentication action based on risk level"""
        level_config = self.risk_levels.get(risk_level, self.risk_levels['CRITICAL'])
        
        return {
            'action': level_config['action'],
            'additional_auth_required': level_config['additional_auth'],
            'message': self._get_action_message(level_config['action']),
            'color': level_config['color']
        }
    
    def _get_action_message(self, action: str) -> str:
        """Get user-friendly message for action"""
        messages = {
            'allow': 'Login approved',
            'step_up': 'Additional verification required',
            'challenge': 'Security challenge required',
            'block': 'Login blocked due to high risk'
        }
        return messages.get(action, 'Unknown action')


class DeviceFingerprint:
    """Generate and verify device fingerprints"""
    
    @staticmethod
    def generate_fingerprint(device_info: Dict) -> str:
        """Generate unique device fingerprint"""
        # Combine device attributes
        fingerprint_data = {
            'user_agent': device_info.get('user_agent', ''),
            'screen_resolution': device_info.get('screen_resolution', ''),
            'timezone': device_info.get('timezone', ''),
            'language': device_info.get('language', ''),
            'platform': device_info.get('platform', ''),
            'canvas': device_info.get('canvas_fingerprint', ''),
            'webgl': device_info.get('webgl_fingerprint', ''),
        }
        
        # Create hash
        fingerprint_string = json.dumps(fingerprint_data, sort_keys=True)
        fingerprint_hash = hashlib.sha256(fingerprint_string.encode()).hexdigest()
        
        return fingerprint_hash
    
    @staticmethod
    def is_trusted_device(fingerprint: str, trusted_devices: list) -> bool:
        """Check if device is in trusted list"""
        return fingerprint in trusted_devices


class BehavioralAnalyzer:
    """Analyze user behavioral patterns"""
    
    def __init__(self):
        self.baseline_patterns = {}
    
    def analyze_keystroke_dynamics(self, keystroke_data: Dict) -> float:
        """
        Analyze keystroke patterns
        Returns anomaly score (0-1, higher = more anomalous)
        """
        if not keystroke_data:
            return 0.0
            
        # Extract features
        avg_dwell_time = keystroke_data.get('avg_dwell_time', 0)
        avg_flight_time = keystroke_data.get('avg_flight_time', 0)
        typing_speed = keystroke_data.get('typing_speed', 0)
        
        # In production, compare with user's baseline
        # For now, return low anomaly score
        return 0.1
    
    def analyze_mouse_dynamics(self, mouse_data: Dict) -> float:
        """
        Analyze mouse movement patterns
        Returns anomaly score (0-1)
        """
        if not mouse_data:
            return 0.0
            
        # Extract features
        avg_speed = mouse_data.get('avg_speed', 0)
        avg_acceleration = mouse_data.get('avg_acceleration', 0)
        click_patterns = mouse_data.get('click_patterns', [])
        
        # Compare with baseline
        return 0.1
    
    def analyze_session_behavior(self, session_data: Dict) -> float:
        """
        Analyze overall session behavior
        Returns anomaly score (0-1)
        """
        anomaly_score = 0.0
        
        # Check for rapid-fire actions
        actions_per_minute = session_data.get('actions_per_minute', 0)
        if actions_per_minute > 100:  # Suspiciously fast
            anomaly_score += 0.3
            
        # Check for unusual navigation patterns
        page_sequence = session_data.get('page_sequence', [])
        if self._is_unusual_sequence(page_sequence):
            anomaly_score += 0.2
            
        # Check for copy-paste behavior (potential bot)
        copy_paste_ratio = session_data.get('copy_paste_ratio', 0)
        if copy_paste_ratio > 0.8:
            anomaly_score += 0.2
            
        return min(anomaly_score, 1.0)
    
    def _is_unusual_sequence(self, page_sequence: list) -> bool:
        """Check if page navigation sequence is unusual"""
        # Implement logic to detect bot-like navigation
        # For now, return False
        return False
    
    def get_combined_behavioral_score(self, behavioral_data: Dict) -> float:
        """Get combined behavioral anomaly score"""
        keystroke_score = self.analyze_keystroke_dynamics(
            behavioral_data.get('keystroke', {})
        )
        mouse_score = self.analyze_mouse_dynamics(
            behavioral_data.get('mouse', {})
        )
        session_score = self.analyze_session_behavior(
            behavioral_data.get('session', {})
        )
        
        # Weighted average
        combined_score = (
            keystroke_score * 0.3 +
            mouse_score * 0.3 +
            session_score * 0.4
        )
        
        return combined_score


class ThreatDetector:
    """Detect various security threats"""
    
    @staticmethod
    def detect_credential_stuffing(login_attempts: list) -> bool:
        """Detect credential stuffing attack patterns"""
        if len(login_attempts) < 5:
            return False
            
        # Check for rapid login attempts with different usernames
        unique_usernames = set(attempt.get('username') for attempt in login_attempts)
        time_window = (login_attempts[-1]['timestamp'] - login_attempts[0]['timestamp']).total_seconds()
        
        # If many different usernames in short time = credential stuffing
        if len(unique_usernames) > 10 and time_window < 60:
            return True
            
        return False
    
    @staticmethod
    def detect_session_hijacking(session_data: Dict) -> bool:
        """Detect potential session hijacking"""
        # Check for sudden changes in:
        # - IP address
        # - User agent
        # - Geolocation
        
        ip_changed = session_data.get('ip_changed', False)
        ua_changed = session_data.get('user_agent_changed', False)
        location_changed = session_data.get('location_changed', False)
        
        # If multiple attributes changed suddenly = potential hijacking
        changes = sum([ip_changed, ua_changed, location_changed])
        return changes >= 2
    
    @staticmethod
    def detect_bot_behavior(request_data: Dict) -> bool:
        """Detect bot-like behavior"""
        # Check for bot indicators
        user_agent = request_data.get('user_agent', '').lower()
        
        # Known bot user agents
        bot_indicators = ['bot', 'crawler', 'spider', 'scraper', 'curl', 'wget']
        if any(indicator in user_agent for indicator in bot_indicators):
            return True
            
        # Check for missing browser features
        has_cookies = request_data.get('has_cookies', True)
        has_javascript = request_data.get('has_javascript', True)
        
        if not has_cookies or not has_javascript:
            return True
            
        return False


# Example usage
if __name__ == '__main__':
    # Example risk calculation
    calculator = RiskCalculator()
    
    context = {
        'is_new_device': True,
        'is_new_location': False,
        'ip_address': '203.0.113.1',
        'country_code': 'IN',
        'timestamp': datetime.datetime.now(),
        'user_timezone': 'Asia/Kolkata',
        'recent_failed_attempts': 2,
        'is_tor': False,
        'is_vpn': False,
        'behavioral_anomaly_score': 0.3,
        'credential_stuffing_detected': False,
    }
    
    risk_score, risk_level, risk_factors = calculator.calculate_risk_score(context)
    action = calculator.get_required_auth_action(risk_level)
    
    print(f"Risk Score: {risk_score}")
    print(f"Risk Level: {risk_level}")
    print(f"Risk Factors: {risk_factors}")
    print(f"Required Action: {action}")
