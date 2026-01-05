# How to See the 17 Cities on Analytics Map 🗺️

## Quick Fix - 3 Steps:

### Step 1: Test the Map Standalone
Open this file in your browser to verify the cities work:
```
test_17_cities_map.html
```
Just double-click it or drag it into your browser. You should see all 17 cities with different colors!

### Step 2: Clear Browser Cache
The issue is browser caching. Do ONE of these:

**Option A - Hard Refresh (Recommended):**
1. Go to `http://127.0.0.1:5000/analytics`
2. Press `Ctrl + Shift + R` (Windows) or `Cmd + Shift + R` (Mac)
3. This forces a fresh reload

**Option B - Clear Cache:**
1. Open browser DevTools (F12)
2. Right-click the refresh button
3. Select "Empty Cache and Hard Reload"

**Option C - Incognito Mode:**
1. Open an Incognito/Private window
2. Go to `http://127.0.0.1:5000/analytics`
3. Login and view the map

### Step 3: Restart Flask Server
Stop the current server (Ctrl+C) and restart:
```bash
py app.py
```

---

## What You Should See:

### 🔴 2 Red Markers (Critical):
- Mumbai (245 cases)
- Delhi (198 cases)

### 🟠 4 Orange Markers (High):
- Bangalore (156 cases)
- Hyderabad (134 cases)
- Ahmedabad (112 cases)
- Pune (98 cases)

### 🟡 5 Yellow Markers (Medium):
- Chennai (87 cases)
- Kolkata (76 cases)
- Surat (64 cases)
- Jaipur (58 cases)
- Lucknow (52 cases)

### 🟢 6 Green Markers (Low):
- Kanpur (43 cases)
- Nagpur (38 cases)
- Indore (35 cases)
- Bhopal (29 cases)
- Chandigarh (24 cases)
- Kochi (19 cases)
- Guwahati (15 cases)

---

## Troubleshooting:

### If you still don't see the cities:

1. **Check Browser Console:**
   - Press F12
   - Go to Console tab
   - Look for any errors
   - Should see: "Using static fraud data with 17 cities"

2. **Verify JavaScript File:**
   - The file `static/js/analytics.js` has been updated
   - Lines 56-82 contain all 17 cities

3. **Check Network Tab:**
   - Press F12
   - Go to Network tab
   - Refresh the page
   - Look for `analytics.js` - it should load the new version

4. **Try Different Browser:**
   - If Chrome doesn't work, try Firefox or Edge
   - Sometimes one browser caches more aggressively

---

## Why This Happened:

The browser cached the old JavaScript file. Even though we updated the code, your browser was still using the old version from memory. The fixes above force the browser to download the new file.

---

## Verification Checklist:

✅ Open `test_17_cities_map.html` - See 17 cities?
✅ Hard refresh analytics page (Ctrl+Shift+R)
✅ Check console for "17 cities" message
✅ Count the markers - should be 17 total
✅ See 4 different colors (red, orange, yellow, green)

If all ✅ are checked, you're good to go! 🎉
