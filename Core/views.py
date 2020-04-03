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

    def get(self, request, uid):
        return render(request, "activation_page.html")

    def post(self, request, uid):

        print(request.POST)

        # To do: compare token to stored AC token.
        # Activate account = is_active = True.

        InputToken = request.POST['token']

        return HttpResponse("Your account has been activated.")      

@receiver(post_save, sender=SCTFUser)
def SendActivationEmail(sender, created, instance, **kwargs):
    """Sends an activation email to the user."""

    if created:

        # Stamps the token with a creation date & expiry date (1 day).
        creation_date = datetime.datetime.today()
        expiry_date = creation_date + datetime.timedelta(days=1)

        # Saves information received from SCTFUser to model.
        AC = AccountVerification(user=instance,
                        expiry_date=expiry_date,

                        # Creates token in AC save.
                        verification_token=PasswordResetTokenGenerator().make_token(instance))

        AC.save()

        # Creates base64 string to identify user with.
        uid = urlsafe_base64_encode(force_bytes(instance.username))

        send_mail(subject="Activate your FirstPass account!",
                from_email=EMAIL_HOST_USER,
                recipient_list=[instance.email],

                message=None,
                html_message=render_to_string("activation_email.html", {
                    'user': instance.username,
                    'token': AC.verification_token,
                    'link': "http://localhost:8000/activate/{0}".format(uid),
                }),

                # Fix server-side password saving later.
                fail_silently=False,
                auth_user=EMAIL_HOST_USER,
                auth_password=EMAIL_HOST_PASSWORD)