from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Workspace, Booking
from .serializers import WorkspaceSerializer, BookingSerializer



@api_view(['GET'])
def get_workspaces(request):
    workspaces = Workspace.objects.filter(is_active=True)
    serializer = WorkspaceSerializer(workspaces, many=True)

    return Response(serializer.data)

@api_view(['POST'])
def create_booking(request):
    serializer = BookingSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_user_bookings(request, user_id):
    """Fetch all bookings for a specific user."""
    bookings = Booking.objects.filter(user_id=user_id).order_by('booking_date', 'start_time')
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data)

@api_view(['PATCH'])
def cancel_booking(request, booking_id):
    """Cancel an existing booking."""
    try:
        booking = Booking.objects.get(id=booking_id)
    except Booking.DoesNotExist:
        return Response({"error": "Booking not found."}, status=status.HTTP_404_NOT_FOUND)

    booking.status = 'Cancelled'
    booking.save()

    serializer = BookingSerializer(booking)
    return Response(serializer.data, status=status.HTTP_200_OK)