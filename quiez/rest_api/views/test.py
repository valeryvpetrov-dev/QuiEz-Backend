from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from ..serializers.test import TestPostSerializer


class TestList(GenericAPIView):
    """
    Test view class.

    post:
    Create test instance.
    """
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    serializer_class = TestPostSerializer

    def post(self, request):
        """
        Creates test instance using passed JSON from request body.

        :param request: test creation initiator.
        :return: HTTP response with id of created test instance.
        """
        serializer = TestPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['owner'] = request.user
            test = serializer.create(validated_data=serializer.validated_data)
            return Response({"test_id": test.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
