from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.user.username


class Workspace(models.Model):
    RESOURCE_TYPES = [
        ('Desk', 'Desk'),
        ('Focus Pod', 'Focus Pod'),
        ('Boardroom', 'Boardroom'),
    ]

    name = models.CharField(max_length=100)
    resource_type = models.CharField(max_length=50, choices=RESOURCE_TYPES)
    floor = models.IntegerField(default=1) # NEW FIELD
    capacity = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='workspaces/', blank=True, null=True)

    def __str__(self):
        return f"Floor {self.floor} - {self.name}"


class Booking(models.Model):
    STATUS_CHOICES = [
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    booking_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Confirmed')

    def __str__(self):
        return f"{self.user.username} - {self.workspace.name} on {self.booking_date}"