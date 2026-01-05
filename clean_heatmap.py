#!/usr/bin/env python3
import re

with open('templates/index.html', 'r') as f:
    content = f.read()

# Find the wrld-map div and clean out all Leaflet markup
pattern = r'(<div\s+id="wrld-map"[^>]*>)(.*?)(\n        </div>\n\n        <!-- Incident Distribution -->)'

replacement = r'\1\n            <!-- Map will be initialized by wrld.js -->\n          \3'

new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# Check if replacement worked
if new_content != content:
    print("✓ Successfully cleaned Leaflet markup from wrld-map")
    with open('templates/index.html', 'w') as f:
        f.write(new_content)
else:
    print("✗ Pattern not found or replacement failed")
    # Try to find what's between wrld-map div
    start = content.find('id="wrld-map"')
    if start > 0:
        section = content[start:start+500]
        print(f"Found wrld-map, next 500 chars:\n{section}")
