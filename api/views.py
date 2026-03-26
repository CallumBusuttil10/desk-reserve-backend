import os
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Workspace, Booking
from .serializers import WorkspaceSerializer, BookingSerializer, RegisterSerializer
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

@api_view(['GET'])
def get_workspaces(request):
    """Fetch all active workspaces."""
    workspaces = Workspace.objects.filter(is_active=True)
    serializer = WorkspaceSerializer(workspaces, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """Register a new user and send a Welcome email."""
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()

        try:
            subject = "Welcome to DeskReserve!"
            plain_message = f"Hi {user.username},\n\nWelcome to DeskReserve! Your account is ready to go."
            html_message = f"""
            <div style="font-family: Arial, sans-serif; color: #333; max-width: 600px; margin: 0 auto; border: 1px solid #e0e0e0; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                <div style="background-color: #1976d2; padding: 20px; text-align: center; color: white;">
                    <h2 style="margin: 0; letter-spacing: 1px;">Welcome to DeskReserve!</h2>
                </div>
                <div style="padding: 30px; background-color: #ffffff; text-align: center;">
                    <p style="font-size: 18px;">Hello <strong>{user.username}</strong>,</p>
                    <p style="font-size: 16px; color: #555;">Your account has been successfully created. You can now log in and start booking workspaces instantly.</p>
                    <br>
                    <p style="font-size: 16px; margin-bottom: 0;">We're excited to have you,</p>
                    <p style="font-size: 16px; font-weight: bold; color: #1976d2; margin-top: 5px;">The DeskReserve Team</p>
                </div>
            </div>
            """
            send_mail(subject, plain_message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False, html_message=html_message)
        except Exception as e:
            print(f"SendGrid Error (Welcome Email): {e}")

        return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
            plain_message = f"Hello {request.user.username},\n\nSuccess! Your booking for {workspace_name} on {date} from {booking.start_time} to {booking.end_time} is confirmed.\n\nThe DeskReserve Team"

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
            send_mail(subject, plain_message, settings.DEFAULT_FROM_EMAIL, [user_email], fail_silently=False, html_message=html_message)
        except Exception as e:
            print(f"SendGrid Error: {e}")

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_bookings(request):
    """Fetch all bookings for the currently authenticated user based on their token."""
    bookings = Booking.objects.filter(user=request.user).order_by('booking_date', 'start_time')
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_booking(request, pk):
    """Delete an existing booking."""
    try:
        booking = Booking.objects.get(id=pk, user=request.user)
    except Booking.DoesNotExist:
        return Response({"error": "Booking not found or not yours."}, status=status.HTTP_404_NOT_FOUND)

    booking.delete()
    return Response({"message": "Booking deleted successfully"}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def request_password_reset(request):
    """Generates a token and sends a password reset link via email."""
    email = request.data.get('email')

    if not email:
        return Response({"error": "Please provide an email address."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        frontend_url = os.environ.get('FRONTEND_URL', 'http://localhost:5173').rstrip('/')
        reset_link = f"{frontend_url}/reset-password/{uid}/{token}/"

        subject = "Password Reset Request - DeskReserve"
        plain_message = f"Click here to reset your password: {reset_link}"
        html_message = f"""
        <div style="font-family: Arial, sans-serif; padding: 20px; text-align: center;">
            <h2 style="color: #1976d2;">Password Reset</h2>
            <p>You requested a password reset for your DeskReserve account.</p>
            <p>Click the button below to choose a new password. This link is only valid for a short time.</p>
            <a href="{reset_link}" style="display: inline-block; padding: 10px 20px; margin-top: 20px; background-color: #1976d2; color: white; text-decoration: none; border-radius: 5px;">Reset Password</a>
            <p style="margin-top: 30px; font-size: 12px; color: #777;">If you did not request this, please ignore this email.</p>
        </div>
        """

        send_mail(subject, plain_message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False, html_message=html_message)

    except User.DoesNotExist:
        pass

    return Response({"message": "If an account with that email exists, a reset link has been sent."}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def confirm_password_reset(request):
    """Verifies the token and updates the user's password."""
    uidb64 = request.data.get('uidb64')
    token = request.data.get('token')
    new_password = request.data.get('new_password')

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.set_password(new_password)
        user.save()
        return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "This reset link is invalid or has expired."}, status=status.HTTP_400_BAD_REQUEST)