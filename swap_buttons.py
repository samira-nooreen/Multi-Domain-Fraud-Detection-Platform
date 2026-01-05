"""
Script to swap Profile and Logout buttons in index.html
"""

# Read the file
with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace Profile in navbar links with a placeholder
content = content.replace('<li><a href="/profile">Profile</a></li>', '<!--PROFILE_PLACEHOLDER-->')

# Find and replace Logout button with Profile button
content = content.replace(
    '<a href="/logout" class="navbar-btn" style="text-decoration: none;">Logout</a>',
    '<a href="/profile" class="navbar-btn" style="text-decoration: none;">Profile</a>'
)

# Replace the placeholder with Logout link
content = content.replace('<!--PROFILE_PLACEHOLDER-->', '<li><a href="/logout">Logout</a></li>')

# Write back
with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Successfully swapped Profile and Logout buttons!")
print("   - Logout is now in the navbar links")
print("   - Profile is now the navbar button")
