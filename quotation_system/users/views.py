from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


# TODO: add typing?
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
