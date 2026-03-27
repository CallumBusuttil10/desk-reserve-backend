from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.core import mail

class AuthenticationTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.password_reset_url = reverse('request_password_reset')

    def test_user_registration_success(self):
        """Ensure a user can register and receives a welcome email."""
        payload = {
            "username": "newuser",
            "email": "newuser@test.com",
            "password": "securepassword123"
        }
        response = self.client.post(self.register_url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="newuser").exists())

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Welcome to DeskReserve!')

    def test_user_registration_missing_email(self):
        """Ensure registration fails if the required email field is missing."""
        payload = {
            "username": "noemailuser",
            "password": "securepassword123"
        }
        response = self.client.post(self.register_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_password_reset_email_generation(self):
        """Ensure requesting a password reset generates an email with a token."""
        User.objects.create_user(username="testuser1", email="user1@test.com", password="password123")

        payload = {
            "email": "user1@test.com"
        }
        response = self.client.post(self.password_reset_url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Password Reset Request - DeskReserve')