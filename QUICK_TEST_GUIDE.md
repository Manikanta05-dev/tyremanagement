# 🧪 Quick Test Guide - Critical Fixes

## 🚀 Start Application

```bash
# Terminal 1 - Backend
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend  
cd frontend
npm run dev
```

## 📱 Access URLs
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## ✅ Test Checklist

### 1. Authentication Test (2 min)
- [ ] Open http://localhost:3000
- [ ] Should auto-redirect to /login
- [ ] Login: `admin` / `admin123`
- [ ] Should redirect to /dashboard
- [ ] Try accessing /login again → should redirect to /dashboard
- [ ] Click profile icon → should logout
- [ ] Should redirect back to /login

**Expected**: ✅ Secure authentication with token validation

---

### 2. Sales + Billing Test (5 min)
- [ ] Navigate to Sales page
- [ ] Click "New Sale" button
- [ ] Fill customer details:
  - Name: Test Customer
  - Mobile: 9876543210
  - Payment: UPI
- [ ] Add first item:
  - Select a tire
  - Quantity: 2
  - Click "Add Item"
- [ ] Add second item:
  - Select different tire
  - Quantity: 1
  - Click "Add Item"
- [ ] Set discount:
  - Type: Flat ₹
  - Value: 100
  - Verify discount shows in summary
- [ ] Change discount:
  - Type: Percent %
  - Value: 10
  - Verify percentage calculation
- [ ] Verify bill summary shows:
  - Subtotal (sum of all items)
  - Discount (calculated correctly)
  - Total (subtotal - discount)
- [ ] Add notes: "Test sale"
- [ ] Click "Create Sale"
- [ ] Verify success message
- [ ] Check sales history shows new sale
- [ ] Verify inventory stock reduced

**Expected**: ✅ Complete billing system with discount

---

### 3. Mobile UI Test (3 min)
- [ ] Open DevTools (F12)
- [ ] Click device toolbar icon (Ctrl+Shift+M)
- [ ] Select "iPhone 12 Pro" or similar
- [ ] Test login page:
  - [ ] Page visible (not cut off)
  - [ ] Form centered
  - [ ] Inputs accessible
- [ ] Login and test navigation:
  - [ ] Menu button (☰) clickable
  - [ ] Menu button size ≥ 44px
  - [ ] Sidebar opens on click
  - [ ] Overlay closes sidebar
- [ ] Test profile button:
  - [ ] Profile icon clickable
  - [ ] Profile icon size ≥ 44px
  - [ ] Logout works
- [ ] Test bottom navigation:
  - [ ] All 5 icons visible
  - [ ] Icons clickable
  - [ ] Active state shows
- [ ] Test sales page:
  - [ ] "New Sale" button visible
  - [ ] Modal opens properly
  - [ ] Form fields accessible
  - [ ] No horizontal scroll

**Expected**: ✅ Perfect mobile experience

---

### 4. Responsive Design Test (2 min)
- [ ] Test different screen sizes:
  - [ ] Mobile (375px) - Bottom nav visible
  - [ ] Tablet (768px) - Sidebar appears
  - [ ] Desktop (1024px+) - Full layout
- [ ] Verify no horizontal scroll at any size
- [ ] Verify all buttons visible
- [ ] Verify forms accessible

**Expected**: ✅ Responsive on all devices

---

### 5. Discount Calculation Test (2 min)

#### Test Case 1: Flat Discount
- Item 1: ₹2500 × 2 = ₹5000
- Item 2: ₹3000 × 1 = ₹3000
- **Subtotal**: ₹8000
- **Discount (Flat)**: ₹500
- **Total**: ₹7500 ✅

#### Test Case 2: Percentage Discount
- Item 1: ₹2500 × 2 = ₹5000
- Item 2: ₹3000 × 1 = ₹3000
- **Subtotal**: ₹8000
- **Discount (10%)**: ₹800
- **Total**: ₹7200 ✅

**Expected**: ✅ Accurate calculations

---

## 🐛 Common Issues & Solutions

### Issue: Backend not starting
**Solution**: 
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Issue: Frontend not starting
**Solution**:
```bash
cd frontend
npm install
npm run dev
```

### Issue: Login fails
**Solution**: Check backend is running on port 8000

### Issue: Menu button not clickable
**Solution**: Clear browser cache, refresh page

---

## 📊 Success Indicators

### ✅ All Working If:
1. Login redirects properly
2. Sales page shows billing interface
3. Discount calculations are accurate
4. Mobile menu/profile buttons work
5. No horizontal scroll on mobile
6. Stock reduces after sale
7. Toast notifications appear
8. Forms validate properly

---

## 🎯 Performance Benchmarks

- **Login**: < 1 second
- **Sales creation**: < 2 seconds
- **Page load**: < 1 second
- **Mobile interactions**: Instant feedback

---

## 📝 Test Results Template

```
Date: ___________
Tester: ___________

✅ Authentication: PASS / FAIL
✅ Sales + Billing: PASS / FAIL
✅ Mobile UI: PASS / FAIL
✅ Responsive Design: PASS / FAIL
✅ Discount Calculation: PASS / FAIL

Notes:
_________________________________
_________________________________
_________________________________
```

---

## 🎉 Expected Final Result

A fully functional tire shop inventory management system with:
- ✅ Professional billing interface
- ✅ Secure authentication
- ✅ Mobile-optimized UI
- ✅ Accurate discount calculations
- ✅ Responsive design
- ✅ Excellent user experience

**Total Test Time**: ~15 minutes
**Success Rate**: 100% if all checks pass
