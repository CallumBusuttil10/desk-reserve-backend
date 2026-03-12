from django.contrib import admin
from .models import UserProfile, Workspace, Booking

admin.site.register(UserProfile)
admin.site.register(Workspace)
admin.site.register(Booking)