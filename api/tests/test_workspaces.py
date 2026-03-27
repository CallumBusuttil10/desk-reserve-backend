from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Workspace

class WorkspaceTests(APITestCase):
    def setUp(self):
        self.workspace = Workspace.objects.create(
            name="Test Desk",
            resource_type="Desk",
            floor=1,
            capacity=1,
            is_active=True
        )
        self.workspaces_url = reverse('workspaces')

    def test_get_active_workspaces(self):
        """Ensure the GET endpoint successfully fetches active workspaces."""
        response = self.client.get(self.workspaces_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Test Desk")