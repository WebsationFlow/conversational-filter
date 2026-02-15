"""
ConversationalFilter Commercial Licensing Module

Handles license verification, key generation, and subscription management.
Integrates with Lemonsqueezy for automated billing.
"""

import os
import hmac
import hashlib
import json
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
try:
    import requests
except ImportError:
    requests = None


class LicenseValidator:
    """Validates commercial licenses for ConversationalFilter."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize license validator.

        Args:
            api_key: API key for Lemonsqueezy
        """
        self.api_key = api_key or os.getenv('LEMONSQUEEZY_API_KEY')
        self.api_base = 'https://api.lemonsqueezy.com/v1'

    def validate_license(self, license_key: str) -> Tuple[bool, Dict]:
        """
        Validate a license key.

        Args:
            license_key: The license key to validate

        Returns:
            Tuple of (is_valid, license_info)
        """
        if not self.api_key or not requests:
            return False, {'error': 'No API key or requests library'}

        try:
            response = requests.get(
                f"{self.api_base}/licenses/validate",
                headers={'Authorization': f'Bearer {self.api_key}'},
                params={'license_key': license_key},
                timeout=5
            )

            if response.status_code == 200:
                data = response.json()
                return True, data
            else:
                return False, {'error': 'Invalid license key'}

        except Exception as e:
            return False, {'error': str(e)}

    def check_subscription_active(self, license_key: str) -> bool:
        """Check if a subscription is active (not expired/cancelled)."""
        is_valid, license_info = self.validate_license(license_key)

        if not is_valid:
            return False

        # Check expiration
        if 'expires_at' in license_info:
            try:
                expires_at = datetime.fromisoformat(license_info['expires_at'])
                if datetime.now() > expires_at:
                    return False
            except (ValueError, TypeError):
                pass

        # Check if cancelled
        if license_info.get('status') == 'cancelled':
            return False

        return True

    def get_license_info(self, license_key: str) -> Optional[Dict]:
        """Get full license information."""
        is_valid, info = self.validate_license(license_key)
        return info if is_valid else None


class LemonsqueezyIntegration:
    """Handles Lemonsqueezy integration for automated billing."""

    PRODUCTS = {
        'individual_monthly': {
            'name': 'Individual Monthly',
            'price': 99,
            'currency': 'USD',
            'interval': 'month',
        },
        'individual_yearly': {
            'name': 'Individual Yearly',
            'price': 990,
            'currency': 'USD',
            'interval': 'year',
        },
        'team_monthly': {
            'name': 'Team Monthly',
            'price': 499,
            'currency': 'USD',
            'interval': 'month',
        },
        'team_yearly': {
            'name': 'Team Yearly',
            'price': 4990,
            'currency': 'USD',
            'interval': 'year',
        },
    }

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('LEMONSQUEEZY_API_KEY')
        self.store_id = os.getenv('LEMONSQUEEZY_STORE_ID')
        self.api_base = 'https://api.lemonsqueezy.com/v1'

    def create_checkout(
        self,
        product_id: str,
        customer_email: str = None
    ) -> Optional[str]:
        """
        Create a checkout URL for a product.

        Args:
            product_id: Lemonsqueezy product ID
            customer_email: Optional customer email

        Returns:
            Checkout URL or None if failed
        """
        if not requests or not self.api_key or not self.store_id:
            return None

        try:
            payload = {
                'data': {
                    'type': 'checkouts',
                    'attributes': {
                        'product_id': product_id,
                    }
                }
            }

            if customer_email:
                payload['data']['attributes']['customer_email'] = customer_email

            response = requests.post(
                f"{self.api_base}/stores/{self.store_id}/checkouts",
                headers={
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/vnd.api+json',
                },
                json=payload,
                timeout=10
            )

            if response.status_code == 201:
                return response.json()['data']['attributes']['url']

        except Exception as e:
            print(f"Error creating checkout: {e}")

        return None

    def webhook_verify(self, body: str, signature: str, secret: str) -> bool:
        """Verify a Lemonsqueezy webhook signature."""
        hash_obj = hmac.new(
            secret.encode(),
            body.encode(),
            hashlib.sha256
        )
        expected_sig = hash_obj.hexdigest()
        return hmac.compare_digest(signature, expected_sig)


if __name__ == "__main__":
    print("ConversationalFilter Licensing System")
    print("Available products:")
    for key, product in LemonsqueezyIntegration.PRODUCTS.items():
        print(f"  {key}: {product['name']} (${product['price']})")
