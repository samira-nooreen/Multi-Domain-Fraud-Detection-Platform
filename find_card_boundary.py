#!/usr/bin/env python3
with open('templates/index.html', 'r') as f:
    lines = f.readlines()

# Find the line with "Real-Time Fraud Heatmap"
heatmap_line = None
for i, line in enumerate(lines):
    if 'Real-Time Fraud Heatmap' in line:
        heatmap_line = i
        print(f"Found heatmap title at line {i+1}")
        break

# Now find the next 'class="dashboard-card' after the heatmap one
if heatmap_line:
    for i in range(heatmap_line + 1, min(heatmap_line + 800, len(lines))):
        if 'class="dashboard-card' in lines[i] and i > heatmap_line + 10:
            print(f"Found next dashboard-card at line {i+1}")
            print(f"\nLines {i-2} to {i+2}:")
            for j in range(max(0, i-2), min(len(lines), i+3)):
                print(f"{j+1}: {lines[j].rstrip()[:100]}")
            print(f"\nSo replace from line 358 to line {i}")
            break
