from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from django.contrib.auth.models import User

from quiez.rest_api.serializers.auth import UserSerializer


class Registration(GenericAPIView):
    """
    Registration view.
    """
    permission_classes = (AllowAny, )
    serializer_class = UserSerializer

    def post(self, request):
        """
        Registration function for new users.
        * Email will be used as username.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            str_username = serializer.validated_data["email"]
            serializer.validated_data["username"] = str_username
            try:
                user = User.objects.get(username=str_username)
                return Response({'detail': 'User with given email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                User.objects.create_user(**serializer.validated_data)
                return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
