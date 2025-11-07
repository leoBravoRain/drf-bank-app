from django.test import SimpleTestCase
from rest_framework.test import APIRequestFactory
from unittest.mock import Mock, create_autospec
from quotation_system.accounts.views import AccountListView
from quotation_system.accounts.serializers import AccountSerializer
from unittest.mock import patch, MagicMock


class AccountListViewTestCase(SimpleTestCase):
    
    def setUp(self):
        # create a request object to pass to the view (instead of using the client who makes the http reuqest)
        self.factory = APIRequestFactory()
        self.user = Mock()
        self.user.id = 1
        self.view = AccountListView()
        
    def test_perform_create_sets_user_and_zero_balance(self):
        # arrange
        
        # creates a DRF Request object representing a POST to path /. It’s not sent over HTTP — it’s just an object.
        request = self.factory.post("/")
        
        # attaches the fake user to the request. 
        # The view’s perform_create uses self.request.user, so we must supply it.
        request.user = self.user
        
        # assigns the fake request to the view instance so the view method reads it normally.
        self.view.request = request

        # create a serializer object instead of using the real serializer
        # creates a mock that enforces the interface of AccountSerializer
        serializer = create_autospec(AccountSerializer, instance=True)

        # act
        
        # This calls the method under test
        self.view.perform_create(serializer)

        # assert
        # This assertion checks that the mocked serializer’s save method was called exactly once and with the exact keyword arguments user=self.user and balance=0
        serializer.save.assert_called_once()
        serializer.save.assert_called_once_with(user=self.user, balance=0)
    
    @patch('quotation_system.accounts.views.Account.objects.filter')
    def test_get_queryset_returns_accounts_for_the_user(self, mock_filter):
        # Arrange
        request = self.factory.get("/")
        request.user = self.user
        self.view.request = request

        # Act
        self.view.get_queryset()

        # Assert
        mock_filter.assert_called_once()
        mock_filter.assert_called_once_with(user=self.user)
    
        