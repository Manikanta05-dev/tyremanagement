// Simple icon generator using Canvas (requires canvas package)
// Run: node generate-icons.js

const fs = require('fs');
const path = require('path');

// Create a simple SVG icon
const sizes = [72, 96, 128, 144, 152, 192, 384, 512];

const generateSVGIcon = (size) => {
  return `<?xml version="1.0" encoding="UTF-8"?>
<svg width="${size}" height="${size}" viewBox="0 0 ${size} ${size}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#1e40af;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#3b82f6;stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="${size}" height="${size}" fill="url(#grad)" rx="${size * 0.15}"/>
  <text x="50%" y="50%" font-size="${size * 0.5}" text-anchor="middle" dominant-baseline="middle" fill="white" font-family="Arial, sans-serif">🚗</text>
</svg>`;
};

const iconsDir = path.join(__dirname, 'public', 'icons');

// Ensure icons directory exists
if (!fs.existsSync(iconsDir)) {
  fs.mkdirSync(iconsDir, { recursive: true });
}

// Generate SVG icons
sizes.forEach(size => {
  const svg = generateSVGIcon(size);
  const filename = `icon-${size}x${size}.svg`;
  fs.writeFileSync(path.join(iconsDir, filename), svg);
  console.log(`✓ Generated ${filename}`);
});

console.log('\n✅ All icons generated successfully!');
console.log('📁 Location: frontend/public/icons/');
console.log('\n💡 Note: SVG icons work for PWA. For better compatibility, convert to PNG using:');
console.log('   - Online tool: https://www.pwabuilder.com/imageGenerator');
console.log('   - Or use ImageMagick/Sharp for conversion');
