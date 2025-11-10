from unittest.mock import MagicMock, create_autospec

import pytest

from .....accounts.models import Account
from ....models import Transaction
from ....serializers import TransactionSerializer
from ..configtest import api_factory, mock_atomic, user, view


@pytest.mark.unit
def test_perform_create_deposit_sets_user_and_update_account_balance(
    api_factory, user, view, mocker, mock_atomic
):

    # arrange
    transaction_amount = 100
    account_balance = 0

    data = {
        "transaction_type": Transaction.TRANSACTION_TYPES[0][0],
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

    # assign the account to the returned value of the Account.objects.select_for_update().get() mock
    mock_select_for_update.return_value.get.return_value = account

    # create serializer object
    serializer = create_autospec(TransactionSerializer, instance=True)
    serializer.validated_data = {"amount": data["amount"], "currency": data["currency"]}

    # act
    view.perform_create(serializer)

    # assert
    serializer.save.assert_called_once()
    account.save.assert_called_once()
    mock_atomic.assert_called_once()

    # check balance was updated
    assert account.balance == data["amount"]
    assert serializer.validated_data["previous_balance"] == account_balance
    assert (
        serializer.validated_data["new_balance"] == account_balance + transaction_amount
    )


@pytest.mark.unit
def test_perform_create_deposit_with_different_currency(
    api_factory, user, view, mocker, mock_atomic
):

    # arrange

    # trx info
    transaction_amount = 1
    trx_currency = "USD"

    # account info
    account_balance = 0
    account_currency = "CLP"

    # rate info
    # USD -> CLP
    currency_rate = 0.0011

    data = {
        "transaction_type": Transaction.TRANSACTION_TYPES[0][0],
        "account": 1,
        "amount": transaction_amount,
        "currency": trx_currency,
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
    account = MagicMock(
        spec=Account, balance=account_balance, id=1, currency=account_currency
    )

    # assign the account to the returned value of the Account.objects.select_for_update().get() mock
    mock_select_for_update.return_value.get.return_value = account

    # create serializer object
    serializer = create_autospec(TransactionSerializer, instance=True)
    serializer.validated_data = {"amount": data["amount"], "currency": data["currency"]}

    # mock currency query
    mock_get_currency_rate = mocker.patch(
        "quotation_system.currencies.utils.CurrencyRate.objects.get"
    )

    mock_get_currency_rate.return_value.rate = currency_rate

    # act
    view.perform_create(serializer)

    # assert
    serializer.save.assert_called_once()
    account.save.assert_called_once()
    mock_atomic.assert_called_once()

    # check balance was updated
    assert account.balance == transaction_amount / currency_rate
    assert serializer.validated_data["previous_balance"] == account_balance
    assert (
        serializer.validated_data["new_balance"]
        == account_balance + transaction_amount / currency_rate
    )
