from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('password-reset/', views.request_password_reset, name='request_password_reset'),
    path('password-reset/confirm/', views.confirm_password_reset, name='confirm_password_reset'),

    path('workspaces/', views.get_workspaces, name='workspaces'),

    path('bookings/create/', views.create_booking, name='create_booking'),
    path('bookings/', views.get_user_bookings, name='get_user_bookings'),
    path('bookings/<int:pk>/delete/', views.delete_booking, name='delete_booking'),
]