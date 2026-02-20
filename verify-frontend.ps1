# Frontend Verification Script

Write-Host "🔍 Verifying Frontend Setup..." -ForegroundColor Cyan
Write-Host ""

$errors = 0
$warnings = 0

# Check if frontend directory exists
if (Test-Path "frontend") {
    Write-Host "✓ Frontend directory exists" -ForegroundColor Green
} else {
    Write-Host "✗ Frontend directory not found" -ForegroundColor Red
    $errors++
}

# Check if node_modules exists
if (Test-Path "frontend/node_modules") {
    Write-Host "✓ Node modules installed" -ForegroundColor Green
} else {
    Write-Host "⚠ Node modules not found - Run: cd frontend; npm install" -ForegroundColor Yellow
    $warnings++
}

# Check critical files
$criticalFiles = @(
    "frontend/src/main.jsx",
    "frontend/src/App.jsx",
    "frontend/src/components/Layout.jsx",
    "frontend/src/styles/app.css",
    "frontend/public/manifest.json",
    "frontend/public/service-worker.js",
    "frontend/index.html"
)

Write-Host ""
Write-Host "📁 Checking Critical Files:" -ForegroundColor Cyan

foreach ($file in $criticalFiles) {
    if (Test-Path $file) {
        Write-Host "  ✓ $file" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $file MISSING" -ForegroundColor Red
        $errors++
    }
}

# Check if icons exist
Write-Host ""
Write-Host "🎨 Checking PWA Icons:" -ForegroundColor Cyan

$iconSizes = @(72, 96, 128, 144, 152, 192, 384, 512)
$iconsExist = 0

foreach ($size in $iconSizes) {
    if (Test-Path "frontend/public/icons/icon-${size}x${size}.svg") {
        $iconsExist++
    }
}

if ($iconsExist -eq 8) {
    Write-Host "  ✓ All 8 icons generated" -ForegroundColor Green
} elseif ($iconsExist -gt 0) {
    Write-Host "  ⚠ Only $iconsExist/8 icons found" -ForegroundColor Yellow
    $warnings++
} else {
    Write-Host "  ✗ No icons found" -ForegroundColor Red
    $errors++
}

# Check main.jsx imports
Write-Host ""
Write-Host "📦 Checking Imports:" -ForegroundColor Cyan

$mainContent = Get-Content "frontend/src/main.jsx" -Raw
if ($mainContent -match "import.*app\.css") {
    Write-Host "  ✓ app.css imported in main.jsx" -ForegroundColor Green
} else {
    Write-Host "  ✗ app.css not imported in main.jsx" -ForegroundColor Red
    $errors++
}

# Check if pages are updated
Write-Host ""
Write-Host "📄 Checking Updated Pages:" -ForegroundColor Cyan

$dashboardContent = Get-Content "frontend/src/pages/Dashboard.jsx" -Raw
if ($dashboardContent -match "page-container") {
    Write-Host "  ✓ Dashboard.jsx updated" -ForegroundColor Green
} else {
    Write-Host "  ⚠ Dashboard.jsx not updated yet" -ForegroundColor Yellow
    $warnings++
}

$inventoryContent = Get-Content "frontend/src/pages/Inventory.jsx" -Raw
if ($inventoryContent -match "data-cards") {
    Write-Host "  ✓ Inventory.jsx updated" -ForegroundColor Green
} else {
    Write-Host "  ⚠ Inventory.jsx not updated yet" -ForegroundColor Yellow
    $warnings++
}

# Summary
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host ""

if ($errors -eq 0 -and $warnings -eq 0) {
    Write-Host "✅ All checks passed! Ready to start development." -ForegroundColor Green
    Write-Host ""
    Write-Host "🚀 Next Steps:" -ForegroundColor Cyan
    Write-Host "  1. cd frontend" -ForegroundColor White
    Write-Host "  2. npm run dev" -ForegroundColor White
    Write-Host "  3. Open http://localhost:5173" -ForegroundColor White
} elseif ($errors -eq 0) {
    Write-Host "⚠️  Setup complete with $warnings warning(s)" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "🚀 You can start development:" -ForegroundColor Cyan
    Write-Host "  cd frontend && npm run dev" -ForegroundColor White
} else {
    Write-Host "❌ Found $errors error(s) and $warnings warning(s)" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please fix the errors above before continuing." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "📚 Documentation:" -ForegroundColor Cyan
Write-Host "  - TEST_FRONTEND.md - Testing guide" -ForegroundColor White
Write-Host "  - IMPLEMENTATION_COMPLETE.md - Current status" -ForegroundColor White
Write-Host "  - QUICK_REFERENCE.md - CSS classes" -ForegroundColor White
Write-Host ""
