from django.urls import path
from . import views

urlpatterns = [
    # General workspace list
    path('workspaces/', views.get_workspaces, name='workspaces'),

    # Booking routes
    path('bookings/create/', views.create_booking, name='create_booking'),
    path('bookings/', views.get_user_bookings, name='get_user_bookings'),
    path('bookings/<int:pk>/delete/', views.delete_booking, name='delete_booking'),
]