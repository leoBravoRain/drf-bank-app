from rest_framework import generics, permissions

from .models import Account
from .serializers import AccountSerializer


class AccountListView(generics.ListCreateAPIView):
    """
    Create a new account for a user.
    List all accounts for a user.
    """

    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, balance=0)

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user).order_by("account_number")
