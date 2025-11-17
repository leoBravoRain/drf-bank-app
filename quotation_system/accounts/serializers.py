from rest_framework import serializers

from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Account
        fields = "__all__"
        read_only_fields = ["user", "balance"]


class AccountUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ("account_name",)


class AccountListSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Account
        fields = ("id", "account_name", "currency", "balance", "user")
