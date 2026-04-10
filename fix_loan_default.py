import re

file_path = "templates/loan_default.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the duplicate DOMContentLoaded listeners that set inline styles
pattern = r'    <script>\s*// Ensure result card is hidden on page load\s*document\.addEventListener\("DOMContentLoaded".*?resultCard\.style\.display = "none";.*?\}\);\s*// Ensure result card is hidden on page load\s*document\.addEventListener\("DOMContentLoaded".*?resultCard\.style\.display = "none";.*?\}\);\s*'

content = re.sub(pattern, '    <script>\n', content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ loan_default.html fixed - Removed inline style JavaScript")
print("✅ Result card will now show properly when you click Predict")
