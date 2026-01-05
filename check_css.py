"""Check CSS file for issues"""
with open('static/style.css', 'r', encoding='utf-8') as f:
    content = f.read()
    
print(f'Total characters: {len(content)}')
print(f'Lines: {len(content.splitlines())}')
print(f'Opening braces: {content.count("{")}')
print(f'Closing braces: {content.count("}")}')
print(f'Difference: {content.count("{") - content.count("}")}')

# Check for missing closing brace
lines = content.splitlines()
for i, line in enumerate(lines[-20:], start=len(lines)-20):
    print(f'Line {i+1}: {line[:80]}')
