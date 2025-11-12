from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import UserSerializer


class LoginView(TokenObtainPairView):
    """
    View for user login.
    Returns access and refresh tokens.
    """

    pass


class RefreshTokenView(TokenRefreshView):
    """
    View for refreshing access tokens.
    """

    pass


class SignUpView(generics.CreateAPIView):
    """
    View for signun up a new user.
    """

    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
