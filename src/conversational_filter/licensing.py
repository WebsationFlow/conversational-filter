"""
ConversationalFilter Commercial Licensing Module

Handles license verification and subscription management.
Integrates with Lemonsqueezy for automated billing.
"""

import os
import hmac
import hashlib
from datetime import datetime
from typing import Dict, Optional, Tuple
try:
    import requests
except ImportError:
    requests = None


class LicenseValidator:
    """Validates commercial licenses against Lemonsqueezy's License API."""

    VALIDATE_URL = 'https://api.lemonsqueezy.com/v1/licenses/validate'
    ACTIVATE_URL = 'https://api.lemonsqueezy.com/v1/licenses/activate'
    DEACTIVATE_URL = 'https://api.lemonsqueezy.com/v1/licenses/deactivate'

    def validate_license(self, license_key: str, instance_id: str = None) -> Tuple[bool, Dict]:
        """
        Validate a license key against Lemonsqueezy.

        This is a keyless API — no Bearer token needed.
        """
        if not requests:
            return False, {'error': 'requests library not available'}

        try:
            payload = {'license_key': license_key}
            if instance_id:
                payload['instance_id'] = instance_id

            response = requests.post(
                self.VALIDATE_URL,
                headers={'Accept': 'application/json'},
                data=payload,
                timeout=10
            )

            data = response.json()

            if response.status_code == 200 and data.get('valid'):
                return True, data
            else:
                return False, data

        except Exception as e:
            return False, {'error': str(e)}

    def activate_license(self, license_key: str, instance_name: str) -> Tuple[bool, Dict]:
        """Activate a license key for a specific instance."""
        if not requests:
            return False, {'error': 'requests library not available'}

        try:
            response = requests.post(
                self.ACTIVATE_URL,
                headers={'Accept': 'application/json'},
                data={
                    'license_key': license_key,
                    'instance_name': instance_name,
                },
                timeout=10
            )

            data = response.json()

            if response.status_code == 200 and data.get('activated'):
                return True, data
            else:
                return False, data

        except Exception as e:
            return False, {'error': str(e)}

    def deactivate_license(self, license_key: str, instance_id: str) -> Tuple[bool, Dict]:
        """Deactivate a license key instance."""
        if not requests:
            return False, {'error': 'requests library not available'}

        try:
            response = requests.post(
                self.DEACTIVATE_URL,
                headers={'Accept': 'application/json'},
                data={
                    'license_key': license_key,
                    'instance_id': instance_id,
                },
                timeout=10
            )

            data = response.json()

            if response.status_code == 200 and data.get('deactivated'):
                return True, data
            else:
                return False, data

        except Exception as e:
            return False, {'error': str(e)}

    def check_subscription_active(self, license_key: str) -> bool:
        """Check if a subscription license is active (not expired/cancelled)."""
        is_valid, data = self.validate_license(license_key)

        if not is_valid:
            return False

        license_info = data.get('license_key', {})

        # Check status
        if license_info.get('status') != 'active':
            return False

        # Check expiration
        expires_at = license_info.get('expires_at')
        if expires_at:
            try:
                exp = datetime.fromisoformat(expires_at.replace('Z', '+00:00'))
                if datetime.now(exp.tzinfo) > exp:
                    return False
            except (ValueError, TypeError):
                pass

        return True


def verify_webhook_signature(body: bytes, signature: str, secret: str) -> bool:
    """Verify a Lemonsqueezy webhook X-Signature header (HMAC-SHA256)."""
    expected = hmac.new(
        secret.encode('utf-8'),
        body,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(signature, expected)


VARIANT_PRODUCTS = {
    '1314502': 'individual_monthly',
    '1314393': 'individual_yearly',
    '1314579': 'team_monthly',
    '1314510': 'team_yearly',
}


if __name__ == "__main__":
    print("ConversationalFilter Licensing System")
    print("License API endpoints:")
    print(f"  Validate: {LicenseValidator.VALIDATE_URL}")
    print(f"  Activate: {LicenseValidator.ACTIVATE_URL}")
    print(f"  Deactivate: {LicenseValidator.DEACTIVATE_URL}")
