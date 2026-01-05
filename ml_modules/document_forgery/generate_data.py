"""
Document Forgery Detection - Realistic Dataset Generator
Generates synthetic document images with genuine and forged characteristics
"""
import numpy as np
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random

def generate_realistic_documents(n_genuine=200, n_forged=200):
    """
    Generate realistic document images
    - Genuine: Clean, consistent formatting, proper alignment
    - Forged: Altered text, inconsistent fonts, compression artifacts, misalignment
    """
    print(f"Generating {n_genuine} genuine + {n_forged} forged documents...")
    
    os.makedirs('doc_data/genuine', exist_ok=True)
    os.makedirs('doc_data/forged', exist_ok=True)
    
    # Generate genuine documents
    for i in range(n_genuine):
        img = create_genuine_document(i)
        img.save(f'doc_data/genuine/doc_{i:04d}.png')
        
    print(f"✓ Generated {n_genuine} genuine documents")
    
    # Generate forged documents
    for i in range(n_forged):
        img = create_forged_document(i)
        img.save(f'doc_data/forged/doc_{i:04d}.png')
        
    print(f"✓ Generated {n_forged} forged documents")
    print(f"✅ Total: {n_genuine + n_forged} documents in doc_data/")

def create_genuine_document(seed):
    """Create a genuine-looking document"""
    random.seed(seed)
    np.random.seed(seed)
    
    # Document size
    width, height = 800, 1000
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    # Try to load a font, fallback to default
    try:
        title_font = ImageFont.truetype("arial.ttf", 32)
        text_font = ImageFont.truetype("arial.ttf", 20)
        small_font = ImageFont.truetype("arial.ttf", 16)
    except:
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Header
    draw.rectangle([(0, 0), (width, 100)], fill='#2c3e50')
    draw.text((50, 35), "OFFICIAL DOCUMENT", fill='white', font=title_font)
    
    # Document ID
    doc_id = f"DOC-{random.randint(10000, 99999)}"
    draw.text((50, 130), f"Document ID: {doc_id}", fill='black', font=text_font)
    
    # Date
    date = f"{random.randint(1, 28)}/{random.randint(1, 12)}/202{random.randint(0, 4)}"
    draw.text((50, 170), f"Issue Date: {date}", fill='black', font=text_font)
    
    # Content lines (consistent formatting)
    y_pos = 230
    for i in range(10):
        line = f"Line {i+1}: This is genuine content with consistent formatting."
        draw.text((50, y_pos), line, fill='black', font=small_font)
        y_pos += 30
    
    # Signature area
    draw.rectangle([(50, 600), (350, 700)], outline='black', width=2)
    draw.text((60, 610), "Authorized Signature:", fill='black', font=small_font)
    
    # Simulated signature (curved line)
    points = [(100 + i*2, 660 + random.randint(-5, 5)) for i in range(100)]
    draw.line(points, fill='blue', width=2)
    
    # Official stamp (circle)
    draw.ellipse([(500, 600), (700, 800)], outline='red', width=3)
    draw.text((550, 680), "OFFICIAL\nSTAMP", fill='red', font=small_font)
    
    # Footer
    draw.text((50, 920), "This is a genuine document.", fill='gray', font=small_font)
    
    return img

def create_forged_document(seed):
    """Create a forged document with telltale signs"""
    random.seed(seed + 1000)  # Different seed
    np.random.seed(seed + 1000)
    
    # Start with a genuine document
    img = create_genuine_document(seed)
    
    # Apply forgery techniques
    forgery_type = random.choice(['altered_text', 'copy_paste', 'compression', 'mixed_fonts'])
    
    if forgery_type == 'altered_text':
        # Overlay altered text (different font/color)
        draw = ImageDraw.Draw(img)
        try:
            altered_font = ImageFont.truetype("arial.ttf", 22)  # Slightly different size
        except:
            altered_font = ImageFont.load_default()
        
        # Overwrite some text with slightly different alignment
        draw.rectangle([(50, 170), (400, 200)], fill='white')  # White out original
        draw.text((52, 172), f"Issue Date: {random.randint(1, 28)}/{random.randint(1, 12)}/2024", 
                 fill='#1a1a1a', font=altered_font)  # Slightly different color
    
    elif forgery_type == 'copy_paste':
        # Copy-paste artifacts (duplicate signature)
        signature_area = img.crop((100, 650, 300, 680))
        img.paste(signature_area, (400, 650))  # Duplicate signature
    
    elif forgery_type == 'compression':
        # Add JPEG compression artifacts
        img = img.filter(ImageFilter.BLUR)
        # Add noise
        img_array = np.array(img)
        noise = np.random.randint(-20, 20, img_array.shape, dtype=np.int16)
        img_array = np.clip(img_array.astype(np.int16) + noise, 0, 255).astype(np.uint8)
        img = Image.fromarray(img_array)
    
    elif forgery_type == 'mixed_fonts':
        # Inconsistent fonts (sign of editing)
        draw = ImageDraw.Draw(img)
        try:
            wrong_font = ImageFont.truetype("arial.ttf", 18)
        except:
            wrong_font = ImageFont.load_default()
        
        # Add text with wrong font
        draw.rectangle([(50, 230), (600, 260)], fill='white')
        draw.text((50, 232), "Line 1: This text has inconsistent formatting.", 
                 fill='black', font=wrong_font)
    
    return img

if __name__ == "__main__":
    generate_realistic_documents(n_genuine=200, n_forged=200)
