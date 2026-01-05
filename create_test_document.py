"""
Create a sample test document for document forgery detection
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_test_document():
    """Create a sample document for testing"""
    
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
    draw.text((50, 35), "OFFICIAL CERTIFICATE", fill='white', font=title_font)
    
    # Document details
    draw.text((50, 130), "Certificate ID: CERT-12345", fill='black', font=text_font)
    draw.text((50, 170), "Issue Date: 15/11/2024", fill='black', font=text_font)
    draw.text((50, 210), "Issued To: John Doe", fill='black', font=text_font)
    
    # Content
    y_pos = 280
    content_lines = [
        "This is to certify that the above-mentioned person",
        "has successfully completed the required training",
        "and is hereby awarded this certificate of completion.",
        "",
        "Valid for: 2 years from date of issue",
        "Certificate Number: 2024-CERT-001",
    ]
    
    for line in content_lines:
        draw.text((50, y_pos), line, fill='black', font=small_font)
        y_pos += 35
    
    # Signature area
    draw.rectangle([(50, 600), (350, 700)], outline='black', width=2)
    draw.text((60, 610), "Authorized Signature:", fill='black', font=small_font)
    
    # Simulated signature
    points = [(100 + i*2, 660 + (i % 10 - 5)) for i in range(100)]
    draw.line(points, fill='blue', width=2)
    
    # Official stamp
    draw.ellipse([(500, 600), (700, 800)], outline='red', width=3)
    draw.text((550, 680), "OFFICIAL\nSTAMP", fill='red', font=small_font, align='center')
    
    # Footer
    draw.line([(50, 850), (750, 850)], fill='gray', width=1)
    draw.text((50, 870), "This is an official document. Any alteration is punishable by law.", 
             fill='gray', font=small_font)
    
    # Save
    os.makedirs('test_documents', exist_ok=True)
    img.save('test_documents/sample_certificate.png')
    print("✅ Created: test_documents/sample_certificate.png")
    
    return img

def create_forged_test_document():
    """Create a forged version for comparison"""
    
    # Start with genuine document
    img = create_test_document()
    
    # Add forgery: Alter the date
    draw = ImageDraw.Draw(img)
    try:
        text_font = ImageFont.truetype("arial.ttf", 22)  # Slightly different size
    except:
        text_font = ImageFont.load_default()
    
    # White out original date
    draw.rectangle([(50, 170), (400, 200)], fill='white')
    # Write altered date with different font
    draw.text((52, 172), "Issue Date: 25/12/2024", fill='#1a1a1a', font=text_font)
    
    # Save
    img.save('test_documents/forged_certificate.png')
    print("✅ Created: test_documents/forged_certificate.png")
    
    return img

if __name__ == "__main__":
    print("\nCreating test documents...\n")
    create_test_document()
    create_forged_test_document()
    print("\n✅ Test documents ready in test_documents/ folder")
    print("\nYou can use these to test the document forgery detection:")
    print("  - sample_certificate.png (genuine)")
    print("  - forged_certificate.png (altered date)")
