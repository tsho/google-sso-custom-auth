import hashlib
import hmac
import os

import requests
from firebase_admin import auth as firebase_auth
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token

GOOGLE_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"


def exchange_code_for_sub(code: str) -> str:
    """Exchange an authorization code for tokens and return the subject.

    Uses the auth code flow with scope=openid only, so Google never
    exposes email or profile info to the consent screen.
    """
    resp = requests.post(
        GOOGLE_TOKEN_ENDPOINT,
        data={
            "code": code,
            "client_id": os.environ["GOOGLE_CLIENT_ID"],
            "client_secret": os.environ["GOOGLE_CLIENT_SECRET"],
            "redirect_uri": "postmessage",
            "grant_type": "authorization_code",
        },
    )
    resp.raise_for_status()

    id_token_str = resp.json()["id_token"]
    id_info = id_token.verify_oauth2_token(
        id_token_str, google_requests.Request(), os.environ["GOOGLE_CLIENT_ID"]
    )
    return id_info["sub"]


def anonymize_uid(google_sub: str) -> str:
    """Generate an anonymized UID using HMAC-SHA256.

    Returns a 64-character hex string that is deterministic but irreversible.
    """
    secret = os.environ["SECRET_SALT"]
    return hmac.new(
        secret.encode(), google_sub.encode(), hashlib.sha256
    ).hexdigest()


def create_firebase_custom_token(uid: str) -> str:
    """Create a Firebase custom token for the given UID."""
    token = firebase_auth.create_custom_token(uid)
    return token.decode() if isinstance(token, bytes) else token
