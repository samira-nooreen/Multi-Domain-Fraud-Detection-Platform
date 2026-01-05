#!/usr/bin/env python3
# Read original file
with open('static/style.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Keep everything up to line 1146 (before the outer 768px media query)
kept_lines = lines[:1146]

# Append the clean About, FAQ, and Footer sections with proper structure
extra_css = '''
/* About Section Styling */
.about-section {
  margin: 80px 0;
  padding: 80px 40px;
  background: linear-gradient(135deg, rgba(136, 118, 248, 0.08) 0%, rgba(112, 89, 210, 0.08) 100%);
  position: relative;
  overflow: hidden;
}

.about-section::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -10%;
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, rgba(136, 118, 248, 0.1) 0%, transparent 70%);
  border-radius: 50%;
  pointer-events: none;
}

.about-container {
  max-width: 1200px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

.about-header {
  text-align: center;
  margin-bottom: 70px;
}

.about-section h2 {
  font-size: 2.8rem;
  font-weight: 800;
  margin: 0 0 15px 0;
  color: #fff;
  letter-spacing: -0.5px;
  background: linear-gradient(135deg, #fff 0%, #c9baff 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.about-subtitle {
  text-align: center;
  font-size: 1.3rem;
  color: #8876f8;
  margin: 0;
  font-weight: 500;
}

.about-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 30px;
  margin-bottom: 70px;
}

.card-icon-wrapper {
  width: 70px;
  height: 70px;
  background: rgba(136, 118, 248, 0.15);
  border-radius: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
  transition: all 0.3s ease;
}

.about-card:hover .card-icon-wrapper {
  background: rgba(136, 118, 248, 0.3);
  transform: scale(1.15);
}

.about-card {
  background: rgba(20, 20, 27, 0.7);
  backdrop-filter: blur(10px);
  padding: 35px 25px;
  border-radius: 14px;
  border: 1px solid rgba(136, 118, 248, 0.25);
  transition: all 0.4s ease;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.about-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(136, 118, 248, 0.15), transparent);
  transition: left 0.6s ease;
}

.about-card:hover::before {
  left: 100%;
}

.about-card:hover {
  border-color: #8876f8;
  box-shadow: 0 10px 40px rgba(136, 118, 248, 0.3);
  transform: translateY(-8px);
}

.about-card i {
  font-size: 2.5rem;
  color: #8876f8;
  transition: transform 0.3s ease;
}

.about-card:hover i {
  transform: scale(1.2) rotate(10deg);
}

.about-card h3 {
  font-size: 1.3rem;
  color: #fff;
  margin: 0 0 15px 0;
  font-weight: 700;
}

.about-card p {
  color: #b7b3c9;
  line-height: 1.6;
  font-size: 0.95rem;
  margin: 0;
}

.about-features {
  background: linear-gradient(135deg, rgba(13, 13, 15, 0.95) 0%, rgba(20, 20, 27, 0.95) 100%);
  padding: 50px;
  border-radius: 16px;
  border: 1px solid rgba(136, 118, 248, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.features-header {
  margin-bottom: 40px;
  text-align: center;
}

.about-features h3 {
  font-size: 1.8rem;
  color: #fff;
  margin: 0 0 10px 0;
  font-weight: 700;
}

.features-header p {
  font-size: 1.1rem;
  color: #8876f8;
  margin: 0;
}

.about-features ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 25px;
}

.about-features li {
  padding: 0;
  color: #b7b3c9;
  font-size: 1.05rem;
  display: flex;
  align-items: flex-start;
  gap: 15px;
  line-height: 1.6;
}

.feature-badge {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  background: linear-gradient(135deg, #8876f8 0%, #7059d2 100%);
  border-radius: 50%;
  color: white;
  font-weight: 700;
  font-size: 1.1rem;
  flex-shrink: 0;
  margin-top: 2px;
}

.about-features strong {
  color: #c9baff;
  font-weight: 700;
}

/* Responsive About Section */
@media (max-width: 1024px) {
  .about-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 25px;
  }

  .about-features ul {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .about-section {
    margin: 60px 0;
    padding: 50px 20px;
  }

  .about-section::before {
    width: 300px;
    height: 300px;
    right: -5%;
    top: -25%;
  }

  .about-header {
    margin-bottom: 40px;
  }

  .about-section h2 {
    font-size: 2rem;
    margin-bottom: 10px;
  }

  .about-subtitle {
    font-size: 1.1rem;
  }

  .about-grid {
    grid-template-columns: 1fr;
    gap: 20px;
    margin-bottom: 40px;
  }

  .about-card {
    padding: 25px 20px;
  }

  .about-card h3 {
    font-size: 1.2rem;
  }

  .about-features {
    padding: 30px 20px;
  }

  .features-header {
    margin-bottom: 25px;
  }

  .about-features h3 {
    font-size: 1.4rem;
  }

  .about-features ul {
    grid-template-columns: 1fr;
    gap: 15px;
  }

  .about-features li {
    gap: 12px;
  }
}

/* FAQ Section Styling */
.faq-section {
  max-width: 900px;
  margin: 80px auto;
  padding: 0 40px;
}

.faq-section h2 {
  text-align: center;
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 50px;
  color: #fff;
}

.faq-container {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.faq-item {
  position: relative;
}

.faq-item input[type="checkbox"] {
  display: none;
}

.faq-question {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  background: #14141b;
  border: 1px solid #2a2a35;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 1.1rem;
  font-weight: 600;
  color: #e6e6e6;
  user-select: none;
}

.faq-question:hover {
  background: #1f1f28;
  border-color: #8876f8;
}

.faq-icon {
  font-size: 1.5rem;
  color: #8876f8;
  transition: transform 0.3s ease;
  min-width: 30px;
  text-align: right;
}

.faq-item input[type="checkbox"]:checked + .faq-question {
  background: linear-gradient(135deg, #8876f870 0%, #7059d270 100%);
  border-color: #8876f8;
  box-shadow: 0 0 15px rgba(136, 118, 248, 0.3);
}

.faq-item input[type="checkbox"]:checked + .faq-question .faq-icon {
  transform: rotate(45deg);
}

.faq-answer {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease, padding 0.3s ease;
  background: transparent;
}

.faq-item input[type="checkbox"]:checked ~ .faq-answer {
  max-height: 400px;
  padding: 0 24px 20px 24px;
}

.faq-answer p {
  margin: 0;
  color: #b7b3c9;
  font-size: 1rem;
  line-height: 1.6;
  font-weight: 400;
}

/* Responsive FAQ */
@media (max-width: 768px) {
  .faq-section {
    margin: 60px auto;
    padding: 0 20px;
  }

  .faq-section h2 {
    font-size: 2rem;
    margin-bottom: 30px;
  }

  .faq-question {
    padding: 16px 18px;
    font-size: 1rem;
  }
}

/* Responsive Footer */
@media (max-width: 1024px) {
  .footer-content {
    grid-template-columns: 1fr;
    gap: 40px;
  }

  .footer-links-group {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .footer {
    padding: 40px 20px 20px;
  }

  .footer-links-group {
    grid-template-columns: 1fr;
    gap: 30px;
  }

  .footer-bottom {
    flex-direction: column;
    text-align: center;
  }
}
'''

kept_lines.append(extra_css)

# Write back
with open('static/style.css', 'w', encoding='utf-8') as f:
    f.writelines(kept_lines)

print(f"Successfully rebuilt CSS file!")
print(f"Original file had nested sections, now cleaned up.")
