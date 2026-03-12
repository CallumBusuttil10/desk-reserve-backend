from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Workspace, Booking

class BookingEngineTests(APITestCase):
    def setUp(self):
        # 1. Create a test user and a test desk for our virtual environment
        self.user = User.objects.create(username="testuser")
        self.workspace = Workspace.objects.create(
            name="Test Desk",
            resource_type="Desk",
            capacity=1,
            is_active=True
        )
        self.create_url = reverse('create_booking')

    def test_prevent_double_booking(self):
        # (Keep your existing double-booking test code here!)
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

    def test_invalid_time_booking(self):
        """Ensure the server rejects a booking if the end time is before the start time."""
        invalid_data = {
            "user": self.user.id,
            "workspace": self.workspace.id,
            "booking_date": "2026-03-21",
            "start_time": "15:00:00",
            "end_time": "14:00:00",
            "status": "Confirmed"
        }
        response = self.client.post(self.create_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_active_workspaces(self):
        """Ensure the GET endpoint successfully fetches active workspaces."""
        url = reverse('get_workspaces')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Test Desk")

    def test_cancel_booking(self):
        """Ensure a user can cancel their booking and it updates the database."""
        booking = Booking.objects.create(
            user=self.user,
            workspace=self.workspace,
            booking_date="2026-03-25",
            start_time="10:00:00",
            end_time="12:00:00",
            status="Confirmed"
        )

        url = reverse('cancel_booking', args=[booking.id])
        response = self.client.patch(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'Cancelled')

        booking.refresh_from_db()
        self.assertEqual(booking.status, 'Cancelled')