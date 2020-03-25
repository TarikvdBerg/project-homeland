from django.contrib.auth import login
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.template.loader import render_to_string, get_template
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.dispatch import receiver
from django.http import HttpResponse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import View
from django.shortcuts import render

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

class ActivateView(View):

    def get(self, request):
        return render(request, "activation_email.html")        

@receiver(post_save, sender=SCTFUser)
def SendActivationEmail(sender, instance, **kwargs):
    """Sends an activation email to the user."""

    creation_date = datetime.datetime.today()
    expiry_date = creation_date + datetime.timedelta(days=1)

    AC = AccountVerification(user=instance,
                     expiry_date=expiry_date,
                     verification_token=PasswordResetTokenGenerator().make_token(instance))

    AC.save()

    send_mail(subject="Activate your FirstPass account!",
              from_email=EMAIL_HOST_USER,
              recipient_list=[instance.email],

              # To do:
              # Create /activate with HTML template.

            #   message=render_to_string("activation_message.txt", {
            #       'user': instance.username,
            #       'url':'http://localhost:8000/activate/',
            #       'token':AC.verification_token,
            #   }),

              message=None,
              html_message=render_to_string("activation_email.html"),

              fail_silently=False,
              auth_user=EMAIL_HOST_USER,
              auth_password=EMAIL_HOST_PASSWORD
)


# @receiver(post_save, sender=SendActivationEmail)
# def ActivateHTML(request)


