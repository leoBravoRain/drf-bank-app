import pytest
from rest_framework.test import APIRequestFactory
from quotation_system.transactions.views import TransactionListView
from unittest.mock import MagicMock

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
    