from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestUserViews(APITestCase):

    correct_user = {"username": "testuser", "password": "testpassword"}
    incorrect_user = {"username": "incorrectusername", "password": "incorrectpassword"}

    # setup
    def setUp(self):
        # create test user
        self.user = User.objects.create_user(**self.correct_user)

    # test login with correct credentials
    def test_login_with_correct_credentials(self):
        """
        Test a user with correct credentials can login and receive tokens.
        """
        # arrange
        url = reverse("login")

        data = {
            "username": self.correct_user["username"],
            "password": self.correct_user["password"],
        }

        # act
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    # test login with incorrect credentials
    def test_login_with_incorrect_credentials(self):
        """
        Test a user with incorrect credentials cannot login and receives an error.
        """
        # arrange
        url = reverse("login")

        data = {
            "username": self.incorrect_user["username"],
            "password": self.incorrect_user["password"],
        }

        # act
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)
        self.assertEqual(
            response.data["detail"],
            "No active account found with the given credentials",
        )

    # test refresh token with valid refresh token
    def test_refresh_token_with_valid_refresh_token(self):
        """
        Test a user can refresh their access token with a valid refresh token.
        """
        # arrange
        url_refresh = reverse("refresh")

        # get refresh token
        response = self.client.post(reverse("login"), self.correct_user, format="json")
        refresh_token = response.data["refresh"]

        data_refresh = {"refresh": refresh_token}

        response = self.client.post(url_refresh, data_refresh, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    # test refresh token with invalid refresh token
    def test_refresh_token_with_invalid_refresh_token(self):
        """
        Test a user cannot refresh their access token with an invalid refresh token.
        """
        # arrange
        url_refresh = reverse("refresh")

        data_refresh = {"refresh": "invalid_refresh_token"}

        # act
        response = self.client.post(url_refresh, data_refresh, format="json")

        # assert
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "Token is invalid")

    # test login with missing credentials
    def test_login_with_missing_credentials(self):
        """
        Test login fails when username or password is missing.
        """
        url = reverse("login")

        # Test missing password
        response = self.client.post(url, {"username": "testuser"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test missing username
        response = self.client.post(url, {"password": "testpassword"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test empty data
        response = self.client.post(url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # test refresh token with missing refresh token
    def test_refresh_token_with_missing_token(self):
        """
        Test refresh token endpoint fails when refresh token is missing.
        """
        url_refresh = reverse("refresh")

        response = self.client.post(url_refresh, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # test token structure and validity
    def test_token_structure(self):
        """
        Test that returned tokens have the correct structure and can be decoded.
        """
        from rest_framework_simplejwt.tokens import RefreshToken

        url = reverse("login")
        response = self.client.post(url, self.correct_user, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify tokens are strings
        self.assertIsInstance(response.data["access"], str)
        self.assertIsInstance(response.data["refresh"], str)

        # Verify tokens are not empty
        self.assertGreater(len(response.data["access"]), 0)
        self.assertGreater(len(response.data["refresh"]), 0)

        # Verify refresh token can be used to create a new access token
        refresh = RefreshToken(response.data["refresh"])
        new_access_token = str(refresh.access_token)
        self.assertIsInstance(new_access_token, str)
        self.assertGreater(len(new_access_token), 0)
