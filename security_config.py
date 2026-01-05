"""
Advanced Security Configuration for MDFDP
Centralized security settings and constants
"""

# ==================== AUTHENTICATION SETTINGS ====================
AUTH_CONFIG = {
    # Multi-Factor Authentication
    'MFA_ENABLED': True,
    'TOTP_ENABLED': True,
    'WEBAUTHN_ENABLED': True,
    'BIOMETRIC_ENABLED': True,
    
    # Session Settings
    'SESSION_TIMEOUT_MINUTES': 30,
    'IDLE_TIMEOUT_MINUTES': 15,
    'MAX_CONCURRENT_SESSIONS': 3,
    'SESSION_REFRESH_INTERVAL': 300,  # 5 minutes
    
    # Password Policy
    'MIN_PASSWORD_LENGTH': 12,
    'REQUIRE_UPPERCASE': True,
    'REQUIRE_LOWERCASE': True,
    'REQUIRE_NUMBERS': True,
    'REQUIRE_SPECIAL_CHARS': True,
    'PASSWORD_EXPIRY_DAYS': 90,
    'PASSWORD_HISTORY_COUNT': 5,
    
    # Account Lockout
    'MAX_LOGIN_ATTEMPTS': 5,
    'LOCKOUT_DURATION_MINUTES': 30,
    'FAILED_ATTEMPT_WINDOW_MINUTES': 15,
}

# ==================== RISK-BASED AUTHENTICATION ====================
RISK_LEVELS = {
    'LOW': {
        'score_range': (0, 30),
        'action': 'allow',
        'additional_auth': False,
        'color': '#2e7d32'
    },
    'MEDIUM': {
        'score_range': (31, 60),
        'action': 'step_up',
        'additional_auth': True,
        'color': '#f9a825'
    },
    'HIGH': {
        'score_range': (61, 85),
        'action': 'challenge',
        'additional_auth': True,
        'color': '#ff6f00'
    },
    'CRITICAL': {
        'score_range': (86, 100),
        'action': 'block',
        'additional_auth': True,
        'color': '#d50000'
    }
}

# Risk Scoring Weights
RISK_WEIGHTS = {
    'new_device': 20,
    'new_location': 15,
    'impossible_travel': 40,
    'suspicious_ip': 25,
    'unusual_time': 10,
    'failed_attempts': 15,
    'tor_vpn': 30,
    'high_risk_country': 20,
    'behavioral_anomaly': 25,
    'credential_stuffing': 35,
}

# ==================== GEO-FENCING ====================
GEO_CONFIG = {
    # Allowed Countries (ISO codes)
    'ALLOWED_COUNTRIES': ['IN', 'US', 'GB', 'CA', 'AU', 'SG', 'AE'],
    
    # High-Risk Countries
    'HIGH_RISK_COUNTRIES': ['KP', 'IR', 'SY'],
    
    # Impossible Travel Settings
    'MAX_TRAVEL_SPEED_KMH': 800,  # Max realistic travel speed
    'MIN_TIME_BETWEEN_LOCATIONS_MINUTES': 30,
    
    # IP Reputation
    'BLOCK_TOR': True,
    'BLOCK_VPN': False,  # Set to True for stricter security
    'BLOCK_PROXY': True,
    'BLOCK_DATACENTER': False,
}

# ==================== BEHAVIORAL BIOMETRICS ====================
BEHAVIORAL_CONFIG = {
    # Keystroke Dynamics
    'KEYSTROKE_ENABLED': True,
    'KEYSTROKE_THRESHOLD': 0.75,  # Similarity threshold
    
    # Mouse Dynamics
    'MOUSE_TRACKING_ENABLED': True,
    'MOUSE_THRESHOLD': 0.70,
    
    # Touch Dynamics (Mobile)
    'TOUCH_ENABLED': True,
    'TOUCH_THRESHOLD': 0.65,
    
    # Continuous Authentication
    'CONTINUOUS_AUTH_ENABLED': True,
    'REAUTH_INTERVAL_MINUTES': 10,
    'ANOMALY_THRESHOLD': 0.60,
}

# ==================== DEVICE FINGERPRINTING ====================
DEVICE_CONFIG = {
    'FINGERPRINTING_ENABLED': True,
    'TRUSTED_DEVICE_DURATION_DAYS': 30,
    'MAX_TRUSTED_DEVICES': 5,
    
    # Device Attributes to Track
    'TRACK_ATTRIBUTES': [
        'user_agent',
        'screen_resolution',
        'timezone',
        'language',
        'platform',
        'plugins',
        'canvas_fingerprint',
        'webgl_fingerprint',
        'audio_fingerprint',
    ],
}

# ==================== THREAT DETECTION ====================
THREAT_CONFIG = {
    # Rate Limiting
    'RATE_LIMIT_ENABLED': True,
    'MAX_REQUESTS_PER_MINUTE': 60,
    'MAX_LOGIN_ATTEMPTS_PER_HOUR': 10,
    'MAX_API_CALLS_PER_MINUTE': 100,
    
    # Bot Detection
    'BOT_DETECTION_ENABLED': True,
    'RECAPTCHA_ENABLED': True,
    'RECAPTCHA_THRESHOLD': 0.5,
    
    # Session Monitoring
    'SESSION_MONITORING_ENABLED': True,
    'DETECT_SESSION_HIJACKING': True,
    'DETECT_TOKEN_THEFT': True,
    
    # Credential Stuffing Detection
    'CREDENTIAL_STUFFING_DETECTION': True,
    'BREACHED_PASSWORD_CHECK': True,
}

# ==================== ENCRYPTION ====================
ENCRYPTION_CONFIG = {
    'PASSWORD_HASH_ALGORITHM': 'argon2',  # argon2, bcrypt, scrypt
    'ARGON2_TIME_COST': 2,
    'ARGON2_MEMORY_COST': 65536,  # 64 MB
    'ARGON2_PARALLELISM': 4,
    
    # Data Encryption
    'ENCRYPT_SENSITIVE_DATA': True,
    'ENCRYPTION_ALGORITHM': 'AES-256-GCM',
    'KEY_ROTATION_DAYS': 90,
    
    # Zero-Knowledge
    'ZERO_KNOWLEDGE_ENABLED': False,  # Advanced feature
}

# ==================== WEBAUTHN / FIDO2 ====================
WEBAUTHN_CONFIG = {
    'ENABLED': True,
    'RP_NAME': 'MDFDP - Multi-Domain Fraud Detection Platform',
    'RP_ID': 'localhost',  # Change to your domain in production
    'ORIGIN': 'http://localhost:5000',  # Change in production
    'ATTESTATION': 'none',  # none, indirect, direct
    'USER_VERIFICATION': 'preferred',  # required, preferred, discouraged
    'AUTHENTICATOR_ATTACHMENT': 'cross-platform',  # platform, cross-platform
    'TIMEOUT': 60000,  # 60 seconds
}

# ==================== LIVENESS DETECTION ====================
LIVENESS_CONFIG = {
    'ENABLED': True,
    'BLINK_DETECTION': True,
    'FACE_DEPTH_ANALYSIS': True,
    'ANTI_SPOOFING': True,
    'CHALLENGE_RESPONSE': True,
    
    # Thresholds
    'MIN_BLINKS': 2,
    'MAX_TIME_SECONDS': 10,
    'FACE_CONFIDENCE_THRESHOLD': 0.85,
}

# ==================== DECEPTION & HONEYPOTS ====================
DECEPTION_CONFIG = {
    'ENABLED': True,
    'FAKE_ADMIN_PANEL': '/admin-legacy',
    'FAKE_API_ENDPOINTS': [
        '/api/v1/internal/users',
        '/api/debug/config',
        '/api/admin/settings',
    ],
    'HONEYPOT_ACCOUNTS': [
        'admin@system.local',
        'root@localhost',
        'administrator@mdfdp.com',
    ],
}

# ==================== ACCESS CONTROL ====================
RBAC_CONFIG = {
    'ENABLED': True,
    
    # Roles
    'ROLES': {
        'SUPER_ADMIN': {
            'level': 100,
            'permissions': ['*'],  # All permissions
        },
        'ADMIN': {
            'level': 80,
            'permissions': [
                'view_all_users',
                'manage_users',
                'view_analytics',
                'manage_settings',
                'view_logs',
            ],
        },
        'ANALYST': {
            'level': 60,
            'permissions': [
                'view_analytics',
                'run_detections',
                'view_reports',
                'export_data',
            ],
        },
        'USER': {
            'level': 40,
            'permissions': [
                'run_detections',
                'view_own_data',
                'update_profile',
            ],
        },
        'GUEST': {
            'level': 20,
            'permissions': [
                'view_public_info',
            ],
        },
    },
}

# ==================== SECURITY LOGGING ====================
LOGGING_CONFIG = {
    'ENABLED': True,
    'LOG_LEVEL': 'INFO',  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    
    # Events to Log
    'LOG_EVENTS': [
        'login_success',
        'login_failure',
        'logout',
        'password_change',
        'mfa_setup',
        'mfa_verification',
        'session_created',
        'session_expired',
        'permission_denied',
        'suspicious_activity',
        'account_locked',
        'device_registered',
        'risk_score_calculated',
        'security_alert',
    ],
    
    # SIEM Integration
    'SIEM_ENABLED': False,
    'SIEM_TYPE': None,  # 'splunk', 'elk', 'sentinel', 'qradar'
    'SIEM_ENDPOINT': None,
}

# ==================== ALERTS & NOTIFICATIONS ====================
ALERT_CONFIG = {
    'ENABLED': True,
    
    # Alert Channels
    'EMAIL_ALERTS': True,
    'SMS_ALERTS': False,
    'PUSH_NOTIFICATIONS': False,
    
    # Alert Triggers
    'ALERT_ON': [
        'account_locked',
        'impossible_travel',
        'new_device_login',
        'high_risk_login',
        'credential_stuffing_detected',
        'session_hijacking_detected',
        'honeypot_triggered',
    ],
    
    # Alert Thresholds
    'MIN_RISK_SCORE_FOR_ALERT': 70,
}

# ==================== WAF SETTINGS ====================
WAF_CONFIG = {
    'ENABLED': True,
    
    # Protection Rules
    'SQL_INJECTION_PROTECTION': True,
    'XSS_PROTECTION': True,
    'CSRF_PROTECTION': True,
    'COMMAND_INJECTION_PROTECTION': True,
    'PATH_TRAVERSAL_PROTECTION': True,
    
    # Request Filtering
    'MAX_REQUEST_SIZE_MB': 10,
    'ALLOWED_METHODS': ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
    'BLOCK_SUSPICIOUS_HEADERS': True,
}

# ==================== API SECURITY ====================
API_CONFIG = {
    'AUTHENTICATION': 'JWT',  # JWT, OAuth2, mTLS
    'JWT_EXPIRY_MINUTES': 60,
    'JWT_REFRESH_ENABLED': True,
    'JWT_ALGORITHM': 'HS256',
    
    # API Rate Limiting
    'RATE_LIMIT_ENABLED': True,
    'REQUESTS_PER_MINUTE': 100,
    'BURST_LIMIT': 150,
    
    # CORS
    'CORS_ENABLED': True,
    'ALLOWED_ORIGINS': ['http://localhost:5000'],
}

# ==================== HIGH-RISK INDICATORS ====================
HIGH_RISK_INDICATORS = {
    'IP_RANGES': [
        # Add known malicious IP ranges
    ],
    
    'USER_AGENTS': [
        'sqlmap',
        'nikto',
        'nmap',
        'masscan',
        'metasploit',
    ],
    
    'SUSPICIOUS_PATTERNS': [
        r'(\bor\b|\band\b).*=.*',  # SQL injection
        r'<script.*?>.*?</script>',  # XSS
        r'\.\./\.\.',  # Path traversal
        r'eval\s*\(',  # Code injection
    ],
}

# ==================== TRUSTED NETWORKS ====================
TRUSTED_NETWORKS = {
    'CORPORATE_IPS': [
        # Add your corporate IP ranges
    ],
    
    'WHITELISTED_IPS': [
        '127.0.0.1',
        '::1',
    ],
}

# ==================== FEATURE FLAGS ====================
FEATURE_FLAGS = {
    'ADVANCED_MFA': True,
    'BEHAVIORAL_BIOMETRICS': True,
    'CONTINUOUS_AUTH': True,
    'IMPOSSIBLE_TRAVEL': True,
    'DEVICE_FINGERPRINTING': True,
    'RISK_BASED_AUTH': True,
    'LIVENESS_DETECTION': False,  # Requires additional setup
    'WEBAUTHN': True,
    'DECEPTION_TECH': True,
    'WAF': True,
    'SIEM_INTEGRATION': False,  # Requires external SIEM
}

# ==================== EXTERNAL SERVICES ====================
EXTERNAL_SERVICES = {
    # IP Geolocation
    'IP_GEOLOCATION_API': 'https://ipapi.co/{ip}/json/',
    'IP_GEOLOCATION_ENABLED': True,
    
    # Breach Database
    'HIBP_API': 'https://api.pwnedpasswords.com/range/',
    'HIBP_ENABLED': True,
    
    # reCAPTCHA
    'RECAPTCHA_SITE_KEY': '',  # Add your key
    'RECAPTCHA_SECRET_KEY': '',  # Add your key
    
    # SMS Provider (for SMS MFA)
    'SMS_PROVIDER': 'twilio',  # twilio, nexmo, aws_sns
    'SMS_API_KEY': '',
    'SMS_API_SECRET': '',
}

# ==================== SECURITY HEADERS ====================
SECURITY_HEADERS = {
    'X-Frame-Options': 'DENY',
    'X-Content-Type-Options': 'nosniff',
    'X-XSS-Protection': '1; mode=block',
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
    'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://unpkg.com; style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com https://unpkg.com; img-src 'self' data: https:; font-src 'self' https://cdnjs.cloudflare.com;",
    'Referrer-Policy': 'strict-origin-when-cross-origin',
    'Permissions-Policy': 'geolocation=(), microphone=(), camera=()',
}

# ==================== EXPORT ====================
__all__ = [
    'AUTH_CONFIG',
    'RISK_LEVELS',
    'RISK_WEIGHTS',
    'GEO_CONFIG',
    'BEHAVIORAL_CONFIG',
    'DEVICE_CONFIG',
    'THREAT_CONFIG',
    'ENCRYPTION_CONFIG',
    'WEBAUTHN_CONFIG',
    'LIVENESS_CONFIG',
    'DECEPTION_CONFIG',
    'RBAC_CONFIG',
    'LOGGING_CONFIG',
    'ALERT_CONFIG',
    'WAF_CONFIG',
    'API_CONFIG',
    'HIGH_RISK_INDICATORS',
    'TRUSTED_NETWORKS',
    'FEATURE_FLAGS',
    'EXTERNAL_SERVICES',
    'SECURITY_HEADERS',
]
