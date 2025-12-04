# Frontend Assets

This directory contains static assets for the frontend application.

## Logo

### Available Logos

This directory contains multiple logo options for easy switching:

- **`logo.png`** - Currently active logo (displayed in app)
- **`logo-todo.png`** - Todo/task management themed logo (24K)
- **`logo-swiftpay.png`** - SwiftPay green corporate logo (6.8K)

### Quick Logo Switching

**Easy Method - Switch between pre-loaded logos:**
```bash
# Switch to Todo logo
cp frontend/src/assets/logo-todo.png frontend/src/assets/logo.png

# Switch to SwiftPay logo
cp frontend/src/assets/logo-swiftpay.png frontend/src/assets/logo.png
```

**Advanced Method - Add your own logo:**
```bash
# Method 1: Replace the active logo directly
cp /path/to/new-logo.png frontend/src/assets/logo.png

# Method 2: Add and switch to a new logo
cp /path/to/new-logo.png frontend/src/assets/logo-mycompany.png
cp frontend/src/assets/logo-mycompany.png frontend/src/assets/logo.png

# Method 3: Update import in App.jsx (requires code change)
# Change: import logo from './assets/logo.png';
# To:     import logo from './assets/logo-mycompany.png';
```

### Current Logo
- **Active file**: `logo.png`
- **Dimensions**: 64x64 pixels (desktop), 48x48 pixels (mobile)
- **Format**: PNG with transparency support
- **Location**: Used in the app header alongside the "Task Manager" title

### Logo Requirements

**Recommended specifications:**
- **Format**: PNG, SVG, or WebP
- **Recommended size**: 128x128 pixels or larger (will be scaled down)
- **Aspect ratio**: Square (1:1) works best
- **Background**: Transparent PNG or SVG recommended
- **File size**: < 100KB for optimal loading

**Supported formats:**
- `.png` - Best for logos with transparency
- `.svg` - Best for scalable vector graphics
- `.jpg` / `.jpeg` - Works but no transparency support
- `.webp` - Modern format with good compression

### CSS Customization

The logo styling can be customized in `frontend/src/App.css`:

```css
.app-logo {
  width: 64px;        /* Desktop width */
  height: 64px;       /* Desktop height */
  object-fit: contain; /* Maintains aspect ratio */
}

/* Mobile styling */
@media (max-width: 768px) {
  .app-logo {
    width: 48px;      /* Mobile width */
    height: 48px;     /* Mobile height */
  }
}
```

**Customization options:**
- **Size**: Adjust `width` and `height` values
- **Spacing**: Modify `gap` in `.app-header` class
- **Animations**: Add hover effects or animations
- **Position**: Change `app-header` flex direction
- **Border**: Add `border-radius` for rounded corners

### Adding More Assets

You can add more images or assets to this directory:

```bash
# Add a favicon
cp /path/to/favicon.ico frontend/public/favicon.ico

# Add background images
cp /path/to/background.jpg frontend/src/assets/background.jpg

# Add icon files
cp /path/to/icon.svg frontend/src/assets/icon.svg
```

Then import and use them in your components:

```javascript
import logo from './assets/logo.png';
import background from './assets/background.jpg';
import icon from './assets/icon.svg';
```

### Best Practices

1. **Optimize images** before adding them:
   - Use tools like ImageOptim, TinyPNG, or Squoosh
   - Target < 100KB for logos and icons
   - Use appropriate formats (PNG for transparency, JPEG for photos)

2. **Use descriptive names**:
   - `logo.png` - Main application logo
   - `icon.svg` - Generic icon
   - `background.jpg` - Background image

3. **Keep it organized**:
   - Images in `assets/images/`
   - Icons in `assets/icons/`
   - Fonts in `assets/fonts/`

4. **Version control**:
   - Commit optimized images only
   - Document image sources and licenses
   - Keep original high-res versions elsewhere

### Example: Using SVG Logo

If you want to use an SVG logo instead:

1. Add your SVG file:
   ```bash
   cp /path/to/logo.svg frontend/src/assets/logo.svg
   ```

2. Update `App.jsx`:
   ```javascript
   import logo from './assets/logo.svg';
   ```

3. No CSS changes needed - SVG scales perfectly!

### Troubleshooting

**Logo not appearing:**
- Check the file exists: `ls frontend/src/assets/logo.png`
- Verify the import path in `App.jsx`
- Check browser console for loading errors
- Restart the Vite dev server: `npm run dev`

**Logo appears blurry:**
- Use a higher resolution image (at least 128x128)
- Try SVG format for perfect scaling
- Check the `object-fit: contain` CSS property

**Logo too large/small:**
- Adjust `width` and `height` in `.app-logo` CSS class
- Maintain aspect ratio by setting both dimensions

## Quick Reference

**File structure:**
```
frontend/src/assets/
├── README.md (this file)
├── logo.png (currently active logo)
├── logo-todo.png (todo/task themed logo - 24K)
└── logo-swiftpay.png (SwiftPay green logo - 6.8K)
```

**Switch logos easily:**
```bash
# Use Todo logo
cp frontend/src/assets/logo-todo.png frontend/src/assets/logo.png

# Use SwiftPay logo  
cp frontend/src/assets/logo-swiftpay.png frontend/src/assets/logo.png
```

**Import in components:**
```javascript
import logo from './assets/logo.png';
```

**Use in JSX:**
```jsx
<img src={logo} alt="Logo" className="app-logo" />
```

**Customize in CSS:**
```css
.app-logo {
  width: 64px;
  height: 64px;
}
