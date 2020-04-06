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
    email = models.EmailField(('email'), unique=True)
    new_password = models.CharField(max_length=255, blank=True, null=True)

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

    def __str__(self):
        return self.verification_token

class PasswordGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    enc_name = models.TextField()
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)

class Password(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    enc_name = models.TextField()
    enc_description = models.TextField()
    enc_username = models.TextField()
    enc_password = models.TextField()

    parent_group = models.ForeignKey("Core.PasswordGroup", on_delete=models.CASCADE)

class Activate(models.Model):
    """
    Model for handling the account activation.
    URL: 127.0.0.1/activate
    """

    Token = models.CharField(max_length=24)