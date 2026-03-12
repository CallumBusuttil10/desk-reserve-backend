from django.urls import path
from . import views

urlpatterns = [
    path('workspaces/', views.get_workspaces, name='get_workspaces'),
]