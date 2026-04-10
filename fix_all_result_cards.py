"""
Fix all fraud detection pages to hide result cards by default
"""
import os
import re

templates_dir = "templates"
fixed_count = 0

# List of fraud detection pages to fix
pages_to_fix = [
    "brand_abuse.html",
    "click_fraud.html",
    "credit_card.html",
    "document_forgery.html",
    "fake_news.html",
    "fake_profile.html",
    "insurance_fraud.html",
    "loan_default.html",
    "phishing_url.html",
    "spam_email.html",
    "upi_fraud.html"
]

for filename in pages_to_fix:
    filepath = os.path.join(templates_dir, filename)
    
    if not os.path.exists(filepath):
        print(f"⚠️  {filename} - File not found")
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Fix 1: Remove inline style="display: none;" if it exists
    content = re.sub(
        r'<div class="result-card" id="resultCard" style="display: none;">',
        '<div class="result-card" id="resultCard">',
        content
    )
    
    # Fix 2: Ensure CSS has display: none for .result-card
    # Check if CSS already has the rule
    if '.result-card {' in content and 'display: none' not in content.split('.result-card.show')[0]:
        # Add display: none to .result-card
        content = re.sub(
            r'(\.result-card \{)',
            r'\1\n            display: none;',
            content
        )
    
    # Fix 3: Add JavaScript to ensure result card is hidden on page load
    # Find the script section and add DOMContentLoaded event
    if "DOMContentLoaded" not in content and "resultCard" in content:
        # Add hiding script at the beginning of the first script tag
        content = re.sub(
            r'(<script>)',
            r'\1\n        // Ensure result card is hidden on page load\n        document.addEventListener("DOMContentLoaded", function() {\n            const resultCard = document.getElementById("resultCard");\n            if (resultCard) {\n                resultCard.style.display = "none";\n            }\n        });\n        ',
            content,
            count=1
        )
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ {filename} - Fixed")
        fixed_count += 1
    else:
        print(f"⏭️  {filename} - No changes needed")

print(f"\n{'='*60}")
print(f"🎉 Fixed {fixed_count}/{len(pages_to_fix)} files")
print(f"{'='*60}")
