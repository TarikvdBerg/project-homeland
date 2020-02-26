from django.urls import include, path
from knox import views as knox_views
from rest_framework import routers

from Core.views import LoginView
from Core.viewsets import (PasswordGroupViewSet, PasswordViewSet,
                           SCTFUserViewSet)

router = routers.DefaultRouter()
router.register(r'users', SCTFUserViewSet)
router.register(r'pw_groups', PasswordGroupViewSet)
router.register(r'passwords', PasswordViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('auth/login', LoginView.as_view(), name="knox_login"),
    path('auth/logout', knox_views.LogoutView.as_view(), name="knox_logout"),
    path('auth/logoutall', knox_views.LogoutAllView.as_view(), name="knox_logoutall"),
]
