"""Regression checks for spam/phishing detector calibration.

Run:
  .venv\\Scripts\\python.exe check_spam_regression.py
"""

from __future__ import annotations

import json
import sys
from typing import Any

from ml_modules.spam_email.predict import SpamDetector


def _check_case(result: dict[str, Any], expected: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    if result.get("risk_level") != expected["risk_level"]:
        errors.append(
            f"risk_level expected {expected['risk_level']} got {result.get('risk_level')}"
        )

    prob = float(result.get("spam_probability", 0.0))
    lo, hi = expected["prob_range"]
    if not (lo <= prob <= hi):
        errors.append(f"spam_probability expected between {lo:.2f} and {hi:.2f}, got {prob:.4f}")

    for flag_name, expected_value in expected.get("flags", {}).items():
        actual = result.get(flag_name)
        if actual != expected_value:
            errors.append(f"{flag_name} expected {expected_value} got {actual}")

    return errors


def main() -> int:
    detector = SpamDetector(
        model_path="ml_modules/spam_email/spam_model.pkl",
        vec_path="ml_modules/spam_email/spam_vectorizer.pkl",
    )

    cases = [
        {
            "name": "safe_internal_email",
            "text": "From: dean@university.edu\n\nDear student, please check your schedule and confirm registration by Friday.",
            "expected": {
                "risk_level": "LOW",
                "prob_range": (0.0, 0.25),
                "flags": {
                    "spoofed_sender_detected": False,
                    "shortened_links_found": 0,
                },
            },
        },
        {
            "name": "promotional_medium",
            "text": "From: offers@unknownsite.com\n\nCongratulations! You have been selected for an exclusive offer. Click the link to claim your reward.",
            "expected": {
                "risk_level": "MEDIUM",
                "prob_range": (0.50, 0.79),
                "flags": {
                    "spoofed_sender_detected": False,
                },
            },
        },
        {
            "name": "phishing_spoof_shortlink_high",
            "text": "From: paypal-security@paypa1-alerts.xyz\n\nURGENT action required: verify your account now at https://bit.ly/secure-login to avoid suspension.",
            "expected": {
                "risk_level": "HIGH",
                "prob_range": (0.80, 0.99),
                "flags": {
                    "spoofed_sender_detected": True,
                    "shortened_links_found": 1,
                },
            },
        },
        {
            "name": "bank_account_blocked_password_high",
            "text": "From: security-alert@fakebank.com\n\nUrgent! Your bank account will be blocked. Click here and enter your password to verify immediately.",
            "expected": {
                "risk_level": "HIGH",
                "prob_range": (0.80, 0.99),
                "flags": {
                    "shortened_links_found": 0,
                },
            },
        },
        {
            "name": "lottery_prize_scam_high",
            "text": "From: lottery@randommail.com\n\nYou have won ₹10,00,000! Claim your prize now by clicking this link.",
            "expected": {
                "risk_level": "HIGH",
                "prob_range": (0.80, 0.99),
                "flags": {
                    "shortened_links_found": 0,
                },
            },
        },
    ]

    failures = 0
    for case in cases:
        result = detector.predict(case["text"])
        case_errors = _check_case(result, case["expected"])

        print(f"\n=== {case['name']} ===")
        print(
            json.dumps(
                {
                    "risk_level": result.get("risk_level"),
                    "spam_probability": result.get("spam_probability"),
                    "confidence_percent": result.get("confidence_percent"),
                    "spoofed_sender_detected": result.get("spoofed_sender_detected"),
                    "shortened_links_found": result.get("shortened_links_found"),
                    "recommendation": result.get("recommendation"),
                },
                indent=2,
            )
        )

        if case_errors:
            failures += 1
            print("RESULT: FAIL")
            for err in case_errors:
                print(f" - {err}")
        else:
            print("RESULT: PASS")

    if failures:
        print(f"\nSpam regression checks finished with {failures} failing case(s).")
        return 1

    print("\nAll spam regression checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
