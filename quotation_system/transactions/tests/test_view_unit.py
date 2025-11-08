import pytest
from rest_framework.test import APIRequestFactory
from quotation_system.transactions.views import TransactionListView
from unittest.mock import MagicMock
from quotation_system.transactions.models import Transaction
from quotation_system.transactions.serializers import TransactionSerializer
from unittest.mock import create_autospec
from quotation_system.accounts.models import Account

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
def test_perform_create_sets_user_and_update_account_balance(api_factory, user, view, mocker):
    
    # arrange
    
    data = {
        "transaction_type": Transaction.TRANSACTION_TYPES[0][0],
        "account": 1,
        "amount": 100,
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
    account.balance = 0
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
    assert serializer.validated_data['previous_balance'] == 0
    assert serializer.validated_data['new_balance'] == data['amount']

    
    
    
    
    