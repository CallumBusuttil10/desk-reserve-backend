from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Workspace, Booking

class BookingEngineTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.workspace = Workspace.objects.create(
            name="Test Desk",
            resource_type="Desk",
            capacity=1,
            is_active=True
        )
        self.create_url = reverse('create_booking')

    def test_prevent_double_booking(self):
        valid_data = {
            "user": self.user.id,
            "workspace": self.workspace.id,
            "booking_date": "2026-03-20",
            "start_time": "09:00:00",
            "end_time": "17:00:00",
            "status": "Confirmed"
        }
        response1 = self.client.post(self.create_url, valid_data, format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        conflict_data = {
            "user": self.user.id,
            "workspace": self.workspace.id,
            "booking_date": "2026-03-20",
            "start_time": "10:00:00",
            "end_time": "12:00:00",
            "status": "Confirmed"
        }
        response2 = self.client.post(self.create_url, conflict_data, format='json')

        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)