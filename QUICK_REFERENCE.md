# Quick Reference Card

## 🎨 CSS Classes Cheat Sheet

### Layout
```jsx
<div className="page-container">        // Main page wrapper
<div className="page-header">           // Page header section
<h1 className="page-title">             // Page title
```

### Cards
```jsx
<div className="card">                  // Basic card
<div className="stat-card">             // Dashboard stat card
<div className="data-card">             // Mobile data card
```

### Buttons
```jsx
<button className="btn btn-primary">    // Primary button
<button className="btn btn-success">    // Success button
<button className="btn btn-danger">     // Danger button
<button className="btn btn-outline">    // Outline button
<button className="btn btn-full">       // Full width
```

### Forms
```jsx
<div className="form-group">            // Form field wrapper
<label className="form-label">          // Form label
<input className="form-input">          // Text input
<select className="form-select">        // Select dropdown
```

### Tables (Responsive)
```jsx
// Desktop
<table className="data-table">
  <thead><tr><th>Column</th></tr></thead>
  <tbody><tr><td>Data</td></tr></tbody>
</table>

// Mobile
<div className="data-cards">
  <div className="data-card">
    <div className="data-card-row">
      <span className="data-card-label">Label</span>
      <span className="data-card-value">Value</span>
    </div>
  </div>
</div>
```

### Modals
```jsx
<div className="modal-overlay">
  <div className="modal-content">
    <div className="modal-header">
      <h2 className="modal-title">Title</h2>
    </div>
    <div className="modal-body">Content</div>
    <div className="modal-footer">Buttons</div>
  </div>
</div>
```

### Badges
```jsx
<span className="badge badge-primary">   // Blue badge
<span className="badge badge-success">   // Green badge
<span className="badge badge-warning">   // Yellow badge
<span className="badge badge-error">     // Red badge
```

## 📱 Responsive Breakpoints

```css
/* Mobile (default) */
/* 0px - 767px */

/* Tablet & Desktop */
@media (min-width: 768px) { }

/* Desktop */
@media (min-width: 1024px) { }

/* Large Desktop */
@media (min-width: 1280px) { }
```

## 🎯 Common Patterns

### Page Structure
```jsx
function MyPage() {
  return (
    <div className="page-container">
      <div className="page-header">
        <h1 className="page-title">Page Title</h1>
      </div>
      
      <div className="card">
        {/* Content */}
      </div>
    </div>
  )
}
```

### Stats Grid
```jsx
<div className="stats-grid">
  <div className="stat-card">
    <div className="stat-content">
      <p className="stat-label">Label</p>
      <p className="stat-value">₹1,234</p>
    </div>
    <div className="stat-icon">💰</div>
  </div>
</div>
```

### Form with Buttons
```jsx
<form onSubmit={handleSubmit}>
  <div className="form-group">
    <label className="form-label">Name</label>
    <input className="form-input" type="text" />
  </div>
  
  <div className="flex gap-2">
    <button type="submit" className="btn btn-primary btn-full">
      Save
    </button>
    <button type="button" className="btn btn-outline btn-full">
      Cancel
    </button>
  </div>
</form>
```

### Search Bar
```jsx
<div className="search-bar">
  <svg className="search-icon" width="20" height="20">
    <path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
  </svg>
  <input 
    type="text"
    className="search-input"
    placeholder="Search..."
  />
</div>
```

## 🔧 Utility Classes

```jsx
// Text
className="text-center"      // Center text
className="text-right"       // Right align
className="font-bold"        // Bold
className="font-semibold"    // Semi-bold
className="text-sm"          // Small text
className="text-xs"          // Extra small

// Spacing
className="mt-2"             // Margin top
className="mb-4"             // Margin bottom

// Flexbox
className="flex"             // Display flex
className="flex-col"         // Flex column
className="items-center"     // Align center
className="justify-between"  // Space between
className="gap-2"            // Gap spacing
```

## 📦 File Structure

```
frontend/
├── public/
│   ├── manifest.json          ← PWA manifest
│   ├── service-worker.js      ← Offline support
│   └── icons/                 ← App icons (create these)
├── src/
│   ├── components/
│   │   └── Layout.jsx         ← New responsive layout
│   ├── pages/
│   │   ├── Dashboard.jsx      ← Update with new classes
│   │   ├── Inventory.jsx      ← Update with new classes
│   │   └── ...
│   ├── styles/
│   │   └── app.css            ← New CSS file
│   └── main.jsx               ← Updated import
└── index.html                 ← PWA meta tags
```

## 🚀 Quick Commands

```bash
# Development
npm run dev

# Build
npm run build

# Preview build
npm run preview

# Test PWA
npm run build && npm run preview
```

## 📱 Testing URLs

```
Mobile:   http://localhost:5173
Desktop:  http://localhost:5173
PWA Test: http://localhost:4173 (after build)
```

## ✅ Testing Checklist

### Mobile (< 768px)
- [ ] Bottom nav visible
- [ ] Top bar shows
- [ ] Tables → Cards
- [ ] Buttons full-width
- [ ] Touch targets 44px+

### Desktop (≥ 768px)
- [ ] Sidebar visible
- [ ] No bottom nav
- [ ] Tables show
- [ ] Multi-column layouts
- [ ] Hover effects work

### PWA
- [ ] Manifest loads
- [ ] Service worker registers
- [ ] Install prompt shows
- [ ] Offline mode works
- [ ] Icons display

## 🎨 Color Variables

```css
--primary: #1e40af
--secondary: #3b82f6
--success: #10b981
--warning: #f59e0b
--error: #ef4444
--bg-primary: #f5f7fa
--text-primary: #1f2937
```

## 📞 Quick Help

**Layout not responsive?**
→ Check media queries in app.css

**Bottom nav not showing?**
→ Only shows on mobile (< 768px)

**PWA not installing?**
→ Requires HTTPS (except localhost)

**Icons missing?**
→ Generate using generate-icons.html

**Styles not applying?**
→ Check import in main.jsx

## 🔗 Important Files

1. **Layout.jsx** - Navigation structure
2. **app.css** - All styles
3. **manifest.json** - PWA config
4. **service-worker.js** - Offline support

## 💡 Pro Tips

1. **Mobile First**: Design for mobile, enhance for desktop
2. **Test Early**: Check responsive behavior frequently
3. **Use Classes**: Don't write inline styles
4. **Touch Targets**: Minimum 44px for mobile
5. **PWA Icons**: Generate all sizes for best experience

---

**Need More Help?**
- See `RESPONSIVE_REDESIGN_GUIDE.md` for detailed integration
- See `PWA_SETUP_GUIDE.md` for PWA setup
- See `REDESIGN_SUMMARY.md` for complete overview
