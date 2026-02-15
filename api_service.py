"""ConversationalFilter REST API Service"""
import os
import json
from functools import wraps
from datetime import datetime

from flask import Flask, request, jsonify
from pydantic import ValidationError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the conversational filter modules
from src.conversational_filter import (
    ConversationalFilter,
    UserProfile,
    FilteredResponse
)

# Initialize Flask app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Configuration from environment
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
LEMONSQUEEZY_API_KEY = os.getenv('LEMONSQUEEZY_API_KEY')
LEMONSQUEEZY_STORE_ID = os.getenv('LEMONSQUEEZY_STORE_ID')
LEMONSQUEEZY_WEBHOOK_SECRET = os.getenv('LEMONSQUEEZY_WEBHOOK_SECRET')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

app.config['SECRET_KEY'] = SECRET_KEY

# In-memory license store (production would use database)
VALID_LICENSES = set()


def require_license(f):
    """Decorator to check for valid license key"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        license_key = request.headers.get('X-License-Key')

        if not license_key:
            return jsonify({
                'error': 'Missing X-License-Key header',
                'message': 'A valid Lemonsqueezy license key is required'
            }), 401

        # Basic validation (production would validate against Lemonsqueezy)
        if license_key not in VALID_LICENSES and not DEBUG:
            # Allow any key in debug mode for testing
            if LEMONSQUEEZY_API_KEY:  # Only enforce if API key is configured
                return jsonify({
                    'error': 'Invalid license key',
                    'message': 'The provided license key is not valid'
                }), 403

        return f(*args, **kwargs)

    return decorated_function


@app.route('/api/v1/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'conversational-filter-api',
        'timestamp': datetime.utcnow().isoformat()
    }), 200


@app.route('/api/v1/products', methods=['GET'])
def list_products():
    """List available products and pricing"""
    products = {
        'individual_monthly': {
            'name': 'Individual Monthly',
            'price': 99.00,
            'currency': 'usd',
            'billing': 'monthly',
            'features': [
                '1 developer license',
                'Commercial use',
                'Email support',
                'All API features'
            ]
        },
        'individual_yearly': {
            'name': 'Individual Yearly',
            'price': 990.00,
            'currency': 'usd',
            'billing': 'yearly',
            'features': [
                '1 developer license',
                'Commercial use',
                'Email support',
                'All API features',
                'Save 10%'
            ]
        },
        'team_monthly': {
            'name': 'Team Monthly',
            'price': 499.00,
            'currency': 'usd',
            'billing': 'monthly',
            'features': [
                'Up to 5 developers',
                'Commercial use',
                'Priority support',
                'All API features',
                'Team management'
            ]
        },
        'team_yearly': {
            'name': 'Team Yearly',
            'price': 4990.00,
            'currency': 'usd',
            'billing': 'yearly',
            'features': [
                'Up to 5 developers',
                'Commercial use',
                'Priority support',
                'All API features',
                'Team management',
                'Save 10%'
            ]
        }
    }

    return jsonify(products), 200


@app.route('/api/v1/checkout', methods=['POST'])
def create_checkout():
    """Create a Lemonsqueezy checkout"""
    if not LEMONSQUEEZY_STORE_ID:
        return jsonify({
            'error': 'Payment system not configured',
            'message': 'Lemonsqueezy store ID not configured on server'
        }), 500

    data = request.get_json() or {}
    product = data.get('product', 'individual_monthly')

    # Map product to variant ID (update these with your Lemonsqueezy variant IDs)
    variants = {
        'individual_monthly': 'REPLACE_WITH_VARIANT_ID',
        'individual_yearly': 'REPLACE_WITH_VARIANT_ID',
        'team_monthly': 'REPLACE_WITH_VARIANT_ID',
        'team_yearly': 'REPLACE_WITH_VARIANT_ID'
    }

    variant_id = variants.get(product)
    if not variant_id:
        return jsonify({
            'error': 'Invalid product',
            'message': f'Product must be one of: {list(variants.keys())}'
        }), 400

    # Lemonsqueezy checkout URL
    checkout_url = f'https://conversationalfilter.lemonsqueezy.com/checkout/buy/{variant_id}'

    return jsonify({
        'checkout_url': checkout_url,
        'product': product,
        'created_at': datetime.utcnow().isoformat()
    }), 200


@app.route('/api/v1/filter', methods=['POST'])
@require_license
def filter_response():
    """Main API endpoint: Filter an LLM response"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'error': 'Invalid request',
                'message': 'Request body must be valid JSON'
            }), 400

        question = data.get('question')
        response = data.get('response')
        user_profile_data = data.get('user_profile')

        if not question or not response:
            return jsonify({
                'error': 'Missing required fields',
                'message': 'Both "question" and "response" are required'
            }), 400

        # Create user profile if provided
        user_profile = None
        if user_profile_data:
            try:
                user_profile = UserProfile(**user_profile_data)
            except ValidationError as e:
                return jsonify({
                    'error': 'Invalid user profile',
                    'details': e.errors()
                }), 400

        # Initialize filter
        cf = ConversationalFilter(user_profile=user_profile)

        # Filter the response
        filtered = cf.filter_response(question, response)

        return jsonify({
            'original_response': filtered.original_response,
            'filtered_response': filtered.filtered_response,
            'clarifying_question': filtered.clarifying_question,
            'filters_applied': filtered.filters_applied,
            'elaboration_ratio': filtered.elaboration_ratio,
            'timestamp': datetime.utcnow().isoformat()
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Processing error',
            'message': str(e)
        }), 500


@app.route('/api/v1/license/validate', methods=['POST'])
def validate_license():
    """Validate a license key (placeholder for Lemonsqueezy integration)"""
    data = request.get_json() or {}
    license_key = data.get('license_key')

    if not license_key:
        return jsonify({
            'error': 'Missing license_key',
            'message': 'Please provide a license_key in the request body'
        }), 400

    # In production, this would validate against Lemonsqueezy API
    # For now, return success for any key in debug mode
    if DEBUG or not LEMONSQUEEZY_API_KEY:
        VALID_LICENSES.add(license_key)
        return jsonify({
            'valid': True,
            'message': 'License is valid (dev mode)',
            'license_key': license_key
        }), 200

    return jsonify({
        'valid': False,
        'message': 'License validation not configured'
    }), 400


@app.route('/api/v1/webhook/lemonsqueezy', methods=['POST'])
def webhook_handler():
    """Handle Lemonsqueezy webhooks for order/subscription events"""
    # Verify webhook signature (simplified for now)
    signature = request.headers.get('X-Lemonsqueezy-Signature')

    data = request.get_json() or {}
    event_type = data.get('meta', {}).get('event_name', 'unknown')

    # Log webhook (in production, would store in database)
    print(f'Webhook received: {event_type}')

    # Handle different event types
    if event_type == 'order_created':
        order_data = data.get('data', {})
        # Add license key to valid set
        # VALID_LICENSES.add(order_data.get('license_key'))

    elif event_type == 'subscription_updated':
        subscription_data = data.get('data', {})
        # Update subscription status
        pass

    elif event_type == 'subscription_cancelled':
        subscription_data = data.get('data', {})
        # Remove or disable license
        pass

    return jsonify({'received': True}), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Not found',
        'message': 'The requested endpoint does not exist',
        'path': request.path
    }), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred on the server'
    }), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=DEBUG)
