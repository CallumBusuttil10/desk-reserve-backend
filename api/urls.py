from django.urls import path
from . import views

urlpatterns = [
    path('workspaces/', views.get_workspaces, name='get_workspaces'),
    path('bookings/create/', views.create_booking, name='create_booking'),
]