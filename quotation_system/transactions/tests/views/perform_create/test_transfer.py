  
import pytest
from ....models import Transaction
from ....serializers import TransactionSerializer
from unittest.mock import MagicMock, call
from .....accounts.models import Account
from unittest.mock import create_autospec   
from rest_framework import serializers
from ..configtest import api_factory, user, view, mock_atomic

@pytest.mark.unit
def test_perform_create_transfer_sets_user_and_update_account_balance(api_factory, user, view, mocker, mock_atomic):
    
    # arrange
    transaction_amount = 50
    initial_sender_balance = 100
    initial_receiver_balance = 0
    
    data = {
        "transaction_type": Transaction.TRANSACTION_TYPES[2][0],
        "account": 1,
        "amount": transaction_amount,
        "currency": "USD",
        "related_account": 2
    }
    # create request obejct
    request =api_factory.post(
        "/",
        data,
        format="json",
    )
    view.request = view.initialize_request(request)
    view.request.user = user
    
     # define mock account
    sender_account = MagicMock(spec=Account, balance = initial_sender_balance, id = 1, currency='USD')
    receiver_account = MagicMock(spec=Account, balance = initial_receiver_balance, id = 2, currency='USD')
    
    # mock get account
    mock_select_for_update = mocker.patch(
        "quotation_system.transactions.views.Account.objects.select_for_update",
    )
    mock_get = mock_select_for_update.return_value.get
    mock_get.side_effect = [sender_account, receiver_account]

    # create serializer object
    serializer = create_autospec(TransactionSerializer, instance=True)
    serializer.validated_data = {
        "amount": data['amount'],
    }
    
    # act
    view.perform_create(serializer)
    
    # Assert - ensure Account.objects.get called twice with correct params
    expected_calls = [
        call(user=user, pk=sender_account.id),
        call(user=user, pk=receiver_account.id),
    ]
    mock_get.assert_has_calls(expected_calls)
    
    # assert serializer was called one time
    assert serializer.save.call_count == 1

    # assert account.save() method was called once for each account
    assert sender_account.save.call_count == 1
    assert receiver_account.save.call_count == 1
    mock_atomic.assert_called_once()
    
    new_sender_balance = initial_sender_balance - data['amount']
    
    # assert balances updating
    assert sender_account.balance == new_sender_balance
    assert receiver_account.balance == initial_receiver_balance + data['amount']
    
    # asserting transactinos sreialiaer balances
    assert serializer.validated_data['amount'] == data['amount']
    assert serializer.validated_data['previous_balance'] == initial_sender_balance
    assert serializer.validated_data['new_balance'] == new_sender_balance
    
   
@pytest.mark.unit
def test_perform_create_transfer_without_enough_balance(api_factory, user, view, mocker, mock_atomic):
    
    # arrange
    transaction_amount = 50
    initial_sender_balance = 0
    initial_receiver_balance = 0
    
    data = {
        "transaction_type": Transaction.TRANSACTION_TYPES[2][0],
        "account": 1,
        "amount": transaction_amount,
        "currency": "USD",
        "related_account": 2
    }
    # create request obejct
    request =api_factory.post(
        "/",
        data,
        format="json",
    )
    view.request = view.initialize_request(request)
    view.request.user = user
    
     # define mock account
    sender_account = MagicMock(spec=Account, balance = initial_sender_balance, id = 1)
    receiver_account = MagicMock(spec=Account, balance = initial_receiver_balance, id = 2)
    
    # mock get account
    # this shoudl be called only once
    mock_select_for_update = mocker.patch(
        "quotation_system.transactions.views.Account.objects.select_for_update",
    )
    mock_select_for_update.return_value.get.return_value = sender_account

    # create serializer object
    serializer = create_autospec(TransactionSerializer, instance=True)
    serializer.validated_data = {
        "amount": data['amount'],
    }
    
    # act
    with pytest.raises(serializers.ValidationError) as e:
        view.perform_create(serializer)
    
    # assert error message
    assert e.value.detail[0] == "Insufficient balance"
    
    # assert save calls
    assert serializer.save.call_count == 0
    assert sender_account.save.call_count == 0
    assert receiver_account.save.call_count == 0
    mock_atomic.assert_called_once()
    
@pytest.mark.unit
def test_perform_create_transfer_without_related_account(api_factory, user, view, mocker, mock_atomic):
    
    # arrange
    transaction_amount = 50
    initial_sender_balance = 0
    initial_receiver_balance = 0
    
    data = {
        "transaction_type": Transaction.TRANSACTION_TYPES[2][0],
        "account": 1,
        "amount": transaction_amount,
        "currency": "USD",
    }
    # create request obejct
    request =api_factory.post(
        "/",
        data,
        format="json",
    )
    view.request = view.initialize_request(request)
    view.request.user = user
    
     # define mock account
    sender_account = MagicMock(spec=Account, balance = initial_sender_balance, id = 1)
    receiver_account = MagicMock(spec=Account, balance = initial_receiver_balance, id = 2)
    
    # mock get account
    # this shoudl be called only once
    mock_select_for_update = mocker.patch(
        "quotation_system.transactions.views.Account.objects.select_for_update",
    )
    mock_select_for_update.return_value.get.return_value = sender_account

    # create serializer object
    serializer = create_autospec(TransactionSerializer, instance=True)
    serializer.validated_data = {
        "amount": data['amount'],
    }
    
    # act
    with pytest.raises(serializers.ValidationError) as e:
        view.perform_create(serializer)
    
    # assert error message
    assert e.value.detail[0] == "Related account must be defined"
    
    # assert save calls
    assert serializer.save.call_count == 0
    assert sender_account.save.call_count == 0
    assert receiver_account.save.call_count == 0
    mock_atomic.assert_called_once()
    