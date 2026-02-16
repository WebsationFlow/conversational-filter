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
from src.conversational_filter.licensing import (
    LicenseValidator,
    verify_webhook_signature,
    VARIANT_PRODUCTS,
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

# License validator (keyless — calls Lemonsqueezy directly)
license_validator = LicenseValidator()

# In-memory license cache (avoids hitting Lemonsqueezy on every request)
# Keys: license_key string -> dict with validation result + timestamp
LICENSE_CACHE = {}
CACHE_TTL_SECONDS = 300  # 5 minutes


def require_license(f):
    """Decorator to validate license key via Lemonsqueezy."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        license_key = request.headers.get('X-License-Key')

        if not license_key:
            return jsonify({
                'error': 'Missing X-License-Key header',
                'message': 'A valid Lemonsqueezy license key is required'
            }), 401

        # Debug mode: allow any key
        if DEBUG:
            return f(*args, **kwargs)

        # Check cache first
        cached = LICENSE_CACHE.get(license_key)
        if cached:
            age = (datetime.utcnow() - cached['checked_at']).total_seconds()
            if age < CACHE_TTL_SECONDS:
                if cached['valid']:
                    return f(*args, **kwargs)
                else:
                    return jsonify({
                        'error': 'Invalid license key',
                        'message': 'The provided license key is not valid'
                    }), 403

        # Validate against Lemonsqueezy
        is_valid, data = license_validator.validate_license(license_key)

        # Cache the result
        LICENSE_CACHE[license_key] = {
            'valid': is_valid,
            'data': data,
            'checked_at': datetime.utcnow()
        }

        if not is_valid:
            return jsonify({
                'error': 'Invalid license key',
                'message': data.get('error', 'The provided license key is not valid')
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
                '2 months free'
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
                '2 months free'
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

    # Map product to Lemonsqueezy checkout variant ID
    variants = {
        'individual_monthly': '1314502',
        'individual_yearly': '1314393',
        'team_monthly': '1314579',
        'team_yearly': '1314510'
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
def validate_license_endpoint():
    """Validate a license key against Lemonsqueezy."""
    data = request.get_json() or {}
    license_key = data.get('license_key')
    instance_id = data.get('instance_id')

    if not license_key:
        return jsonify({
            'error': 'Missing license_key',
            'message': 'Please provide a license_key in the request body'
        }), 400

    is_valid, result = license_validator.validate_license(license_key, instance_id)

    if is_valid:
        # Cache it
        LICENSE_CACHE[license_key] = {
            'valid': True,
            'data': result,
            'checked_at': datetime.utcnow()
        }

        license_info = result.get('license_key', {})
        meta = result.get('meta', {})

        return jsonify({
            'valid': True,
            'license_key': license_info.get('key'),
            'status': license_info.get('status'),
            'activation_limit': license_info.get('activation_limit'),
            'activation_usage': license_info.get('activation_usage'),
            'product': meta.get('product_name'),
            'customer_email': meta.get('customer_email'),
            'expires_at': license_info.get('expires_at'),
        }), 200

    return jsonify({
        'valid': False,
        'error': result.get('error', 'Invalid license key')
    }), 400


@app.route('/api/v1/license/activate', methods=['POST'])
def activate_license_endpoint():
    """Activate a license key for a specific instance."""
    data = request.get_json() or {}
    license_key = data.get('license_key')
    instance_name = data.get('instance_name', 'default')

    if not license_key:
        return jsonify({
            'error': 'Missing license_key',
            'message': 'Please provide a license_key in the request body'
        }), 400

    is_activated, result = license_validator.activate_license(license_key, instance_name)

    if is_activated:
        instance = result.get('instance', {})
        return jsonify({
            'activated': True,
            'instance_id': instance.get('id'),
            'instance_name': instance.get('name'),
        }), 200

    return jsonify({
        'activated': False,
        'error': result.get('error', 'Activation failed')
    }), 400


@app.route('/api/v1/webhook/lemonsqueezy', methods=['POST'])
def webhook_handler():
    """Handle Lemonsqueezy webhooks for order/subscription/license events."""
    # Verify signature if secret is configured
    if LEMONSQUEEZY_WEBHOOK_SECRET:
        signature = request.headers.get('X-Signature', '')
        raw_body = request.get_data()

        if not verify_webhook_signature(raw_body, signature, LEMONSQUEEZY_WEBHOOK_SECRET):
            print('Webhook signature verification FAILED')
            return jsonify({'error': 'Invalid signature'}), 401

    data = request.get_json() or {}
    event_name = request.headers.get('X-Event-Name') or data.get('meta', {}).get('event_name', 'unknown')

    print(f'Webhook received: {event_name}')

    attrs = data.get('data', {}).get('attributes', {})

    if event_name == 'order_created':
        print(f'  Order #{attrs.get("order_number")} from {attrs.get("user_email")} '
              f'- {attrs.get("status")} - {attrs.get("total_formatted")}')

    elif event_name == 'license_key_created':
        key = attrs.get('key', '')
        email = attrs.get('user_email', '')
        product_id = str(attrs.get('product_id', ''))
        plan = VARIANT_PRODUCTS.get(product_id, 'unknown')
        print(f'  License created: {key[:8]}... for {email} ({plan})')

        # Pre-cache the new license as valid
        LICENSE_CACHE[key] = {
            'valid': True,
            'data': {'license_key': attrs, 'meta': {'product_id': product_id}},
            'checked_at': datetime.utcnow()
        }

    elif event_name == 'subscription_updated':
        status = attrs.get('status', '')
        print(f'  Subscription updated: {status}')

    elif event_name == 'subscription_cancelled':
        print(f'  Subscription cancelled for customer {attrs.get("customer_id")}')
        # Invalidate any cached licenses for this subscription
        # (next validation call will hit Lemonsqueezy and get the real status)
        LICENSE_CACHE.clear()

    elif event_name == 'subscription_expired':
        print(f'  Subscription expired for customer {attrs.get("customer_id")}')
        LICENSE_CACHE.clear()

    return jsonify({'received': True, 'event': event_name}), 200


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
