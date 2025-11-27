from http import HTTPMethod
from typing import Any

from django.contrib.auth.models import User
from rest_framework import generics, permissions, serializers

from ..notifications.email_producer import publish_email
from ..notifications.kafka_event_producer import send_event
from .models import Account
from .serializers import (
    AccountListSerializer,
    AccountSerializer,
    AccountUpdateSerializer,
)


class AccountListView(generics.ListCreateAPIView):
    """
    Create a new account for a user.
    List all accounts for a user.
    """

    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self) -> Any:
        if self.request.method == HTTPMethod.GET:
            return AccountListSerializer
        return AccountSerializer

    def perform_create(self, serializer):

        serializer.save(user=self.request.user, balance=0)

        print(self)

        # get user for send email
        user = User.objects.get(username=self.request.user)

        # publish emeail on rabbit mq
        # publish_email(
        #     {
        #         "to": user.email,
        #         "template": "new_account",
        #         "data": serializer.validated_data,
        #     }
        # )

        # send event to kafka
        send_event("account", "created", user.id, serializer.validated_data)

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user).order_by("account_number")


class AccountDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Get, update or destroy an account
    """

    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)

    def get_serializer_class(self) -> Any:
        if self.request.method == HTTPMethod.PATCH:
            return AccountUpdateSerializer
        return AccountSerializer

    def perform_destroy(self, instance: Account) -> None:
        """
        Only accounts with balace 0 can be deleted.
        """
        if instance.balance != 0:
            raise serializers.ValidationError(
                "This account can not be deleted because balance is not zero"
            )
        return super().perform_destroy(instance)
