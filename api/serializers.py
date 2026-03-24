from rest_framework import serializers
from .models import Workspace, Booking, UserProfile

class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        # ADD 'floor' TO THIS LIST
        fields = ['id', 'name', 'resource_type', 'floor', 'capacity', 'is_active', 'image']

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'user', 'workspace', 'booking_date', 'start_time', 'end_time', 'status']

    def validate(self, data):
        """
        Custom enterprise validation to prevent double bookings.
        """
        workspace = data.get('workspace')
        booking_date = data.get('booking_date')
        start_time = data.get('start_time')
        end_time = data.get('end_time')

        # Basic time logic check
        if start_time >= end_time:
            raise serializers.ValidationError("End time must be after start time.")

        # Logic to prevent two people from booking the same desk at the same time
        overlapping_bookings = Booking.objects.filter(
            workspace=workspace,
            booking_date=booking_date,
            status__in=['Pending', 'Confirmed'],
            start_time__lt=end_time,
            end_time__gt=start_time
        )

        if overlapping_bookings.exists():
            raise serializers.ValidationError("This workspace is already booked for this time slot.")

        return data