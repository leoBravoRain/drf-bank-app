from unittest.mock import MagicMock, create_autospec

import pytest
from rest_framework import serializers

from .....accounts.models import Account
from ....models import Transaction
from ....serializers import TransactionSerializer
from ..configtest import api_factory, mock_atomic, user, view


@pytest.mark.unit
def test_perform_create_withdrawal_sets_user_and_update_account_balance(
    api_factory, user, view, mocker, mock_atomic
):

    # arrange
    transaction_amount = 50
    account_balance = 100

    data = {
        "transaction_type": Transaction.TRANSACTION_TYPES[1][0],
        "account": 1,
        "amount": transaction_amount,
        "currency": "USD",
    }
    # create request obejct
    request = api_factory.post(
        "/",
        data,
        format="json",
    )
    request.user = user
    view.request = view.initialize_request(request)

    # mock get account
    mock_select_for_update = mocker.patch(
        "quotation_system.transactions.views.Account.objects.select_for_update"
    )

    # define account
    account = MagicMock(spec=Account)
    account.balance = account_balance
    account.id = 1
    account.currency = "USD"

    # assign the account ot the returned vallue of the Account.objects.select_for_update().get() mock
    mock_select_for_update.return_value.get.return_value = account

    # create serializer object
    serializer = create_autospec(TransactionSerializer, instance=True)
    serializer.validated_data = {"amount": data["amount"], "currency": data["currency"]}

    # act
    view.perform_create(serializer)

    # assert
    assert serializer.save.call_count == 1
    assert account.save.call_count == 1
    mock_atomic.assert_called_once()

    # check balance was updated
    assert account.balance == data["amount"]
    assert serializer.validated_data["previous_balance"] == account_balance
    assert (
        serializer.validated_data["new_balance"] == account_balance - transaction_amount
    )


@pytest.mark.unit
def test_perform_create_withdrawal_with_not_enough_balance(
    api_factory, user, view, mocker, mock_atomic
):

    # arrange
    transaction_amount = 100
    account_balance = 50

    data = {
        "transaction_type": Transaction.TRANSACTION_TYPES[1][0],
        "account": 1,
        "amount": transaction_amount,
        "currency": "USD",
    }

    request = api_factory.post("/", data, format="json")
    view.request = view.initialize_request(request)
    view.request.user = user  # assign after initialize_request

    # mock get account
    mock_select_for_update = mocker.patch(
        "quotation_system.transactions.views.Account.objects.select_for_update"
    )

    # define account
    account = MagicMock(spec=Account, balance=account_balance, id=1, currency="USD")

    # assign the account ot the returned vallue of the Account.objects.select_for_update().get() mock
    mock_select_for_update.return_value.get.return_value = account

    # create serializer object
    serializer = create_autospec(TransactionSerializer, instance=True)
    serializer.validated_data = {"amount": data["amount"], "currency": data["currency"]}

    # act
    with pytest.raises(serializers.ValidationError) as e:
        view.perform_create(serializer)

    # assert
    assert e.value.detail[0] == "Insufficient balance"
    assert serializer.save.call_count == 0
    assert account.save.call_count == 0
    mock_atomic.assert_called_once()
