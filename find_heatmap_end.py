#!/usr/bin/env python3
with open('templates/index.html', 'r') as f:
    lines = f.readlines()

# Find dashboard-card heatmap opening at line 358 (index 357)
heatmap_start = 357
incident_start = None

for i in range(heatmap_start, min(heatmap_start + 600, len(lines))):
    # Look for dashboard-card incident (the next card after heatmap)
    if i > heatmap_start and 'class="dashboard-card incident' in lines[i]:
        incident_start = i
        print(f'Heatmap card ends before incident card at line {i+1}')
        print(f'\nLines {i-3} to {i+3}:')
        for j in range(max(0, i-3), min(len(lines), i+3)):
            print(f'{j+1}: {lines[j].rstrip()[:100]}')
        break

if incident_start:
    print(f'\n\nSo heatmap card is from line 358 to line {incident_start}')
