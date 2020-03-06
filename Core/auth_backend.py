from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from rest_framework.authentication import TokenAuthentication
from Core.models import SCTFUser


class SCTFAuthBackend(BaseBackend):
    """
    The SCTFAuthBackend implements the SCTFUser with additional authentication requirements
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Try to retrieve user
        try:
            u = SCTFUser.objects.get(username=username)
        except SCTFUser.DoesNotExist:
            return None

        # Verify is_verified
        if not u.is_verified:
            return None

        if not check_password(password, u.password):
            return None
        return u

    def get_user(self, user_id):
        try:
            return SCTFUser.objects.get(pk=user_id)
        except SCTFUser.DoesNotExist:
                return None