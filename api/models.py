from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Employee', 'Employee'),
        ('Admin', 'Admin'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Employee')
    profile_image_url = models.URLField(blank=True, null=True) # Ready for Cloudinary later

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class Workspace(models.Model):
    RESOURCE_TYPES = [
        ('Desk', 'Desk'),
        ('Meeting Room', 'Meeting Room'),
        ('Pod', 'Soundproof Pod'),
    ]

    name = models.CharField(max_length=100)
    resource_type = models.CharField(max_length=50, choices=RESOURCE_TYPES)
    capacity = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.resource_type})"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} -> {self.workspace.name} on {self.booking_date}"