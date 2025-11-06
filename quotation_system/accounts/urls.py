from django.urls import path
from .views import CreateAccountView

urlpatterns = [
    path('', CreateAccountView.as_view(), name='create_account'),
]