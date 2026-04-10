import re

file_path = "templates/insurance_fraud.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the DOMContentLoaded event listener that sets inline style
pattern = r'\s*// Ensure result card is hidden on page load\s*document\.addEventListener\("DOMContentLoaded", function\(\) \{\s*const resultCard = document\.getElementById\("resultCard"\);\s*if \(resultCard\) \{\s*resultCard\.style\.display = "none";\s*\}\s*\}\);'

content = re.sub(pattern, '', content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Removed inline style JavaScript from insurance_fraud.html")
print("✅ Result card will now show properly when you click Analyze Claim")
