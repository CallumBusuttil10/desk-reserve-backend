from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Workspace
from .serializers import WorkspaceSerializer


@api_view(['GET'])
def get_workspaces(request):
    workspaces = Workspace.objects.filter(is_active=True)
    serializer = WorkspaceSerializer(workspaces, many=True)

    return Response(serializer.data)