"""Small regression checks for fake-news model calibration.

Run:
  .venv\\Scripts\\python.exe check_fake_news_regression.py
"""

from __future__ import annotations

import json
import sys
from typing import Any

from ml_modules.fake_news.predict import DJDarkCyberFakeNewsDetector


def _check_case(result: dict[str, Any], expected: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    if result.get("prediction") != expected["prediction"]:
        errors.append(
            f"prediction expected {expected['prediction']} got {result.get('prediction')}"
        )

    if result.get("risk_level") != expected["risk_level"]:
        errors.append(
            f"risk_level expected {expected['risk_level']} got {result.get('risk_level')}"
        )

    fake_prob = float(result.get("fake_probability", 0.0))
    min_prob, max_prob = expected["fake_prob_range"]
    if not (min_prob <= fake_prob <= max_prob):
        errors.append(
            f"fake_probability expected between {min_prob:.2f} and {max_prob:.2f}, got {fake_prob:.4f}"
        )

    return errors


def main() -> int:
    detector = DJDarkCyberFakeNewsDetector(model_dir="ml_modules/fake_news/models")

    cases = [
        {
            "name": "factual_isro_with_placeholder_url",
            "text": "The Indian Space Research Organisation (ISRO) successfully launched a new satellite aimed at improving weather forecasting and disaster management across the country.",
            "source": "https://example.com/news-article",
            "expected": {
                "prediction": "REAL",
                "risk_level": "LOW",
                "fake_prob_range": (0.08, 0.20),
            },
        },
        {
            "name": "misleading_exaggerated_smartphone_claim",
            "text": "A recent report claims that using smartphones for more than 2 hours a day reduces intelligence by 50%.",
            "source": "https://example.com/news-article",
            "expected": {
                "prediction": "MISLEADING",
                "risk_level": "MEDIUM",
                "fake_prob_range": (0.45, 0.65),
            },
        },
        {
            "name": "strong_health_misinformation",
            "text": "Doctors hate this secret miracle cure that guarantees 100% cancer recovery in 7 days! You won't believe it.",
            "source": "https://unknownblog.com/health",
            "expected": {
                "prediction": "FAKE",
                "risk_level": "HIGH",
                "fake_prob_range": (0.75, 0.99),
            },
        },
    ]

    failures = 0
    for case in cases:
        result = detector.analyze_article("", case["text"], case["source"])
        case_errors = _check_case(result, case["expected"])

        print(f"\n=== {case['name']} ===")
        print(
            json.dumps(
                {
                    "prediction": result.get("prediction"),
                    "risk_level": result.get("risk_level"),
                    "fake_probability": result.get("fake_probability"),
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
        print(f"\nRegression checks finished with {failures} failing case(s).")
        return 1

    print("\nAll fake-news regression checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
