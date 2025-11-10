import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


@pytest.mark.integration
class TestAccountViewsIntegration(APITestCase):
    """
    Test the Account views integration.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_create_account_with_correct_data(self):
        """
        Test that a new account can be created with correct data.
        """
        # assert
        url = reverse("account-list")

        self.client.force_authenticate(user=self.user)

        data = {
            "currency": "USD",
        }

        # act
        response = self.client.post(url, data, format="json")

        # get the account
        account = response.data

        # assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(account["account_number"], 1)
        self.assertEqual(account["currency"], "USD")
        self.assertEqual(account["balance"], "0.00")
        self.assertEqual(account["user"], self.user.username)

    def test_create_account_with_incorrect_data(self):
        """
        Test that a new account cannot be created with incorrect data.
        """
        # assert
        url = reverse("account-list")

        self.client.force_authenticate(user=self.user)

        data = {}

        # act
        response = self.client.post(url, data, format="json")

        # assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_account_with_missing_authentication(self):
        """
        Test that a new account cannot be created with missing authentication.
        """
        # assert
        url = reverse("account-list")

        data = {
            "currency": "USD",
        }

        # act
        response = self.client.post(url, data, format="json")

        # assert
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_account_with_balance(self):
        """
        Test that a new account can be created with a balance.
        """
        # assert
        url = reverse("account-list")

        self.client.force_authenticate(user=self.user)

        data = {
            "currency": "USD",
            "balance": 100,
        }

        # act
        response = self.client.post(url, data, format="json")

        # assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["balance"], "0.00")

    def test_list_accounts(self):
        """
        Test that a user can list their accounts.
        """
        # assert
        url = reverse("account-list")

        self.client.force_authenticate(user=self.user)

        # create account
        self.client.post(url, {"currency": "USD"}, format="json")

        # list accounts
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["currency"], "USD")
        self.assertEqual(response.data[0]["balance"], "0.00")
        self.assertEqual(response.data[0]["user"], self.user.username)

    def test_list_accounts_with_missing_authentication(self):
        """
        Test that a user cannot list their accounts with missing authentication.
        """
        # assert
        url = reverse("account-list")

        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_accounts_only_returns_accounts_for_the_user(self):
        """
        Test that a user can only list their own accounts.
        """
        # assert
        url = reverse("account-list")

        # authenticate with defaul user
        self.client.force_authenticate(user=self.user)

        # create account
        self.client.post(url, {"currency": "USD"}, format="json")

        # authenticate with new user

        # create new user
        user2 = User.objects.create_user(username="testuser2", password="testpassword2")

        self.client.force_authenticate(user=user2)

        # create account
        self.client.post(url, {"currency": "USD"}, format="json")

        # list accounts
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["currency"], "USD")
        self.assertEqual(response.data[0]["balance"], "0.00")
        self.assertEqual(response.data[0]["user"], user2.username)
