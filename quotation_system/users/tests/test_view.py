from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status

class TestUserViews(APITestCase):
    
    correct_user = {
        'username': 'testuser',
        'password': 'testpassword'
    }
    incorrect_user = {
        'username': 'incorrectusername',
        'password': 'incorrectpassword'
    }
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
        url = reverse('login')
        
        data = {
            'username': self.correct_user['username'],
            'password': self.correct_user['password']
        }
        
        # act
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        
    # test login with incorrect credentials
    def test_login_with_incorrect_credentials(self):
        """
        Test a user with incorrect credentials cannot login and receives an error.
        """
        # arrange
        url = reverse('login')
        
        data = {
            'username': self.incorrect_user['username'],
            'password': self.incorrect_user['password']
        }
        
        # act
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'No active account found with the given credentials')
        
    # test refresh token with valid refresh token
    def test_refresh_token_with_valid_refresh_token(self):
        """
        Test a user can refresh their access token with a valid refresh token.
        """
        # arrange
        url_refresh = reverse('refresh')
        
        # get refresh token
        response = self.client.post(reverse('login'), self.correct_user, format='json')
        refresh_token = response.data['refresh']
        
        data_refresh = {
            'refresh': refresh_token
        }
        
        response = self.client.post(url_refresh, data_refresh, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        
    # test refresh token with invalid refresh token
    def test_refresh_token_with_invalid_refresh_token(self):
        """
        Test a user cannot refresh their access token with an invalid refresh token.
        """
        # arrange
        url_refresh = reverse('refresh')
        
        data_refresh = {
            'refresh': 'invalid_refresh_token'
        }
        
        # act
        response = self.client.post(url_refresh, data_refresh, format='json')
        
        # assert
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'Token is invalid')
        
        