from rest_framework import status
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from accounts.manager import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from accounts.models import User

# Create your views here.
@api_view(['GET'])
@permission_classes([AllowAny])
def test(request, format=None):
	return Response({"message": "Transaction API working."}, status=status.HTTP_200_OK)
