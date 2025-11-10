import pytest
from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from quotation_system.accounts.models import Account


@pytest.mark.integration
class TestAccountModel(APITestCase):
    """
    Test the Account model.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.account = Account.objects.create(
            user=self.user, currency="USD", balance=100
        )

    def test_account_number_initialization(self):
        """
        Test that the account number is initialized correctly.
        """
        self.assertEqual(self.account.account_number, 1)

    def test_account_number_increment_on_creation(self):
        """
        Test that the account number is incremented correctly.
        """
        account = Account.objects.create(user=self.user, currency="USD", balance=100)
        self.assertEqual(account.account_number, self.account.account_number + 1)

    def test_keep_account_number_on_update(self):
        """
        Test that the account number is not incremented on update.
        """
        self.account.balance = 200
        self.account.save()
        self.assertEqual(self.account.account_number, 1)
