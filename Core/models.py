import binascii
import os
import uuid

from django.contrib.auth.models import *
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from SCTFServer.settings import AUTH_USER_MODEL


class SCTFUser(AbstractUser):
    """
    Extends the base Django User, the SCTFUser has additional properties for
    integration with the SCTF Password Manager. The settings file will specify the
    AUTH_USER_MODEL. When creating foreign keys to this object please import from
    SCTFServer.AUTH_USER_MODEL instead of directly linking to this class.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    is_verified = models.BooleanField(default=False)

    @property
    def display_name(self):
        return " ".join([self.first_name, self.last_name])
    
    class Meta:
        permissions = [
            # GodMode Permissions
            ('view_all_users', 'Can view all users in database'),
            ('edit_all_users', 'Can edit all the users'),
            ('delete_all_users', "Can delete any and all users"),
            
            # Normal Permissinos
            ('view_own_user', 'Can view own user information'),
            ('edit_own_user', 'Can edit own user information'),
            ('delete_own_user', 'Can delete own user information'),
        ]

class AccountVerification(models.Model):
    """
    AccountVerification is an extra step in the signup stage to ensure the
    user is legitimate.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    verification_token = models.CharField(max_length=512)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    expiry_date = models.DateTimeField()

class PasswordGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    enc_name = models.TextField()
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)

class Password(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    enc_name = models.TextField()
    enc_description = models.TextField()
    enc_password = models.TextField()

    parent_group = models.ForeignKey("Core.PasswordGroup", on_delete=models.CASCADE)

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.template.loader import render_to_string
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.dispatch import receiver

from Core.models import AccountVerification, SCTFUser
from SCTFServer.settings import EMAIL_HOST, EMAIL_HOST_PASSWORD, EMAIL_PORT, EMAIL_HOST_USER

import hashlib
import datetime

@receiver(post_save, sender=SCTFUser)
def GenerateToken(sender, instance, **kwargs):
    """Generates a token for new users to validate
    the registration and activate an account."""

    print('hallo')

    token = PasswordResetTokenGenerator().make_token(instance)
    creation_date = datetime.datetime.today()
    expiry_date = creation_date + datetime.timedelta(days=1)

    AC = AccountVerification(user=instance,
                     expiry_date=expiry_date,
                     verification_token=token)

    AC.save()

    # send_mail(
    #     subject='Activate your FirstPass account!',
    #     from_email = 'supercybertaskforce@gmail.com',
    #     recipient_list = SCTFUser.email,

    #     message='Hello there.',
    #     html_message=render_to_string('activation_email.html'),

    #     fail_silently=False,
        
    #     auth_user=EMAIL_HOST_USER,
    #     auth_password=EMAIL_HOST_PASSWORD)

    return instance, token, expiry_date


# TEST_TOKEN = PasswordResetTokenGenerator().make_token('john')
# print(TEST_TOKEN)