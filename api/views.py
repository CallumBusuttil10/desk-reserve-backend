from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Workspace, Booking
from .serializers import WorkspaceSerializer, BookingSerializer

@api_view(['GET'])
def get_workspaces(request):
    """Fetch all active workspaces."""
    workspaces = Workspace.objects.filter(is_active=True)
    serializer = WorkspaceSerializer(workspaces, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_booking(request):
    """Create a new booking."""
    serializer = BookingSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_bookings(request):
    """Fetch all bookings for the currently authenticated user based on their token."""
    # request.user is automatically populated by the JWT token
    bookings = Booking.objects.filter(user=request.user).order_by('booking_date', 'start_time')
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_booking(request, pk):
    """Delete an existing booking."""
    try:
        # We also ensure the user can only delete THEIR OWN bookings
        booking = Booking.objects.get(id=pk, user=request.user)
    except Booking.DoesNotExist:
        return Response({"error": "Booking not found or not yours."}, status=status.HTTP_404_NOT_FOUND)

    booking.delete()
    return Response({"message": "Booking deleted successfully"}, status=status.HTTP_200_OK)