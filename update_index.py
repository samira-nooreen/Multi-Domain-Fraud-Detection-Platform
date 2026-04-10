# Update index.html with coming soon feature
file_path = "templates/index.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add CSS link before </head>
css_link = '  <link rel="stylesheet" href="{{ url_for(\'static\', filename=\'css/coming-soon.css\') }}">\n'
content = content.replace('</head>', css_link + '</head>')

# 2. Add JS script before </head>  
js_script = '  <script src="{{ url_for(\'static\', filename=\'js/coming-soon.js\') }}"></script>\n'
content = content.replace('</head>', js_script + '</head>')

# 3. Update Document Forgery card
old_card = '''    <div class="card">
      <div class="card-icon"><i class="fa-solid fa-id-badge"></i></div>
      <div class="card-title">Document Forgery</div>
      <div class="card-desc">Detect tampered identity cards with OCR and image analysis.</div>
      <button class="detect-btn" onclick="checkLoginAndRedirect('/detect_forgery')">Detect</button>
    </div>'''

new_card = '''    <div class="card coming-soon-card">
      <div class="card-icon"><i class="fa-solid fa-id-badge"></i></div>
      <div class="card-title">Document Forgery</div>
      <div class="card-desc">Detect tampered identity cards with OCR and image analysis.</div>
      <button class="detect-btn coming-soon-btn" onclick="showComingSoonPopup('Document Forgery')" disabled>
        <i class="fas fa-clock"></i> Coming Soon
      </button>
    </div>'''

content = content.replace(old_card, new_card)

# Write back
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ index.html updated successfully!")
print("✅ Added coming-soon.css")
print("✅ Added coming-soon.js")
print("✅ Updated Document Forgery card")
