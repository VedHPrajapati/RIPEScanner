import os
import logging
import json
import ipaddress
from datetime import datetime, timedelta
from flask import Flask, render_template, request, flash, session, jsonify
from rdap_service import RDAPService, GeolocationService, ASNService, BatchService

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# Initialize services
rdap_service = RDAPService()
geo_service = GeolocationService()
asn_service = ASNService()
batch_service = BatchService(rdap_service)

@app.route('/')
def index():
    """Main page with RDAP lookup form"""
    # Get search history from session
    history = session.get('search_history', [])
    return render_template('index.html', history=history)

@app.route('/lookup', methods=['POST'])
def lookup():
    """Handle RDAP lookup requests"""
    ip_input = request.form.get('ip_address', '').strip()
    
    if not ip_input:
        flash('Please enter an IP address or network prefix', 'error')
        return render_template('index.html', history=session.get('search_history', []))
    
    try:
        # Check if enhanced lookup is requested
        enhanced_mode = request.form.get('enhanced_lookup') == 'true'
        
        # Perform RDAP lookup
        result = rdap_service.lookup(ip_input)
        
        if 'error' in result:
            flash(f'Registry scan failed: {result["error"]}', 'error')
            return render_template('index.html', history=session.get('search_history', []))
        
        # Enhanced data collection if requested
        if enhanced_mode:
            geo_data = geo_service.get_location_data(ip_input)
            asn_data = asn_service.get_asn_data(ip_input)
            
            result['enhanced'] = True
            result['geolocation'] = geo_data
            result['asn_info'] = asn_data
        
        # Add to search history
        if 'search_history' not in session:
            session['search_history'] = []
        
        # Add current search to history (limit to 10 items)
        history_item = {
            'ip': ip_input,
            'rir': result.get('rir', 'Unknown'),
            'timestamp': result.get('timestamp', ''),
            'enhanced': enhanced_mode
        }
        
        session['search_history'].insert(0, history_item)
        session['search_history'] = session['search_history'][:10]
        session.modified = True
        
        return render_template('index.html', 
                             result=result, 
                             query=ip_input,
                             history=session.get('search_history', []))
        
    except Exception as e:
        logging.error(f"Error during RDAP lookup: {str(e)}")
        flash(f'An error occurred: {str(e)}', 'error')
        return render_template('index.html', history=session.get('search_history', []))

@app.route('/validate', methods=['POST'])
def validate_ip():
    """AJAX endpoint for real-time IP validation"""
    ip_input = request.json.get('ip_address', '').strip()
    
    if not ip_input:
        return jsonify({'valid': False, 'message': 'Please enter an IP address'})
    
    validation_result = rdap_service.validate_ip(ip_input)
    return jsonify(validation_result)

@app.route('/clear_history', methods=['POST'])
def clear_history():
    """Clear search history"""
    session.pop('search_history', None)
    flash('Search history cleared', 'success')
    return render_template('index.html', history=[])

@app.route('/batch_lookup', methods=['POST'])
def batch_lookup():
    """Handle batch IP address processing"""
    ip_list_text = request.form.get('ip_list', '').strip()
    
    if not ip_list_text:
        return jsonify({'success': False, 'error': 'Please provide IP addresses to process'})
    
    # Parse IP list (support multiple formats)
    ip_addresses = []
    for line in ip_list_text.split('\n'):
        line = line.strip()
        if line and not line.startswith('#'):  # Skip comments
            if ',' in line:  # CSV format
                ip_addresses.extend([ip.strip() for ip in line.split(',')])
            else:  # Line-separated
                ip_addresses.append(line)
    
    try:
        # Process batch
        results = batch_service.process_batch(ip_addresses)
        
        # Store results in session for export
        session['batch_results'] = results
        session.modified = True
        
        return jsonify({
            'success': True,
            'total_processed': results['total_processed'],
            'total_errors': results['total_errors'],
            'results': results['results'][:50],  # Limit display results
            'has_more': len(results['results']) > 50
        })
        
    except Exception as e:
        logging.error(f"Batch processing error: {str(e)}")
        return jsonify({'success': False, 'error': f'Batch processing failed: {str(e)}'})

@app.route('/enhanced_lookup', methods=['POST'])
def enhanced_lookup():
    """Enhanced IP lookup with geolocation and ASN data"""
    ip_input = request.json.get('ip_address', '').strip()
    
    if not ip_input:
        return jsonify({'success': False, 'error': 'Please provide an IP address'})
    
    try:
        # Validate IP
        validation = rdap_service.validate_ip(ip_input)
        if not validation['valid']:
            return jsonify({'success': False, 'error': validation['message']})
        
        # Get all data
        rdap_result = rdap_service.lookup(ip_input)
        geo_data = geo_service.get_location_data(ip_input)
        asn_data = asn_service.get_asn_data(ip_input)
        
        return jsonify({
            'success': True,
            'ip': ip_input,
            'rdap': rdap_result,
            'geolocation': geo_data,
            'asn': asn_data,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logging.error(f"Enhanced lookup error: {str(e)}")
        return jsonify({'success': False, 'error': f'Enhanced lookup failed: {str(e)}'})

@app.route('/geolocation/<ip_address>')
def geolocation(ip_address):
    """Get geolocation data for IP address"""
    try:
        geo_data = geo_service.get_location_data(ip_address)
        return jsonify(geo_data)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/asn/<ip_address>')
def asn_lookup(ip_address):
    """Get ASN information for IP address"""
    try:
        asn_data = asn_service.get_asn_data(ip_address)
        return jsonify(asn_data)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/export/<format_type>')
def export_results(format_type):
    """Export batch results in various formats"""
    results = session.get('batch_results', {})
    
    if not results:
        flash('No batch results to export', 'error')
        return redirect('/')
    
    try:
        export_data = batch_service.export_results(results, format_type)
        
        if format_type == 'csv':
            from flask import Response
            return Response(
                export_data,
                mimetype='text/csv',
                headers={'Content-Disposition': 'attachment; filename=ripescanner_results.csv'}
            )
        else:  # JSON
            from flask import Response
            return Response(
                export_data,
                mimetype='application/json',
                headers={'Content-Disposition': 'attachment; filename=ripescanner_results.json'}
            )
            
    except Exception as e:
        flash(f'Export failed: {str(e)}', 'error')
        return redirect('/')

@app.route('/analytics')
def analytics():
    """Display analytics and statistics"""
    history = session.get('search_history', [])
    
    # Generate basic analytics
    analytics_data = {
        'total_searches': len(history),
        'rir_distribution': {},
        'recent_activity': history[:5],
        'enhanced_searches': 0
    }
    
    for item in history:
        rir = item.get('rir', 'Unknown')
        analytics_data['rir_distribution'][rir] = analytics_data['rir_distribution'].get(rir, 0) + 1
        
        if item.get('enhanced', False):
            analytics_data['enhanced_searches'] += 1
    
    return render_template('analytics.html', analytics=analytics_data)

@app.route('/api/stats')
def api_stats():
    """API endpoint for usage statistics"""
    history = session.get('search_history', [])
    
    stats = {
        'session_searches': len(history),
        'rir_breakdown': {},
        'enhanced_usage': 0,
        'last_search': history[0] if history else None
    }
    
    for item in history:
        rir = item.get('rir', 'Unknown')
        stats['rir_breakdown'][rir] = stats['rir_breakdown'].get(rir, 0) + 1
        
        if item.get('enhanced', False):
            stats['enhanced_usage'] += 1
    
    return jsonify(stats)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
