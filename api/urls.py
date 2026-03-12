from django.urls import path
from . import views

urlpatterns = [
    path('workspaces/', views.get_workspaces, name='get_workspaces'),
    path('bookings/create/', views.create_booking, name='create_booking'),
    path('bookings/user/<int:user_id>/', views.get_user_bookings, name='get_user_bookings'),
    path('bookings/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
]