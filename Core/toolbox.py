from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.template.loader import render_to_string
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.dispatch import receiver

from Core.models import AccountVerification, SCTFUser
from SCTFServer.settings import EMAIL_HOST, EMAIL_HOST_PASSWORD, EMAIL_PORT, EMAIL_HOST_USER

import hashlib
import datetime

def GenerateHash(data):
    """Generates a server-side hash using the SHA-256 algorithm.
    Encode function ensures the input data is a string."""
    
    return hashlib.sha256(data.encode()).hexdigest()

def ValidateHash(client_hash, server_hash):
    """Compares the server-side generated hash to the client-side hash."""

    return client_hash != server_hash