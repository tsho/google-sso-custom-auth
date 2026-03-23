import os

import firebase_admin
from firebase_admin import credentials


def initialize_firebase() -> None:
    """Initialize Firebase Admin SDK with service account credentials."""
    if firebase_admin._apps:
        return

    cred_path = os.environ.get(
        "GOOGLE_APPLICATION_CREDENTIALS", "serviceAccountKey.json"
    )
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)
