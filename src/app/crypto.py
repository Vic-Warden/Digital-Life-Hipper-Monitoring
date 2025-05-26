import hmac
import hashlib
import base64
import time
import os

HOUR = 3600
DAY = 24 * HOUR
WEEK = 7 * DAY
MONTH = 30 * DAY


class Cookie:
    def __init__(self):
        self.secret_key = base64.urlsafe_b64encode(os.urandom(32)).decode()

    def compute(self, data: str) -> str:
        return hashlib.sha256(data.encode()).hexdigest()

    def create_cookie(self, value: str) -> tuple[bool, str]:
        """
        Create a signed cookie with value and expiration.

        The cookie format is: value|expires|signature

        Returns a tuple (True, cookie) if successful.
        """
        expires = int(time.time()) + WEEK  # Expires in one week
        payload = f"{value}|{expires}"

        signature = hmac.new(self.secret_key, payload.encode(),
                             hashlib.sha256).digest()
        signature_b64 = base64.urlsafe_b64encode(signature).decode()

        cookie = f"{payload}|{signature_b64}"
        return (True, cookie)

    def verify_cookie(self, cookie: str) -> tuple[bool, str]:
        """
        Verify a signed cookie and return the value if valid.

        Raises ValueError if the cookie is invalid or expired.

        The cookie format is: value|expires|signature

        Returns boolean indicating whether the cookie is valid,
        """
        try:
            value, expires, signature_b64 = cookie.rsplit("|", 2)
            payload = f"{value}|{expires}"
            expected_signature = hmac.new(
                self.secret_key, payload.encode(), hashlib.sha256).digest()
            actual_signature = base64.urlsafe_b64decode(signature_b64.encode())

            if not hmac.compare_digest(expected_signature, actual_signature):
                return (False, "Invalid signature")

            if int(expires) < time.time():
                return (False, "Expired cookie")

            return (True, "")
        except Exception as e:
            return (False, f"Invalid cookie: {e}")
