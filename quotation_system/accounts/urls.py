from django.urls import path

from .views import AccountDetailView, AccountListView

urlpatterns = [
    path("", AccountListView.as_view(), name="account-list"),
    path("<int:pk>", AccountDetailView.as_view(), name="account-detail"),
]
