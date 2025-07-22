# RIPEScanner - Multi-Registry RDAP Lookup Tool

## Overview

RIPEScanner is a Flask-based web application providing comprehensive RDAP (Registration Data Access Protocol) capabilities across all Regional Internet Registries. It automatically detects and queries appropriate RIR endpoints (RIPE, ARIN, APNIC, LACNIC, AFRINIC) to retrieve detailed registration information with equal treatment of all registries. Features a professional red and black theme for network intelligence operations.

## User Preferences

Preferred communication style: Simple, everyday language.
Creator: Hitesh Prajapati - B.E. (Computer), M.Sc (Computer Systems Engg), CCNP Enterprise, Juniper Certified Professional

## System Architecture

The application follows a simple three-tier architecture:

1. **Presentation Layer**: HTML templates with Bootstrap styling and JavaScript for client-side interactions
2. **Application Layer**: Flask web framework handling HTTP requests and business logic
3. **Service Layer**: RDAP service for handling IP address lookups and RIR detection

The architecture emphasizes simplicity and maintainability, avoiding over-engineering while providing a clean separation of concerns.

## Key Components

### Backend Components

- **Flask Application** (`app.py`): Main web application handling routes, session management, and request processing
- **RDAP Service** (`rdap_service.py`): Core service responsible for:
  - Automatic RIR detection based on IP address ranges
  - RDAP protocol interactions with different registry endpoints
  - Response parsing and formatting
- **Application Entry Point** (`main.py`): Simple application launcher for development

### Frontend Components

- **Base Template** (`templates/base.html`): Common layout with Bootstrap dark theme and navigation
- **Index Template** (`templates/index.html`): Main interface with lookup form and results display
- **Custom Styling** (`static/css/style.css`): Additional styles for loading states and form validation
- **JavaScript** (`static/js/main.js`): Client-side validation and user experience enhancements

### RIR Support

The application supports all five Regional Internet Registries:
- **ARIN**: North America
- **RIPE**: Europe, Middle East, Central Asia
- **APNIC**: Asia Pacific
- **LACNIC**: Latin America and Caribbean
- **AFRINIC**: Africa

## Data Flow

1. **User Input**: User enters an IP address or network prefix in the web form
2. **Client-side Validation**: JavaScript validates input format before submission
3. **Server Processing**: Flask receives the request and passes it to the RDAP service
4. **RIR Detection**: Service determines the appropriate RIR based on IP address ranges
5. **RDAP Query**: Service makes HTTP request to the corresponding RIR's RDAP endpoint
6. **Response Processing**: Service parses and formats the RDAP response
7. **Session Management**: Search history is stored in user session (limited to 10 items)
8. **Result Display**: Formatted results are rendered back to the user

## External Dependencies

### Python Libraries
- **Flask**: Web framework for handling HTTP requests and responses
- **requests**: HTTP library for making RDAP queries to external registries
- **ipaddress**: Built-in library for IP address validation and manipulation

### Frontend Libraries
- **Bootstrap**: CSS framework with dark theme customization
- **Feather Icons**: Icon library for consistent UI elements
- **Vanilla JavaScript**: No heavy frameworks, keeping the client-side lightweight

### External Services
- **RDAP Endpoints**: Direct integration with official RIR RDAP services
  - ARIN: `https://rdap.arin.net/registry/ip/`
  - RIPE: `https://rdap.db.ripe.net/ip/`
  - APNIC: `https://rdap.apnic.net/ip/`
  - LACNIC: `https://rdap.lacnic.net/rdap/ip/`
  - AFRINIC: `https://rdap.afrinic.net/rdap/ip/`

## Deployment Strategy

The application is designed for simple deployment with minimal configuration:

### Development
- Uses Flask's built-in development server
- Debug mode enabled for detailed error information
- Environment-based configuration for secrets

### Production Considerations
- Session secret should be set via environment variable
- Application runs on all interfaces (0.0.0.0) for container compatibility
- Logging configured for debugging and monitoring
- No database dependencies - uses in-memory session storage

### Configuration
- **Port**: Default 5000, configurable
- **Host**: Binds to all interfaces for container deployment
- **Session Secret**: Environment variable `SESSION_SECRET` with fallback to development key

The architecture prioritizes simplicity and reliability, making it easy to deploy on various platforms including Replit, Docker containers, or traditional web servers.