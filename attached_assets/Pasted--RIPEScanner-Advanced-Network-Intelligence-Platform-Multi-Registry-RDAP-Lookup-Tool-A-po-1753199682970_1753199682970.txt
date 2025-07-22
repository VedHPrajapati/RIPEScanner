# 🌐 RIPEScanner

**Advanced Network Intelligence Platform** - Multi-Registry RDAP Lookup Tool

A powerful Flask-based web application providing comprehensive RDAP (Registration Data Access Protocol) capabilities across all Regional Internet Registries with intelligent automatic detection and professional red-black themed interface.

![RIPEScanner Interface](https://img.shields.io/badge/Interface-Professional%20Red%20%26%20Black-dc3545?style=for-the-badge&logo=html5&logoColor=white)
![Multi-RIR Support](https://img.shields.io/badge/RIR%20Support-All%205%20Registries-success?style=for-the-badge&logo=globe&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.0+-000000?style=for-the-badge&logo=flask&logoColor=white)

## ✨ Features

### 🎯 **Core Functionality**
- **Intelligent RIR Detection** - Automatically identifies the correct Regional Internet Registry
- **Multi-Registry RDAP Queries** - Supports all major RIRs with equal treatment
- **Comprehensive IP Intelligence** - Detailed network information, organization data, and contact details
- **Real-time Lookup** - Fast, responsive queries with professional error handling
- **Search History** - Session-based lookup history tracking (last 10 searches)

### 🌍 **Regional Internet Registry Coverage**
- **RIPE NCC** - Europe/Middle East
- **ARIN** - North America  
- **APNIC** - Asia Pacific
- **LACNIC** - Latin America
- **AFRINIC** - Africa

### 🎨 **Professional Interface**
- Modern red and black themed design
- Responsive Bootstrap-based layout
- Real-time form validation
- Loading states and progress indicators
- Clean, intuitive user experience

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Flask and dependencies (see `pyproject.toml`)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/[username]/ripescanner.git
   cd ripescanner
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   # or using modern Python package managers:
   pip install .
   ```

3. **Set environment variables**
   ```bash
   export SESSION_SECRET="your-secret-key-here"
   ```

4. **Run the application**
   ```bash
   python main.py
   # or using gunicorn for production:
   gunicorn --bind 0.0.0.0:5000 main:app
   ```

5. **Open your browser**
   ```
   http://localhost:5000
   ```

## 📁 Project Structure

```
RIPEScanner/
├── app.py                 # Main Flask application
├── main.py               # Application entry point  
├── rdap_service.py       # RDAP query service and RIR detection
├── build_dist.py         # Static build generator
├── templates/
│   ├── base.html         # Base template with navigation
│   └── index.html        # Main interface template
├── static/
│   ├── css/
│   │   └── style.css     # Custom styling and theme
│   └── js/
│       └── main.js       # Client-side validation and UX
├── dist/                 # Production build (generated)
└── replit.md            # Project documentation
```

## 🔧 Technical Architecture

### Backend Components
- **Flask Web Framework** - Lightweight, modern web application framework
- **RDAP Service Layer** - Intelligent RIR detection and protocol handling
- **Session Management** - Secure session-based search history

### Frontend Stack
- **Bootstrap 5** - Professional dark theme with Replit customization
- **Vanilla JavaScript** - Lightweight client-side validation and interactions
- **Feather Icons** - Clean, consistent iconography
- **Responsive Design** - Mobile-first approach

### RIR Detection Logic
```python
# Automatic RIR detection based on IP ranges
def detect_rir(ip_address):
    # Intelligent detection logic for:
    # - ARIN (North America)
    # - RIPE (Europe/Middle East)
    # - APNIC (Asia Pacific) 
    # - LACNIC (Latin America)
    # - AFRINIC (Africa)
```

## 🌐 Deployment Options

### 1. Static Deployment (Recommended)
Generate a static build for hosting on CDNs or static hosts:

```bash
python build_dist.py
```

Deploy the `dist/` folder to:
- **Netlify** - Drag & drop deployment
- **Vercel** - GitHub integration
- **GitHub Pages** - Free static hosting
- **AWS S3** - Scalable static hosting
- **CloudFlare Pages** - Global CDN deployment

### 2. Server Deployment

#### Docker Deployment
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install .
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
```

#### Traditional Server
```bash
# Using gunicorn (recommended)
gunicorn --bind 0.0.0.0:5000 --workers 4 main:app

# Using nginx + gunicorn
# See dist/nginx.conf for configuration
```

## 📊 Performance Features

- **Lightweight Architecture** - No database dependencies
- **Session-based Storage** - Efficient memory usage
- **CDN-Ready Assets** - Optimized static files
- **Service Worker Support** - PWA capabilities for offline access
- **Compression Ready** - Gzip/Brotli compression support

## 🔒 Security Features

- **Secure Headers** - XSS protection, CSRF prevention
- **Input Validation** - Client and server-side validation
- **Session Security** - Secure session management
- **HTTPS Ready** - TLS/SSL configuration included
- **Content Security Policy** - CSP headers configured

## 🛠️ Development

### Local Development
```bash
# Enable debug mode
export FLASK_ENV=development
export FLASK_DEBUG=1
python main.py
```

### Adding New RIRs
1. Update `rdap_service.py` with new RIR endpoints
2. Add detection logic in `detect_rir()` function
3. Update templates to include new registry badge

### Customizing Theme
- Modify `static/css/style.css` for custom styling
- Bootstrap variables can be overridden
- Color scheme uses CSS custom properties

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable names
- Add comments for complex logic
- Maintain the existing project structure

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Created By

**Hitesh Prajapati**
- B.E. (Computer) • M.Sc (Computer Systems Engineering)
- CCNP Enterprise • Juniper Certified Professional

## 🙏 Acknowledgments

- **Regional Internet Registries** - RIPE, ARIN, APNIC, LACNIC, AFRINIC for providing RDAP services
- **Bootstrap Team** - For the excellent CSS framework
- **Feather Icons** - For beautiful, consistent iconography
- **Flask Community** - For the lightweight, powerful web framework

## 🔗 Links

- [Live Demo](https://your-deployment-url.com)
- [RDAP Specification](https://tools.ietf.org/html/rfc7483)
- [Bootstrap Documentation](https://getbootstrap.com/)

---

<div align="center">

**Advanced Network Intelligence Platform**

[![GitHub stars](https://img.shields.io/github/stars/[username]/ripescanner?style=social)](https://github.com/[username]/ripescanner)
[![GitHub forks](https://img.shields.io/github/forks/[username]/ripescanner?style=social)](https://github.com/[username]/ripescanner)

</div>
