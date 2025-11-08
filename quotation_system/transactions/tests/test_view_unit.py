import pytest
from rest_framework.test import APIRequestFactory
from quotation_system.transactions.views import TransactionListView
from unittest.mock import MagicMock
from quotation_system.transactions.models import Transaction
from quotation_system.transactions.serializers import TransactionSerializer
from unittest.mock import create_autospec
from quotation_system.accounts.models import Account
from rest_framework.request import Request

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
    
    # create request obejct
    request = Request(api_factory.post(
        "/", 
        {
        # set as deposit
        'transaction_type': Transaction.TRANSACTION_TYPES[0][0],
        'account': 1,
        'amount': 100,
        'currency': 'USD',
        }
    ))
    request.user = user
    view.request = request
    
    # mock get account
    mock_get_account = mocker.patch('quotation_system.transactions.views.Account.objects.get')
    
    # define account
    account = MagicMock(spec=Account)
    account.id = 1
    account.account_number = 1
    account.currency = 'USD'
    account.balance = 0
    account.user = user
    
    mock_get_account.return_value = account
    
    # create serializer object
    serializer = create_autospec(TransactionSerializer, instance=True)
    
    # act
    view.perform_create(serializer)
    
    # assert
    # TODO: complemte more assertions
    serializer.save.assert_called_once()
    
    
    
    