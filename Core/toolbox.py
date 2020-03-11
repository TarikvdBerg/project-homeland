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
    
    hash = hashlib.sha256(data.encode()).hexdigest()

    return hash

def ValidateHash(client_hash, server_hash):
    """Compares the server-side generated hash to the client-side hash."""

    return client_hash != server_hash

@receiver(post_save, sender=SCTFUser)
def GenerateToken(sender, instance, **kwargs):
    """Generates a token for new users to validate
    the registration and activate an account."""

    print('hallo')

    token = PasswordResetTokenGenerator()
    creation_date = datetime.datetime.today()
    expiry_date = creation_date + datetime.timedelta(days=1)

    AC = AccountVerification(user=instance,
                     expiry_date=expiry_date,
                     verification_token=token)

    AC.save()

    send_mail(
        subject='Activate your FirstPass account!',
        from_email = 'supercybertaskforce@gmail.com',
        recipient_list = SCTFUser.email,

        message=render_to_string('activate_email.html'),
        html_message=render_to_string('activate_email.html'),

        fail_silently=False,
        
        auth_user=EMAIL_HOST_USER,
        auth_password=EMAIL_HOST_PASSWORD)

    return instance, token, expiry_date