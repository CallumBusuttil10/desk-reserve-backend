from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Workspace, Booking
from .serializers import WorkspaceSerializer, BookingSerializer
from django.core.mail import send_mail
from django.conf import settings

@api_view(['GET'])
def get_workspaces(request):
    """Fetch all active workspaces."""
    workspaces = Workspace.objects.filter(is_active=True)
    serializer = WorkspaceSerializer(workspaces, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_booking(request):
    """Create a new booking and send an HTML confirmation email."""
    serializer = BookingSerializer(data=request.data)

    if serializer.is_valid():
        booking = serializer.save()

        try:
            user_email = request.user.email
            workspace_name = booking.workspace.name
            date = booking.booking_date

            subject = f"Booking Confirmed: {workspace_name}"

            # 1. Keep the plain text fallback for older email clients/smartwatches
            plain_message = (
                f"Hello {request.user.username},\n\n"
                f"Success! Your booking for {workspace_name} on {date} from "
                f"{booking.start_time} to {booking.end_time} is confirmed.\n\n"
                f"The DeskReserve Team"
            )

            # 2. Add the slick HTML version
            html_message = f"""
            <div style="font-family: Arial, sans-serif; color: #333; max-width: 600px; margin: 0 auto; border: 1px solid #e0e0e0; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                <div style="background-color: #1976d2; padding: 20px; text-align: center; color: white;">
                    <h2 style="margin: 0; letter-spacing: 1px;">DESKRESERVE</h2>
                </div>
                <div style="padding: 30px; background-color: #ffffff;">
                    <p style="font-size: 16px;">Hello <strong>{request.user.username}</strong>,</p>
                    <p style="font-size: 16px; color: #555;">Your workspace has been successfully reserved. Here are the details of your booking:</p>

                    <div style="background-color: #f8fafc; padding: 20px; border-radius: 6px; margin: 25px 0; border-left: 4px solid #1976d2;">
                        <p style="margin: 5px 0; font-size: 15px;"><strong>Workspace:</strong> {workspace_name}</p>
                        <p style="margin: 5px 0; font-size: 15px;"><strong>Date:</strong> {date}</p>
                        <p style="margin: 5px 0; font-size: 15px;"><strong>Time:</strong> {booking.start_time} - {booking.end_time}</p>
                    </div>

                    <p style="font-size: 14px; color: #777;">If you need to adjust or cancel this reservation, you can do so directly from the <strong>My Bookings</strong> page on your dashboard.</p>
                    <br>
                    <p style="font-size: 16px; margin-bottom: 0;">See you soon,</p>
                    <p style="font-size: 16px; font-weight: bold; color: #1976d2; margin-top: 5px;">The DeskReserve Team</p>
                </div>
            </div>
            """

            # 3. Pass BOTH to send_mail
            send_mail(
                subject=subject,
                message=plain_message,          # Fallback
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user_email],
                fail_silently=False,
                html_message=html_message       # The fancy HTML version
            )
        except Exception as e:
            print(f"SendGrid Error: {e}")

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