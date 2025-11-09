import pytest
from rest_framework.test import APIRequestFactory
from quotation_system.transactions.views import TransactionListView, TransactionDetailView
from unittest.mock import MagicMock
from quotation_system.transactions.models import Transaction
from quotation_system.transactions.serializers import TransactionSerializer
from unittest.mock import create_autospec
from quotation_system.accounts.models import Account
from rest_framework import serializers

# fixtures
@pytest.fixture
def api_factory():
    """Provides a DRF APIRequestFactory instance."""
    return APIRequestFactory()

@pytest.fixture
def user():
    """Provides a fake user object."""
    user = MagicMock()
    user.id = 1
    return user

@pytest.fixture
def view():
    """Provides a AccountListView instance."""
    return TransactionListView()

@pytest.fixture
def detail_view():
    """Provides a TransactionDetailView instance."""
    return TransactionDetailView()

@pytest.mark.unit
def test_get_queryset_returns_transactions_filtered_by_user(api_factory, user, view, mocker):
    
    # arrange
    
    # mock filter() method
    mock_filter = mocker.patch('quotation_system.transactions.views.Transaction.objects.filter')
    
    # create request object
    request = api_factory.get("/")
    request.user = user
    view.request = request
    
    # act
    view.get_queryset()
    
    # assert
    mock_filter.assert_called_once()
    mock_filter.assert_called_once_with(user=user)
    
@pytest.mark.unit
def test_perform_create_deposit_sets_user_and_update_account_balance(api_factory, user, view, mocker):
    
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
    request =api_factory.post(
        "/",
        data,
        format="json",
    )
    request.user = user
    view.request = view.initialize_request(request)
    
    # mock get account
    mock_get_account = mocker.patch('quotation_system.transactions.views.Account.objects.get')
    
    # define account
    account = MagicMock(spec=Account)
    account.balance = account_balance
    account.id = 1
    
    # assign the account ot the returned vallue of the Account.objects.get() mock
    mock_get_account.return_value = account
    
    # create serializer object
    serializer = create_autospec(TransactionSerializer, instance=True)
    serializer.validated_data = {
        "amount": data['amount'],
    }
    
    # act
    view.perform_create(serializer)
    
    # assert
    serializer.save.assert_called_once()
    account.save.assert_called_once()
    
    # check balance was updated
    assert account.balance == data['amount']
    assert serializer.validated_data['previous_balance'] == account_balance
    assert serializer.validated_data['new_balance'] == account_balance + transaction_amount
    

@pytest.mark.unit
def test_perform_create_withdrawal_sets_user_and_update_account_balance(api_factory, user, view, mocker):
    
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
    request =api_factory.post(
        "/",
        data,
        format="json",
    )
    request.user = user
    view.request = view.initialize_request(request)
    
    # mock get account
    mock_get_account = mocker.patch('quotation_system.transactions.views.Account.objects.get')
    
    # define account
    account = MagicMock(spec=Account)
    account.balance = account_balance
    account.id = 1
    
    # assign the account ot the returned vallue of the Account.objects.get() mock
    mock_get_account.return_value = account
    
    # create serializer object
    serializer = create_autospec(TransactionSerializer, instance=True)
    serializer.validated_data = {
        "amount": data['amount'],
    }
    
    # act
    view.perform_create(serializer)
    
    # assert
    assert serializer.save.call_count == 1
    assert account.save.call_count == 1
    
    # check balance was updated
    assert account.balance == data['amount']
    assert serializer.validated_data['previous_balance'] == account_balance
    assert serializer.validated_data['new_balance'] == account_balance - transaction_amount
    

@pytest.mark.unit
def test_perform_create_with_invalid_transaction_type(api_factory, user, view, mocker):
    
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

    mock_get_account = mocker.patch(
        "quotation_system.transactions.views.Account.objects.get",
        return_value=MagicMock(spec=Account),
    )

    serializer = create_autospec(TransactionSerializer, instance=True)
    serializer.validated_data = {"amount": data["amount"]}

    with pytest.raises(serializers.ValidationError):
        view.perform_create(serializer)

    mock_get_account.assert_called_once_with(user=user, pk=data["account"])
    serializer.save.assert_not_called()
    
@pytest.mark.unit
def test_perform_create_withdrawal_with_not_enough_balance(api_factory, user, view, mocker):
    
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
    mock_get_account = mocker.patch('quotation_system.transactions.views.Account.objects.get')
    
    # define account
    account = MagicMock(spec=Account)
    account.balance = account_balance
    account.id = 1
    
    # assign the account ot the returned vallue of the Account.objects.get() mock
    mock_get_account.return_value = account
    
     # create serializer object
    serializer = create_autospec(TransactionSerializer, instance=True)
    serializer.validated_data = {
        "amount": data['amount'],
    }
    
    # act
    with pytest.raises(serializers.ValidationError) as e:
        view.perform_create(serializer)
    
    # assert
    assert e.value.detail[0] == "Insufficient balance"
    assert serializer.save.call_count == 0
    assert account.save.call_count == 0
    

@pytest.mark.unit
def test_get_object_returns_transaction(api_factory, user, detail_view, mocker):
    
    """
    Test to get a transaction by its id
    """
   # Arrange
    mock_transaction = MagicMock(spec=Transaction, instance=True)
    mock_get = mocker.patch(
        "quotation_system.transactions.views.Transaction.objects.get",
        return_value=mock_transaction,
    )

    request = api_factory.get("/")
    detail_view.request = detail_view.initialize_request(request)
    detail_view.request.user = user
    detail_view.kwargs = {"pk": 1}

    # Act
    result = detail_view.get_object()

    # Assert
    mock_get.assert_called_once_with(user=user, pk=1)
    assert result == mock_transaction