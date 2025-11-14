from django.urls import path

from .views import LoginView, RefreshTokenView, SignUpView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("refresh/", RefreshTokenView.as_view(), name="refresh"),
]
