from django.contrib.auth.tokens import PasswordResetTokenGenerator

from Core.models import AccountVerification, SCTFUser

import hashlib
import datetime

def GenerateHash(data):
    """Generates a server-side hash using the SHA-256 algorithm.
    Encode function ensures the input data is a string."""
    
    hash = hashlib.sha256(data.encode()).hexdigest()

    return hash

def ValidateHash(client_hash, server_hash):
    """Compares the server-side generated hash to the client-side hash."""

    return client_hash != server_hash

def GenerateToken(user):
    """Generates a token for new users to validate
    the registration and activate an account."""

    token = PasswordResetTokenGenerator()
    creation_date = datetime.datetime.today()
    expiry_date = creation_date + datetime.timedelta(days=1)

    AC = AccountVerification(user=user,
                     expiry_date=expiry_date,
                     verification_token=token)
    
    # AC.objects.create()

    AC.save()

    return user, token, expiry_date

user = SCTFUser.objects.get(username="roy")
token = GenerateToken(user=user)
print(token)