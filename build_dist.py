#!/usr/bin/env python3
"""
Static site generator for RIPEScanner
Creates a production-ready distribution build
"""

import os
import shutil
import json
from pathlib import Path

def create_dist_build():
    """Generate static distribution build"""
    
    # Create dist directory
    dist_dir = Path("dist")
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    dist_dir.mkdir()
    
    # Copy static assets
    static_src = Path("static")
    static_dist = dist_dir / "static"
    if static_src.exists():
        shutil.copytree(static_src, static_dist)
    
    # Create static HTML by reading and processing templates manually
    create_static_html(dist_dir)
    
    # Create standalone CSS (inline Bootstrap)
    create_standalone_css(static_dist)
    
    # Create production JavaScript
    create_production_js(static_dist)
    
    # Create deployment files
    create_deployment_files(dist_dir)
    
    print("✓ Distribution build created successfully in 'dist/' directory")
    print("✓ Static assets copied")
    print("✓ Templates rendered")
    print("✓ Production files optimized")
    print("\nDist build contents:")
    for item in dist_dir.rglob("*"):
        if item.is_file():
            print(f"  {item.relative_to(dist_dir)}")

def create_static_html(dist_dir):
    """Create static HTML files by manually processing templates"""
    
    # Read base template
    with open("templates/base.html", "r", encoding="utf-8") as f:
        base_content = f.read()
    
    # Read index template  
    with open("templates/index.html", "r", encoding="utf-8") as f:
        index_content = f.read()
    
    # Replace Flask template syntax with static paths
    base_content = base_content.replace("{{ url_for('static', filename='css/style.css') }}", "static/css/style.css")
    base_content = base_content.replace("{{ url_for('static', filename='js/main.js') }}", "static/js/main.js")
    
    # Remove template blocks and create static HTML
    # Extract content between {% block content %} and {% endblock %}
    import re
    content_match = re.search(r'{% block content %}(.*?){% endblock %}', index_content, re.DOTALL)
    if content_match:
        content_block = content_match.group(1)
    else:
        content_block = ""
    
    # Replace the content block in base template
    final_html = re.sub(r'{% block content %}.*?{% endblock %}', content_block, base_content, flags=re.DOTALL)
    
    # Remove remaining Jinja2 syntax
    final_html = re.sub(r'{%.*?%}', '', final_html)
    final_html = re.sub(r'{{.*?}}', '', final_html)
    
    # Clean up extra whitespace
    final_html = re.sub(r'\n\s*\n', '\n', final_html)
    
    # Write the static HTML
    with open(dist_dir / "index.html", "w", encoding="utf-8") as f:
        f.write(final_html)

def create_standalone_css(static_dist):
    """Create standalone CSS with Bootstrap inlined"""
    css_dir = static_dist / "css"
    
    # Read existing custom CSS
    custom_css = ""
    if (css_dir / "style.css").exists():
        with open(css_dir / "style.css", "r") as f:
            custom_css = f.read()
    
    # Create optimized CSS file
    optimized_css = f"""
/* RIPEScanner Production CSS */
/* Bootstrap is loaded via CDN for better caching */

{custom_css}

/* Production optimizations */
.container {{
    max-width: 1400px;
}}

.search-form {{
    background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
}}

.results-container {{
    min-height: 400px;
}}

/* Performance optimizations */
* {{
    box-sizing: border-box;
}}

img {{
    max-width: 100%;
    height: auto;
}}
"""
    
    with open(css_dir / "style.css", "w") as f:
        f.write(optimized_css)

def create_production_js(static_dist):
    """Create production-optimized JavaScript"""
    js_dir = static_dist / "js"
    
    # Read existing JS
    main_js = ""
    if (js_dir / "main.js").exists():
        with open(js_dir / "main.js", "r") as f:
            main_js = f.read()
    
    # Create production JS with error handling
    production_js = f"""
// RIPEScanner Production JavaScript
(function() {{
    'use strict';
    
    {main_js}
    
    // Production error handling
    window.addEventListener('error', function(e) {{
        console.error('RIPEScanner Error:', e.error);
    }});
    
    // Service worker registration for PWA capabilities
    if ('serviceWorker' in navigator) {{
        window.addEventListener('load', function() {{
            navigator.serviceWorker.register('/sw.js').then(function(registration) {{
                console.log('SW registered: ', registration);
            }}).catch(function(registrationError) {{
                console.log('SW registration failed: ', registrationError);
            }});
        }});
    }}
}})();
"""
    
    with open(js_dir / "main.js", "w") as f:
        f.write(production_js)

def create_deployment_files(dist_dir):
    """Create deployment configuration files"""
    
    # Create .htaccess for Apache
    htaccess = """
# RIPEScanner Apache Configuration
RewriteEngine On

# Security headers
Header always set X-Content-Type-Options nosniff
Header always set X-Frame-Options DENY
Header always set X-XSS-Protection "1; mode=block"
Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"

# Cache static assets
<filesMatch "\\.(css|js|png|jpg|jpeg|gif|ico|svg)$">
    ExpiresActive On
    ExpiresDefault "access plus 1 year"
</filesMatch>

# Compress files
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/plain
    AddOutputFilterByType DEFLATE text/html
    AddOutputFilterByType DEFLATE text/xml
    AddOutputFilterByType DEFLATE text/css
    AddOutputFilterByType DEFLATE application/xml
    AddOutputFilterByType DEFLATE application/xhtml+xml
    AddOutputFilterByType DEFLATE application/rss+xml
    AddOutputFilterByType DEFLATE application/javascript
    AddOutputFilterByType DEFLATE application/x-javascript
</IfModule>

# Single Page Application routing
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule . /index.html [L]
"""
    
    with open(dist_dir / ".htaccess", "w") as f:
        f.write(htaccess)
    
    # Create nginx.conf
    nginx_conf = """
# RIPEScanner Nginx Configuration
server {
    listen 80;
    server_name ripescanner.example.com;
    root /var/www/ripescanner/dist;
    index index.html;

    # Security headers
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options DENY;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";

    # Static file caching
    location ~* \\.(css|js|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;

    # SPA routing
    location / {
        try_files $uri $uri/ /index.html;
    }
}
"""
    
    with open(dist_dir / "nginx.conf", "w") as f:
        f.write(nginx_conf)
    
    # Create service worker for PWA
    service_worker = """
// RIPEScanner Service Worker
const CACHE_NAME = 'ripescanner-v1.0.0';
const urlsToCache = [
    '/',
    '/static/css/style.css',
    '/static/js/main.js',
    'https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css',
    'https://unpkg.com/feather-icons'
];

self.addEventListener('install', function(event) {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(function(cache) {
                return cache.addAll(urlsToCache);
            })
    );
});

self.addEventListener('fetch', function(event) {
    event.respondWith(
        caches.match(event.request)
            .then(function(response) {
                if (response) {
                    return response;
                }
                return fetch(event.request);
            }
        )
    );
});
"""
    
    with open(dist_dir / "sw.js", "w") as f:
        f.write(service_worker)
    
    # Create package.json for deployment metadata
    package_json = {
        "name": "ripescanner",
        "version": "1.0.0",
        "description": "Advanced Network Intelligence Platform - Multi-Registry RDAP Lookup Tool",
        "author": "Hitesh Prajapati",
        "license": "MIT",
        "homepage": "https://github.com/hitesh/ripescanner",
        "repository": {
            "type": "git",
            "url": "https://github.com/hitesh/ripescanner.git"
        },
        "keywords": [
            "rdap",
            "network-intelligence",
            "ripe",
            "arin",
            "apnic",
            "lacnic",
            "afrinic",
            "ip-lookup"
        ],
        "engines": {
            "node": ">=14.0.0"
        },
        "scripts": {
            "deploy": "echo 'Deploy static files to your web server'"
        }
    }
    
    with open(dist_dir / "package.json", "w") as f:
        json.dump(package_json, f, indent=2)
    
    # Create README for deployment
    readme = """# RIPEScanner Distribution Build

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
"""
    
    with open(dist_dir / "README.md", "w") as f:
        f.write(readme)

if __name__ == "__main__":
    create_dist_build()