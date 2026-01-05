with open('static/style.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    print(f'✅ New CSS file created successfully!')
    print(f'Lines: {len(lines)}')
    print(f'Size: {sum(len(line) for line in lines)} bytes')
    print(f'Opening braces: {sum(line.count("{") for line in lines)}')
    print(f'Closing braces: {sum(line.count("}") for line in lines)}')
    print(f'Balanced: {"✅ YES" if sum(line.count("{") for line in lines) == sum(line.count("}") for line in lines) else "❌ NO"}')
