# Frontend Testing Guide

## Quick Test Steps

### 1. Start Development Server
```bash
cd frontend
npm run dev
```

### 2. Open Browser
Navigate to: http://localhost:5173

### 3. Test Responsive Design

#### Mobile View (< 768px)
1. Press F12 to open DevTools
2. Click the device toolbar icon (or Ctrl+Shift+M)
3. Select "iPhone 12 Pro" or set width to 390px
4. Check:
   - ✅ Bottom navigation visible (5 icons)
   - ✅ Top bar with menu and avatar
   - ✅ Dashboard stats in single column
   - ✅ Inventory shows as cards (not table)
   - ✅ Buttons are full-width
   - ✅ No horizontal scrolling

#### Tablet View (768px - 1023px)
1. Set width to 768px
2. Check:
   - ✅ Sidebar visible on left
   - ✅ No bottom navigation
   - ✅ Dashboard stats in 2 columns
   - ✅ Inventory shows as table
   - ✅ Charts side-by-side

#### Desktop View (1024px+)
1. Set width to 1280px
2. Check:
   - ✅ Sidebar visible on left
   - ✅ Dashboard stats in 5 columns
   - ✅ Inventory table fully visible
   - ✅ Hover effects work
   - ✅ All features accessible

### 4. Test Navigation

#### Mobile
- Tap bottom nav icons
- Verify page changes
- Check top bar updates

#### Desktop
- Click sidebar links
- Verify active state
- Check hover effects

### 5. Test Features

#### Dashboard
- ✅ Stats cards display
- ✅ Chart renders
- ✅ Low stock items show

#### Inventory
- ✅ Search bar works
- ✅ Add button opens modal
- ✅ Table/cards display data
- ✅ Edit/Delete buttons work
- ✅ Modal form submits

## Common Issues & Fixes

### Issue: CSS not loading
**Symptoms**: No styling, plain HTML
**Fix**: 
```bash
# Check if app.css exists
ls frontend/src/styles/app.css

# Verify import in main.jsx
cat frontend/src/main.jsx | grep "app.css"

# Restart dev server
npm run dev
```

### Issue: Bottom nav not showing
**Symptoms**: No navigation on mobile
**Fix**: 
- Resize browser to < 768px
- Bottom nav only shows on mobile
- Check DevTools console for errors

### Issue: Sidebar not showing
**Symptoms**: No sidebar on desktop
**Fix**:
- Resize browser to ≥ 768px
- Sidebar only shows on desktop
- Check CSS media queries

### Issue: Tables not converting to cards
**Symptoms**: Horizontal scroll on mobile
**Fix**:
- Check both `.data-table` and `.data-cards` exist
- Verify CSS media queries
- Check browser width < 768px

### Issue: Blank page
**Symptoms**: White screen, no content
**Fix**:
```bash
# Check console for errors
# Press F12 → Console tab

# Common fixes:
npm install
npm run dev

# Clear cache
Ctrl+Shift+R (hard refresh)
```

## Browser Console Commands

```javascript
// Check if CSS loaded
console.log(getComputedStyle(document.body).getPropertyValue('--primary'));

// Check viewport width
console.log(window.innerWidth);

// Check if mobile nav exists
console.log(document.querySelector('.mobile-bottom-nav'));

// Check if sidebar exists
console.log(document.querySelector('.desktop-sidebar'));
```

## Expected Behavior

### Mobile (< 768px)
```
┌─────────────────────────────┐
│  ☰  Tire Shop         👤    │ ← Top Bar
├─────────────────────────────┤
│                             │
│  Dashboard                  │
│                             │
│  ┌───────────────────────┐  │
│  │ 💰 Today's Sales      │  │
│  │ ₹1,234                │  │
│  └───────────────────────┘  │
│                             │
│  (More stats...)            │
│                             │
├─────────────────────────────┤
│ 🏠  📦  🛒  💰  📊         │ ← Bottom Nav
└─────────────────────────────┘
```

### Desktop (≥ 768px)
```
┌──────┬──────────────────────┐
│ 🚗   │  Dashboard           │
│ Tire │                      │
│ Shop │  ┌───┬───┬───┬───┐  │
│      │  │ 1 │ 2 │ 3 │ 4 │  │
│ 📊   │  └───┴───┴───┴───┘  │
│ 📦   │                      │
│ 🛒   │  ┌────────┬────────┐ │
│ 💰   │  │ Chart  │ Items  │ │
│ 📈   │  └────────┴────────┘ │
│      │                      │
│ 👤   │                      │
└──────┴──────────────────────┘
```

## Performance Checks

### Load Time
- Initial load: < 2 seconds
- Page transitions: < 500ms
- Smooth animations: 60fps

### Bundle Size
```bash
npm run build
# Check dist/ folder size
# CSS should be ~15KB
# Total bundle < 500KB
```

### Lighthouse Score
1. Open DevTools
2. Go to Lighthouse tab
3. Run audit
4. Target scores:
   - Performance: 90+
   - Accessibility: 90+
   - Best Practices: 90+
   - SEO: 90+
   - PWA: 100

## Debugging Tips

### Enable Verbose Logging
```javascript
// Add to main.jsx temporarily
console.log('App starting...');
console.log('CSS loaded:', !!document.querySelector('style'));
```

### Check Network Tab
1. Open DevTools → Network
2. Reload page
3. Check:
   - app.css loads (200 status)
   - No 404 errors
   - Fast load times

### Check Elements Tab
1. Open DevTools → Elements
2. Inspect body element
3. Check:
   - CSS classes applied
   - Styles computed correctly
   - No inline style conflicts

## Success Criteria

✅ All pages load without errors
✅ Responsive design works on all sizes
✅ Navigation functions correctly
✅ Forms submit successfully
✅ Modals open and close
✅ No console errors
✅ No console warnings
✅ Smooth animations
✅ Fast load times

## Next Steps After Testing

1. ✅ Verify all features work
2. ✅ Test on real devices
3. ✅ Update remaining pages
4. ✅ Build for production
5. ✅ Deploy to hosting
6. ✅ Test PWA installation

---

**Need Help?**
- Check `IMPLEMENTATION_COMPLETE.md` for status
- Check `RESPONSIVE_REDESIGN_GUIDE.md` for patterns
- Check `QUICK_REFERENCE.md` for CSS classes
