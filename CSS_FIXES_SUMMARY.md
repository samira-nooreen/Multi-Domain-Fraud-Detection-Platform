# CSS Issues Fixed Summary

## Problem
The `style.css` file had missing CSS rules for elements used in `index.html`:
- Chatbot window and messages
- Top cities list
- News feed items
- FAQ answers

## Solution
I've added all the missing CSS rules to `static/style.css`:

### Added CSS Classes:
1. **Chatbot Styles:**
   - `.chatbot-window` - Fixed chatbot container
   - `.chatbot-header` - Header with gradient
   - `.chatbot-messages` - Message container
   - `.bot-message` / `.user-message` - Message bubbles
   - `.chatbot-input` - Input area styling
   - `.close-btn` - Close button

2. **Top Cities List:**
   - `.top-cities` - Container
   - `.top-cities-list` - List styling
   - `.critical`, `.high`, `.medium`, `.low` - Risk level dots

3. **News Feed:**
   - `.news-feed` - Container
   - `.news-items` - Items container
   - `.news-item` - Individual news item
   - `.news-header`, `.news-source`, `.news-time` - Header elements
   - `.news-badge.verified` - Verified badge

4. **FAQ Styles:**
   - `.faq-answer` - Collapsible answer
   - `.faq-item input:checked` - Checked state

5. **Footer Styles:**
   - Complete footer styling
   - Newsletter form
   - Responsive media queries

## Note
There appears to be some duplicate content in the CSS file now. You may want to review and clean up any duplicates.

## Recommendation
The HTML file (index.html) has JavaScript code mixed into the chatbot input section (lines 422-454). This should be moved to a proper `<script>` tag before the closing `</body>` tag.
