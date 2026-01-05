#!/usr/bin/env python3
with open('templates/index.html', 'r') as f:
    content = f.read()

# Find "Real-Time Fraud Heatmap" and the next "Incidents Detected"
heatmap_start = content.find('Real-Time Fraud Heatmap')
incidents_start = content.find('Incidents Detected', heatmap_start)

print(f"Heatmap title at: {heatmap_start}")
print(f"Incidents title at: {incidents_start}")

# Find the closing </div> of heatmap card before incidents
section = content[heatmap_start:incidents_start]
last_close = section.rfind('</div>')
actual_end = heatmap_start + last_close + 6  # +6 for "</div>"

print(f"Heatmap div ends at: {actual_end}")

# Get context
context_start = content.rfind('<', heatmap_start - 100, heatmap_start)
context_lines = content[context_start:actual_end+200].split('\n')
print("\nContext (last 10 lines of heatmap, then first 3 after):")
for i, line in enumerate(context_lines[-13:]):
    print(f"{i}: {line[:100]}")
