from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Workspace, Booking

class DeskReserveAPITests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="testuser1", password="password123")
        self.user2 = User.objects.create_user(username="testuser2", password="password123")

        self.workspace = Workspace.objects.create(
            name="Test Desk",
            resource_type="Desk",
            floor=1,
            capacity=1,
            is_active=True
        )

        self.create_url = reverse('create_booking')
        self.workspaces_url = reverse('workspaces')
        self.user_bookings_url = reverse('get_user_bookings')


    def test_prevent_double_booking(self):
        """Ensure the server prevents overlapping bookings on the same resource."""
        self.client.force_authenticate(user=self.user1) # Auth required now

        valid_data = {
            "user": self.user1.id,
            "workspace": self.workspace.id,
            "booking_date": "2026-03-20",
            "start_time": "09:00:00",
            "end_time": "17:00:00",
            "status": "Confirmed"
        }
        response1 = self.client.post(self.create_url, valid_data, format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        conflict_data = {
            "user": self.user1.id,
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
        self.client.force_authenticate(user=self.user1)

        invalid_data = {
            "user": self.user1.id,
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
        # Note: Anyone can fetch workspaces (no auth required)
        response = self.client.get(self.workspaces_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Test Desk")

    def test_create_booking_unauthenticated(self):
        """A guest cannot create a booking."""
        payload = {
            "user": self.user1.id,
            "workspace": self.workspace.id,
            "booking_date": "2026-03-22",
            "start_time": "10:00:00",
            "end_time": "12:00:00"
        }
        response = self.client.post(self.create_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_user_bookings_isolation(self):
        """Users should only see their own bookings."""
        Booking.objects.create(
            user=self.user1,
            workspace=self.workspace,
            booking_date="2026-03-25",
            start_time="10:00:00",
            end_time="12:00:00",
            status="Confirmed"
        )

        self.client.force_authenticate(user=self.user2)
        response = self.client.get(self.user_bookings_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.user_bookings_url)
        self.assertEqual(len(response.data), 1)

    def test_delete_own_booking(self):
        """Ensure a user can cancel/delete their own booking and it updates the database."""
        booking = Booking.objects.create(
            user=self.user1,
            workspace=self.workspace,
            booking_date="2026-03-25",
            start_time="10:00:00",
            end_time="12:00:00",
            status="Confirmed"
        )

        self.client.force_authenticate(user=self.user1)
        url = reverse('delete_booking', args=[booking.id])

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Booking.objects.count(), 0)

    def test_delete_other_users_booking(self):
        """Users cannot delete someone else's booking."""
        booking = Booking.objects.create(
            user=self.user1,
            workspace=self.workspace,
            booking_date="2026-03-26",
            start_time="09:00:00",
            end_time="11:00:00",
            status="Confirmed"
        )

        self.client.force_authenticate(user=self.user2)
        url = reverse('delete_booking', args=[booking.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Booking.objects.count(), 1)