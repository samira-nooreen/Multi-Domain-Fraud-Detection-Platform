# 🎨 Color Standardization Guide

### Primary Colors
```css
/* Main Purple */
--primary-purple: #8876f8;
--primary-purple-dark: #7059d2;
--primary-purple-light: #c9baff;
--primary-purple-lighter: #dabfff;
```

### Background Colors
```css
--bg-black: #000000;
--bg-dark: #0d0d0f;
--bg-card: #14141b;
--bg-secondary: #20202b;
```

### Text Colors
```css
--text-primary: #ffffff;
--text-secondary: #e6e6e6;
--text-muted: #b7b3c9;
```

---

## Color Replacements Needed

### ❌ REMOVE These Colors (Red/Pink Theme):
- `#ff1744` → Replace with `#8876f8`
- `#f50057` → Replace with `#c9baff`
- `#d50000` → Replace with `#7059d2`
- `#ff5252` → Replace with `#fa395f` (keep for critical alerts)
- `#0a0e27` → Replace with `#000000`
- `#1a1f3a` → Replace with `#0d0d0f`

### ✅ USE These Colors (Purple Theme):
- **Primary Actions**: `#8876f8`
- **Hover States**: `#7059d2`
- **Light Accents**: `#c9baff`
- **Backgrounds**: `#000000`, `#0d0d0f`, `#14141b`
- **Text**: `#e6e6e6`, `#b7b3c9`

---

## Quick Find & Replace

### For Analytics Dashboard (`analytics_dashboard.html`):
```
Find: #ff1744
Replace: #8876f8

Find: #f50057
Replace: #c9baff

Find: #d50000
Replace: #7059d2

Find: #0a0e27
Replace: #000000

Find: #1a1f3a
Replace: #0d0d0f

Find: #b0b0b0
Replace: #b7b3c9
```

### For Security Dashboard (`security_dashboard.html`):
```
Same replacements as above
```

---

## Gradient Patterns

### ❌ Old (Red):
```css
background: linear-gradient(135deg, #ff1744 0%, #f50057 100%);
background: linear-gradient(135deg, #ff1744 0%, #d50000 100%);
```

### ✅ New (Purple):
```css
background: linear-gradient(135deg, #8876f8 0%, #c9baff 100%);
background: linear-gradient(135deg, #8876f8 0%, #7059d2 100%);
```

---

## Button Styles

### ❌ Old:
```css
.back-btn {
    background: linear-gradient(135deg, #ff1744 0%, #d50000 100%);
}
```

### ✅ New:
```css
.back-btn {
    background: #8876f8;
}

.back-btn:hover {
    background: #7059d2;
}
```

---

## Border Colors

### ❌ Old:
```css
border-bottom: 1px solid rgba(255, 23, 68, 0.2);
```

### ✅ New:
```css
border-bottom: 1px solid rgba(136, 118, 248, 0.2);
```

---

## Shadow Effects

### ❌ Old:
```css
box-shadow: 0 10px 30px rgba(255, 23, 68, 0.2);
```

### ✅ New:
```css
box-shadow: 0 2px 24px 0 #8876f860;
```

---

## Status Colors (Keep These)

These are universal and should stay the same:
```css
--status-critical: #fa395f;  /* Red - for critical alerts */
--status-high: #fc8d26;      /* Orange - for high priority */
--status-medium: #fcea26;    /* Yellow - for medium priority */
--status-low: #22d168;       /* Green - for low priority */
```

---

## Files That Need Color Updates

1. ✅ **Homepage** (`index.html` + `style.css`) - Already correct!
2. ⚠️ **Analytics Dashboard** (`analytics_dashboard.html`) - Needs update
3. ⚠️ **Security Dashboard** (`security_dashboard.html`) - Needs update
4. ⚠️ **All Detection Module Pages** - Should match homepage

---

## Quick Visual Reference

### Homepage Colors (CORRECT):
- **Primary**: Purple (#8876f8)
- **Background**: Black (#000000)
- **Cards**: Dark (#0d0d0f, #14141b)
- **Text**: Light gray (#e6e6e6, #b7b3c9)
- **Buttons**: Purple (#8876f8) → Darker purple on hover (#7059d2)

### What to Avoid:
- ❌ Red/Pink (#ff1744, #f50057)
- ❌ Blue gradients (#0a0e27, #1a1f3a)
- ❌ Bright colors except for status indicators

---

## Implementation Steps

1. **Open each HTML file**
2. **Use Find & Replace** (Ctrl+H)
3. **Replace all red colors** with purple equivalents
4. **Test the page** to ensure it looks good
5. **Repeat for all pages**

---

## Expected Result

All pages should have:
- ✅ Same purple theme as homepage
- ✅ Black background
- ✅ Purple buttons and accents
- ✅ Consistent text colors
- ✅ Matching gradients and shadows

---

**Last Updated**: November 28, 2025
**Theme**: Purple/Violet (#8876f8)
**Status**: Ready to implement
