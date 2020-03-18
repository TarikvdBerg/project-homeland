from django.contrib.auth import login
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.template.loader import render_to_string, get_template
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.dispatch import receiver

from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView

from Core.models import AccountVerification, SCTFUser
from Core.serializers import SCTFUserSerializer
from SCTFServer.settings import EMAIL_HOST, EMAIL_HOST_PASSWORD, EMAIL_PORT, EMAIL_HOST_USER

import hashlib
import datetime

class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)

@receiver(post_save, sender=SCTFUser)
def GenerateToken(sender, instance, **kwargs):
    """Generates a token for new users to validate
    the registration and activate an account."""

    token = PasswordResetTokenGenerator().make_token(instance)
    creation_date = datetime.datetime.today()
    expiry_date = creation_date + datetime.timedelta(days=1)

    AC = AccountVerification(user=instance,
                     expiry_date=expiry_date,
                     verification_token=token)

    AC.save()

    return instance, token, expiry_date

@receiver(post_save, sender=SCTFUser)
def ActivationEmail(sender, instance, **kwargs):
    """Sends an activation email to the user."""

    UserEmail = instance.email
    ActivationURL = "http://localhost:8000/activate/"

    send_mail(subject="Activate your FirstPass account!",
              from_email=EMAIL_HOST_USER,
              recipient_list=[UserEmail],

              # To do:
              # Add activation token to email input.
              # Create model for Activation & URL.
              # Add HTML template to model (later).

              message=render_to_string("activation_message.txt"),
            #   html_message=activation_email.html,

              fail_silently=False,
              auth_user=EMAIL_HOST_USER,
              auth_password=EMAIL_HOST_PASSWORD
)

# def VerifyAccountToken():