"""Regression checks for phishing URL detector calibration.

Run:
  .venv\\Scripts\\python.exe check_phishing_regression.py
"""

from __future__ import annotations

import json
from typing import Any

from ml_modules.phishing_url.predict import PhishingDetector


def _check_case(result: dict[str, Any], expected: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    if result.get("risk_level") != expected["risk_level"]:
        errors.append(f"risk_level expected {expected['risk_level']} got {result.get('risk_level')}")

    prob = float(result.get("phishing_probability", 0.0))
    lo, hi = expected["prob_range"]
    if not (lo <= prob <= hi):
        errors.append(f"phishing_probability expected between {lo:.2f} and {hi:.2f}, got {prob:.4f}")

    return errors


def main() -> int:
    detector = PhishingDetector(model_path="ml_modules/phishing_url/phishing_model.pkl")

    cases = [
        {
            "name": "amazon_india_legitimate",
            "url": "https://www.amazon.in/account",
            "expected": {"risk_level": "LOW", "prob_range": (0.0, 0.15)},
        },
        {
            "name": "google_accounts_legitimate",
            "url": "https://accounts.google.com",
            "expected": {"risk_level": "LOW", "prob_range": (0.0, 0.15)},
        },
        {
            "name": "shortened_scam_critical",
            "url": "https://bit.ly/free-prize-login",
            "expected": {"risk_level": "CRITICAL", "prob_range": (0.80, 0.99)},
        },
        {
            "name": "paypal_subdomain_spoof_critical",
            "url": "http://paypal.com.security-update.xyz/login",
            "expected": {"risk_level": "CRITICAL", "prob_range": (0.80, 0.99)},
        },
        {
            "name": "brand_typo_spoof_high",
            "url": "https://paypa1.com/login",
            "expected": {"risk_level": "HIGH", "prob_range": (0.60, 0.95)},
        },
    ]

    failures = 0
    for case in cases:
        result = detector.predict(case["url"])
        case_errors = _check_case(result, case["expected"])

        print(f"\n=== {case['name']} ===")
        print(
            json.dumps(
                {
                    "url": case["url"],
                    "risk_level": result.get("risk_level"),
                    "phishing_probability": result.get("phishing_probability"),
                    "is_phishing": result.get("is_phishing"),
                    "url_features": result.get("url_features"),
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
        print(f"\nPhishing regression checks finished with {failures} failing case(s).")
        return 1

    print("\nAll phishing regression checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
