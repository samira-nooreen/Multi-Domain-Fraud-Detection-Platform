file_path = "templates/insurance_fraud.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add textarea styling after the input/select styling
old_css = '''        .form-group input, .form-group select {
            width: 100%;
            padding: 12px 15px;
            border-radius: 8px;
            border: 1px solid #2a2a35;
            background: #0d0d0f;
            color: #e6e6e6;
            font-size: 1rem;
        }'''

new_css = '''        .form-group input, .form-group select, .form-group textarea {
            width: 100%;
            padding: 12px 15px;
            border-radius: 8px;
            border: 1px solid #2a2a35;
            background: #0d0d0f;
            color: #e6e6e6;
            font-size: 1rem;
        }
        
        .form-group textarea {
            min-height: 100px;
            resize: vertical;
            font-family: inherit;
        }'''

content = content.replace(old_css, new_css)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Added textarea styling to insurance fraud page")
print("✅ Textarea now matches input field styling")
