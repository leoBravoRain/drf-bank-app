from rest_framework import serializers

from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"
        read_only_fields = ["user", "previous_balance", "new_balance"]
        extra_kwargs = {"currency": {"required": False, "allow_blank": True}}

        def validate(self, attrs):
            tx_type = attrs.get("transaction_type")
            currency = attrs.get("currency")
            if (
                tx_type
                in {
                    Transaction.TRANSACTION_TYPES[0][0],
                    Transaction.TRANSACTION_TYPES[1][0],
                }
                and not currency
            ):
                raise serializers.ValidationError(
                    {"currency": "Required for deposit and withdrawal"}
                )
            return attrs
