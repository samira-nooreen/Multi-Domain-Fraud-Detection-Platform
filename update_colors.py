"""
Automatic Color Standardization Script
Updates all HTML files to match homepage purple theme
"""

import os
import re

# Color mappings: old_color -> new_color
COLOR_MAPPINGS = {
    # Red/Pink to Purple
    '#ff1744': '#8876f8',
    '#f50057': '#c9baff',
    '#d50000': '#7059d2',
    
    # Blue backgrounds to Black/Dark
    '#0a0e27': '#000000',
    '#1a1f3a': '#0d0d0f',
    '#0f1419': '#14141b',
    
    # Text colors
    '#b0b0b0': '#b7b3c9',
    '#e0e0e0': '#e6e6e6',
    
    # Keep critical colors (don't change)
    # '#fa395f': '#fa395f',  # Critical red
    # '#fc8d26': '#fc8d26',  # High orange
    # '#fcea26': '#fcea26',  # Medium yellow
    # '#22d168': '#22d168',  # Low green
}

# Files to update
FILES_TO_UPDATE = [
    'templates/analytics_dashboard.html',
    'templates/security_dashboard.html',
]

def update_colors_in_file(filepath):
    """Update colors in a single file"""
    print(f"\n📝 Processing: {filepath}")
    
    if not os.path.exists(filepath):
        print(f"   ⚠️  File not found: {filepath}")
        return
    
    # Read file
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    changes_made = 0
    
    # Replace each color
    for old_color, new_color in COLOR_MAPPINGS.items():
        # Case-insensitive replacement
        pattern = re.compile(re.escape(old_color), re.IGNORECASE)
        matches = len(pattern.findall(content))
        if matches > 0:
            content = pattern.sub(new_color, content)
            print(f"   ✅ Replaced {matches}x: {old_color} → {new_color}")
            changes_made += matches
    
    # Write back if changes were made
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"   💾 Saved {changes_made} changes")
    else:
        print(f"   ℹ️  No changes needed")

def main():
    """Main function"""
    print("🎨 MDFDP Color Standardization")
    print("=" * 50)
    print("Converting all pages to purple theme...")
    
    # Get base directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Update each file
    for filepath in FILES_TO_UPDATE:
        full_path = os.path.join(base_dir, filepath)
        update_colors_in_file(full_path)
    
    print("\n" + "=" * 50)
    print("✅ Color standardization complete!")
    print("\n📋 Summary:")
    print("   - Primary color: #8876f8 (Purple)")
    print("   - Background: #000000 (Black)")
    print("   - Text: #e6e6e6 (Light gray)")
    print("\n💡 Tip: Restart your Flask app to see changes")

if __name__ == '__main__':
    main()
