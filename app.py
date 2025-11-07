#!/usr/bin/env python3
"""
Simple Flask API for AB SDL-C Agent AI Backend
"""

from flask import Flask, jsonify, request
import os

# Initialize the Flask application
app = Flask(__name__)

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify the API is running"""
    return jsonify({
        'status': 'healthy',
        'service': 'AB SDL-C Agent AI Backend'
    }), 200

# Echo endpoint for testing
@app.route('/echo', methods=['POST'])
def echo():
    """Echo endpoint that returns the posted data"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON data provided'}), 400
    
    return jsonify({
        'received': data,
        'message': 'Data received successfully'
    }), 200

# Main endpoint
@app.route('/', methods=['GET'])
def main():
    """Main endpoint providing service information"""
    return jsonify({
        'message': 'Welcome to AB SDL-C Agent AI Backend API',
        'version': '1.0.0',
        'endpoints': {
            'GET /health': 'Check if service is healthy',
            'POST /echo': 'Echo back posted data'
        }
    }), 200

if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    # Run the Flask app
    app.run(host='0.0.0.0', port=port, debug=True)