import os
import logging
from flask import Flask, render_template, request, flash, session, jsonify
from rdap_service import RDAPService

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# Initialize RDAP service
rdap_service = RDAPService()

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
        # Perform RDAP lookup
        result = rdap_service.lookup(ip_input)
        
        if 'error' in result:
            flash(f'Registry scan failed: {result["error"]}', 'error')
            return render_template('index.html', history=session.get('search_history', []))
        
        # Add to search history
        if 'search_history' not in session:
            session['search_history'] = []
        
        # Add current search to history (limit to 10 items)
        history_item = {
            'ip': ip_input,
            'rir': result.get('rir', 'Unknown'),
            'timestamp': result.get('timestamp', '')
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
