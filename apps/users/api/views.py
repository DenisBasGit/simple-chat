from django.utils.decorators import method_decorator
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.users.api.docs import AuthorizationSwagger, RefreshSwagger


@method_decorator(AuthorizationSwagger.extend_schema, name="post")
class LoginUserAPIView(TokenObtainPairView):
    """Method for login user"""


@method_decorator(RefreshSwagger.extend_schema, name="post")
class RefreshUserAPIView(TokenRefreshView):
    """Method for refresh token"""
