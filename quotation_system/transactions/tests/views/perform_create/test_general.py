from unittest.mock import MagicMock, call, create_autospec

import pytest
from rest_framework import serializers

from .....accounts.models import Account
from ....serializers import TransactionSerializer
from ..configtest import api_factory, mock_atomic, user, view


@pytest.mark.unit
def test_perform_create_with_invalid_transaction_type(
    api_factory, user, view, mocker, mock_atomic
):

    # # arrange
    data = {
        "transaction_type": "invalid_transaction_type",
        "account": 1,
        "amount": 100,
        "currency": "USD",
    }

    request = api_factory.post("/", data, format="json")
    view.request = view.initialize_request(request)
    view.request.user = user  # assign after initialize_request

    mock_select_for_update = mocker.patch(
        "quotation_system.transactions.views.Account.objects.select_for_update",
    )
    mock_select_for_update.return_value.get.return_value = MagicMock(spec=Account)

    serializer = create_autospec(TransactionSerializer, instance=True)
    serializer.validated_data = {"amount": data["amount"], "currency": data["currency"]}

    with pytest.raises(serializers.ValidationError):
        view.perform_create(serializer)

    mock_select_for_update.return_value.get.assert_called_once_with(
        user=user, pk=data["account"]
    )
    serializer.save.assert_not_called()
    mock_atomic.assert_called_once()
