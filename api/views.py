from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Workspace
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