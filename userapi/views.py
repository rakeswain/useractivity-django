from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from rest_framework.views import APIView


class ListUsers(APIView):
    """ List all users with their activity periods."""

    def get(self, request, format=None):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response({'ok': True, 'members': serializer.data})
