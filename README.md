# 🌐 RIPEScanner

**Advanced Network Intelligence Platform** - Multi-Registry RDAP Lookup Tool

A powerful Flask-based web application providing comprehensive RDAP (Registration Data Access Protocol) capabilities across all Regional Internet Registries with intelligent automatic detection, advanced geolocation intelligence, ASN analysis, batch processing, and professional red-black themed interface.

![RIPEScanner Interface](https://img.shields.io/badge/Interface-Professional%20Red%20%26%20Black-dc3545?style=for-the-badge&logo=html5&logoColor=white)
![Multi-RIR Support](https://img.shields.io/badge/RIR%20Support-All%205%20Registries-success?style=for-the-badge&logo=globe&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.0+-000000?style=for-the-badge&logo=flask&logoColor=white)
![Enhanced Intelligence](https://img.shields.io/badge/Enhanced-Geo%20%2B%20ASN-orange?style=for-the-badge&logo=location-arrow&logoColor=white)

## ✨ Features

### 🎯 **Core Functionality**
- **Intelligent RIR Detection** - Automatically identifies the correct Regional Internet Registry
- **Multi-Registry RDAP Queries** - Supports all major RIRs with equal treatment
- **Comprehensive IP Intelligence** - Detailed network information, organization data, and contact details
- **Real-time Lookup** - Fast, responsive queries with professional error handling
- **Search History** - Session-based lookup history tracking (last 10 searches)

### 🌍 **Enhanced Intelligence Features** ⭐ **NEW**
- **Geolocation Intelligence** - Detailed geographic information with coordinates, timezone, and regional data
- **ASN Analysis** - Autonomous System Number lookup with provider details
- **Enhanced Lookup Mode** - Combined RDAP, geolocation, and ASN data in single queries
- **Batch Processing** - Process multiple IP addresses simultaneously with progress tracking
- **Analytics Dashboard** - Usage statistics, RIR distribution, and performance insights
- **Export Capabilities** - CSV and JSON export for batch results and analytics

### 🚀 **Advanced Operations**
- **Batch IP Scanning** - Process lists of IP addresses with progress indicators
- **Multi-format Input** - Support for individual IPs, CIDR blocks, and CSV format
- **Real-time Progress** - Live batch processing with success/error tracking
- **Export & Analytics** - Professional data export and usage analytics
- **API Endpoints** - RESTful API for programmatic access

### 🌍 **Regional Internet Registry Coverage**
- **RIPE NCC** - Europe/Middle East/Central Asia
- **ARIN** - North America  
- **APNIC** - Asia Pacific
- **LACNIC** - Latin America and Caribbean
- **AFRINIC** - Africa

### 🎨 **Professional Interface**
- Modern red and black themed design
- Responsive Bootstrap-based layout with dark theme
- Real-time form validation and user feedback
- Loading states and progress indicators
- Advanced modal interfaces for batch operations
- Quick access panel for advanced features
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
   gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
   ```

5. **Open your browser**
   ```
   http://localhost:5000
   ```

## 📁 Project Structure

```
RIPEScanner/
├── app.py                 # Main Flask application with all routes
├── main.py               # Application entry point  
├── rdap_service.py       # Enhanced RDAP service with geo/ASN support
├── build_dist.py         # Static build generator
├── templates/
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Main interface with advanced features
│   └── analytics.html    # Analytics dashboard template
├── static/
│   ├── css/
│   │   └── style.css     # Custom styling and theme
│   └── js/
│       └── main.js       # Enhanced JavaScript with batch processing
├── dist/                 # Production build (generated)
└── replit.md            # Project documentation
```

## 🔧 Technical Architecture

### Backend Components
- **Flask Web Framework** - Lightweight, modern web application framework
- **Enhanced RDAP Service** - Intelligent RIR detection with geolocation and ASN support
- **Batch Processing Engine** - Efficient multi-IP processing with progress tracking
- **Session Management** - Secure session-based search history and analytics
- **Export Services** - CSV/JSON export functionality

### Frontend Stack
- **Bootstrap 5** - Professional dark theme with Replit customization
- **Enhanced JavaScript** - Advanced client-side features including batch processing
- **Feather Icons** - Clean, consistent iconography
- **Modal Interfaces** - Professional batch processing and API documentation
- **Responsive Design** - Mobile-first approach with advanced UI components

### Enhanced Services
```python
# Enhanced RDAP service with intelligence features
def enhanced_rdap_lookup(ip_address):
    # Combined lookup providing:
    # - Standard RDAP data
    # - Geolocation intelligence
    # - ASN information
    # - Enhanced error handling
```

## 🌐 API Endpoints

### Core RDAP Services
- `POST /lookup` - Standard RDAP lookup
- `POST /enhanced_lookup` - Enhanced lookup with geo/ASN data
- `POST /validate` - IP address validation
- `POST /batch_lookup` - Batch processing endpoint

### Intelligence Services
- `GET /geolocation/<ip>` - Geolocation data for IP
- `GET /asn/<ip>` - ASN information for IP
- `GET /analytics` - Analytics dashboard
- `GET /api/stats` - Usage statistics JSON

### Export Services
- `GET /export/csv` - Export batch results as CSV
- `GET /export/json` - Export batch results as JSON

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

## 📊 Advanced Features Guide

### 🔄 **Batch Processing**
1. Click the batch processing button (layers icon) in the quick access panel
2. Enter IP addresses (one per line or comma-separated)
3. Supports CIDR blocks and comments (lines starting with #)
4. Monitor real-time progress with success/error counters
5. Export results in CSV or JSON format

### 📈 **Analytics Dashboard**
- Access via the analytics button (bar chart icon)
- View session statistics and RIR distribution
- Monitor enhanced lookup usage
- Track recent activity and performance insights

### 🌍 **Enhanced Lookup Mode**
Enhanced lookups provide:
- **Standard RDAP data** - Registry information, organization details
- **Geolocation intelligence** - Country, region, city, timezone, coordinates  
- **ASN information** - Autonomous System details and provider data
- **Combined results** - Single interface for comprehensive intelligence

### 📤 **Export Capabilities**
- **CSV Export** - Structured data for spreadsheet analysis
- **JSON Export** - Machine-readable format for further processing
- **Session Analytics** - Export usage statistics and activity data

## 🔒 Security Features

- **Secure Headers** - XSS protection, CSRF prevention
- **Input Validation** - Comprehensive client and server-side validation
- **Session Security** - Secure session management with configurable secrets
- **HTTPS Ready** - TLS/SSL configuration included
- **Content Security Policy** - CSP headers configured
- **Rate Limiting** - Built-in protection against abuse

## 🛠️ Development

### Local Development
```bash
# Enable debug mode
export FLASK_ENV=development
export FLASK_DEBUG=1
python main.py
```

### Adding New Features
1. **New RIRs** - Update `rdap_service.py` with endpoints and detection logic
2. **Enhanced Services** - Extend geolocation or ASN providers
3. **UI Components** - Add new modals or interface elements
4. **Export Formats** - Implement additional export options

### Customizing Theme
- Modify `static/css/style.css` for custom styling
- Bootstrap variables can be overridden
- Color scheme uses CSS custom properties for easy theming

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
- Test all new features thoroughly

## 🔄 Recent Updates (v2.0)

### Major Enhancements
- ✅ **Enhanced Intelligence** - Added geolocation and ASN lookup capabilities
- ✅ **Batch Processing** - Multi-IP processing with progress tracking
- ✅ **Analytics Dashboard** - Usage statistics and performance insights  
- ✅ **Export Features** - CSV/JSON export functionality
- ✅ **Advanced UI** - Modal interfaces and quick access panel
- ✅ **API Expansion** - New endpoints for enhanced services

### Technical Improvements
- Enhanced RDAP service with multi-provider support
- Improved JavaScript with async batch processing
- Professional analytics dashboard with real-time updates
- Advanced error handling and user feedback
- Production-ready static build pipeline

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Created By

**Hitesh Prajapati**
- B.E. (Computer) • M.Sc (Computer Systems Engineering)
- CCNP Enterprise • Juniper Certified Professional

## 🙏 Acknowledgments

- **Regional Internet Registries** - RIPE, ARIN, APNIC, LACNIC, AFRINIC for providing RDAP services
- **Geolocation Providers** - For enhanced geographic intelligence
- **ASN Data Sources** - For autonomous system information
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

*Comprehensive Multi-Registry RDAP Intelligence with Advanced Analytics*
