# PWA Setup Guide - Tire Shop Inventory Management

## Overview
This application is now configured as a Progressive Web App (PWA) that can be installed on mobile devices and desktops, providing an app-like experience.

## What's Been Implemented

### 1. PWA Manifest (`/public/manifest.json`)
- App name, description, and branding
- Theme colors matching the app design
- App icons in multiple sizes (72px to 512px)
- Standalone display mode (fullscreen app experience)
- App shortcuts for quick actions
- Screenshot placeholders for app stores

### 2. Service Worker (`/public/service-worker.js`)
- Offline caching strategy
- Network-first for API calls
- Cache-first for static assets
- Background sync support
- Push notification support (optional)

### 3. HTML Meta Tags
- PWA-specific meta tags
- Apple Touch Icon support
- Theme color for mobile browsers
- Viewport settings optimized for mobile

### 4. Responsive Layout
- Mobile-first design (360px+)
- Bottom navigation for mobile
- Sidebar navigation for desktop
- Adaptive layouts for all screen sizes

## Installation Instructions

### Step 1: Generate App Icons

You need to create app icons in the following sizes:
- 72x72, 96x96, 128x128, 144x144, 152x152, 192x192, 384x384, 512x512

**Option A: Use an online tool**
1. Go to https://www.pwabuilder.com/imageGenerator
2. Upload your logo (recommended: 512x512 PNG with transparent background)
3. Download the generated icons
4. Place them in `frontend/public/icons/` directory

**Option B: Use ImageMagick (command line)**
```bash
# Install ImageMagick first
# Then run these commands from your logo file:

convert logo.png -resize 72x72 frontend/public/icons/icon-72x72.png
convert logo.png -resize 96x96 frontend/public/icons/icon-96x96.png
convert logo.png -resize 128x128 frontend/public/icons/icon-128x128.png
convert logo.png -resize 144x144 frontend/public/icons/icon-144x144.png
convert logo.png -resize 152x152 frontend/public/icons/icon-152x152.png
convert logo.png -resize 192x192 frontend/public/icons/icon-192x192.png
convert logo.png -resize 384x384 frontend/public/icons/icon-384x384.png
convert logo.png -resize 512x512 frontend/public/icons/icon-512x512.png
```

### Step 2: Create Icons Directory
```bash
mkdir -p frontend/public/icons
```

### Step 3: Update Vite Config

Add to `frontend/vite.config.js`:
```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  build: {
    rollupOptions: {
      output: {
        manualChunks: undefined,
      },
    },
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
```

### Step 4: Build and Test

```bash
cd frontend
npm run build
npm run preview
```

Visit the preview URL and test PWA installation.

## Testing PWA Installation

### On Chrome Desktop:
1. Open the app in Chrome
2. Look for the install icon (⊕) in the address bar
3. Click "Install" to add to desktop

### On Chrome Android:
1. Open the app in Chrome
2. Tap the menu (⋮) → "Add to Home screen"
3. Confirm installation
4. App icon will appear on home screen

### On iOS Safari:
1. Open the app in Safari
2. Tap the Share button
3. Scroll down and tap "Add to Home Screen"
4. Confirm and the app will appear on home screen

## PWA Features

### ✅ Installable
- Can be installed on home screen
- Runs in standalone mode (no browser UI)
- Splash screen on launch

### ✅ Offline Support
- Static assets cached for offline use
- API responses cached
- Graceful degradation when offline

### ✅ App-like Experience
- No browser chrome in standalone mode
- Bottom navigation on mobile
- Native-like transitions
- Touch-optimized UI

### ✅ Fast Loading
- Service worker caching
- Optimized assets
- Lazy loading where appropriate

## Converting to Android APK

### Option 1: Using PWA Builder
1. Go to https://www.pwabuilder.com/
2. Enter your deployed app URL
3. Click "Build My PWA"
4. Download the Android package
5. Sign and publish to Play Store

### Option 2: Using Bubblewrap
```bash
# Install Bubblewrap
npm install -g @bubblewrap/cli

# Initialize project
bubblewrap init --manifest https://your-domain.com/manifest.json

# Build APK
bubblewrap build

# The APK will be in the output directory
```

### Option 3: Using Capacitor
```bash
# Install Capacitor
npm install @capacitor/core @capacitor/cli
npx cap init

# Add Android platform
npx cap add android

# Build and sync
npm run build
npx cap sync

# Open in Android Studio
npx cap open android
```

## Deployment Checklist

- [ ] Generate all required icon sizes
- [ ] Update manifest.json with your domain
- [ ] Test service worker in production build
- [ ] Test installation on multiple devices
- [ ] Verify offline functionality
- [ ] Test on iOS Safari
- [ ] Test on Chrome Android
- [ ] Configure HTTPS (required for PWA)
- [ ] Add to app stores (optional)

## HTTPS Requirement

PWAs require HTTPS to work. Options:
1. **Development**: Use `localhost` (works without HTTPS)
2. **Production**: Use a service like:
   - Netlify (free HTTPS)
   - Vercel (free HTTPS)
   - Cloudflare Pages (free HTTPS)
   - Your own server with Let's Encrypt

## Updating the PWA

When you make changes:
1. Update the `CACHE_NAME` in `service-worker.js` (e.g., 'tire-shop-v2')
2. Rebuild the app
3. Deploy
4. Users will get the update on next visit

## Browser Support

### Full PWA Support:
- Chrome 67+ (Android, Desktop)
- Edge 79+
- Samsung Internet 8.2+
- Opera 54+

### Partial Support:
- Safari 11.1+ (iOS, macOS) - No service worker background sync
- Firefox 79+ - Limited PWA features

## Troubleshooting

### PWA not installing?
- Check HTTPS is enabled
- Verify manifest.json is accessible
- Check browser console for errors
- Ensure all required manifest fields are present

### Service worker not working?
- Check browser console for registration errors
- Verify service-worker.js is in public directory
- Clear browser cache and try again
- Check HTTPS is enabled

### Icons not showing?
- Verify icon files exist in /public/icons/
- Check file names match manifest.json
- Ensure icons are PNG format
- Verify icon sizes are correct

## Performance Optimization

### Already Implemented:
- Lazy loading of routes
- Code splitting
- Asset caching
- Optimized images

### Additional Recommendations:
- Use WebP images where possible
- Implement image lazy loading
- Minimize bundle size
- Use CDN for static assets

## Security Considerations

- Always use HTTPS in production
- Validate all user inputs
- Implement proper authentication
- Use secure API endpoints
- Regular security updates

## Analytics (Optional)

Add Google Analytics or similar:
```javascript
// In service-worker.js
self.addEventListener('fetch', (event) => {
  // Track offline usage
  if (!navigator.onLine) {
    // Send analytics when back online
  }
});
```

## Next Steps

1. Generate and add app icons
2. Test on multiple devices
3. Deploy to production with HTTPS
4. Test PWA installation
5. Submit to app stores (optional)
6. Monitor usage and performance

## Resources

- [PWA Builder](https://www.pwabuilder.com/)
- [Google PWA Checklist](https://web.dev/pwa-checklist/)
- [MDN PWA Guide](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps)
- [Workbox (Advanced SW)](https://developers.google.com/web/tools/workbox)
