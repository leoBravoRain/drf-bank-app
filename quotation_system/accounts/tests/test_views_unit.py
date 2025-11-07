import pytest
from rest_framework.test import APIRequestFactory
from unittest.mock import Mock, create_autospec
from quotation_system.accounts.views import AccountListView
from quotation_system.accounts.serializers import AccountSerializer
from unittest.mock import patch, MagicMock
    
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
    return AccountListView()

def test_perform_create_sets_user_and_zero_balance(api_factory, user, view):
    """Test that the perform_create method sets the user and zero balance."""
    #  arrange
    request = api_factory.post("/")
    request.user = user
    view.request = request
    
    # create a serializer object instead of using the real serializer
    # creates a mock that enforces the interface of AccountSerializer
    serializer = create_autospec(AccountSerializer, instance=True)
        
    # act
    view.perform_create(serializer)
    
    # assertj
    serializer.save.assert_called_once()
    serializer.save.assert_called_once_with(user=user, balance=0)
    
def test_get_queryset_returns_accounts_for_the_user(api_factory, user, view, mocker):
    # Arrange
    mock_filter = mocker.patch('quotation_system.accounts.views.Account.objects.filter')
    
    request = api_factory.get("/")
    request.user = user
    view.request = request
    
    # Act
    view.get_queryset()
    
    # Assert
    mock_filter.assert_called_once()
    mock_filter.assert_called_once_with(user=user)
        