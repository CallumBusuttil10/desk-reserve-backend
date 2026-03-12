from rest_framework import serializers
from .models import Workspace, Booking, UserProfile

class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = ['id', 'name', 'resource_type', 'capacity', 'is_active', 'image_url']