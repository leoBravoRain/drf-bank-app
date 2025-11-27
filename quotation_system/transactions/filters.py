import django_filters

from .models import Transaction


class TransactionFilter(django_filters.FilterSet):

    account_id = django_filters.NumberFilter(field_name="account")
    type = django_filters.ChoiceFilter(
        field_name="transaction_type",
        choices=Transaction.TRANSACTION_TYPES,
    )

    class Meta:
        model = Transaction
        fields = ("account_id", "type")
