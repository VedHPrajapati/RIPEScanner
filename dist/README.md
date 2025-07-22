# RIPEScanner Distribution Build

This directory contains the production-ready static build of RIPEScanner.

## Deployment Options

### 1. Static Hosting (Recommended)
- Upload contents to any static hosting provider
- Supports: Netlify, Vercel, GitHub Pages, AWS S3, etc.

### 2. Web Server
- Copy files to web server document root
- Configure using provided nginx.conf or .htaccess

### 3. CDN Deployment
- Upload to CDN for global distribution
- Configure origin server settings

## Files Included
- `index.html` - Main application page
- `static/` - CSS, JavaScript, and assets
- `sw.js` - Service worker for PWA functionality
- `nginx.conf` - Nginx configuration example
- `.htaccess` - Apache configuration
- `package.json` - Deployment metadata

## Performance Features
- Optimized static assets
- Service worker caching
- Gzip compression support
- Long-term caching headers

## Security Features
- CSP headers configured
- XSS protection enabled
- HTTPS redirect ready
- Secure headers included

Created by: Hitesh Prajapati
Platform: Advanced Network Intelligence Platform
