from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from ..serializers.test import TestPostSerializer, TestGetSerializer, TestSubmissionPostSerializer
from ..models.test import Test
from ..models.test import TestSubmission as TestSubmissionModel

from django.utils.timezone import localtime


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


class TestDetail(GenericAPIView):
    """
    Test view class.

    get:
    Read test instance by id.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = TestGetSerializer

    def get(self, request, test_id: int):
        """
        Reads test instance by id.

        :param request: test read initiator.
        :param test_id: test instance id.
        :return: HTTP response with serialized test instance.
        """
        test = get_object_or_404(Test, pk=test_id)
        serializer = TestGetSerializer(test)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TestSubmission(GenericAPIView):
    """
    Test submission view class.

    post:
    Submit test.
    """
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    serializer_class = TestSubmissionPostSerializer

    def post(self, request, test_id):
        """
        Creates test submission instance using passed JSON from request body.

        :param request: test submission initiator.
        :param test_id: source test to submit.
        :return: HTTP response with id of created test submission instance.
        """
        test = get_object_or_404(Test, pk=test_id)
        # if test has not been submitted yet
        if not TestSubmissionModel.objects.filter(test__id=test.id, user__id=request.user.id):
            # check if test is opened for submission
            if test.date_open is None:
                return Response({"detail": "Test is not open for submission."}, status=status.HTTP_400_BAD_REQUEST)
            if test.date_open > localtime():
                return Response({"detail": "Test open date is in future."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            # check if test is not closed for submission
            if test.date_close is not None:
                return Response({"detail": "Test is closed for submission."}, status=status.HTTP_410_GONE)
            else:
                request.data['test_id'] = test_id
                request.data['user_id'] = request.user.id
                serializer = TestSubmissionPostSerializer(data=request.data)
                if serializer.is_valid():
                    test_submission = serializer.create(validated_data=serializer.validated_data)
                    return Response({"test_submission_id": test_submission.id}, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Test has been already submitted."}, status=status.HTTP_400_BAD_REQUEST)


class TestSubmissionOpen(GenericAPIView):
    """
    Open test submission view class.

    post:
    Open submission.
    """
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get_serializer_class(self):
        pass

    def post(self, request, test_id):
        """
        Opens test submission.

        :param request: test submission open initiator.
        :param test_id: test id to open.
        :return: HTTP response with operation result code.
        """
        test = get_object_or_404(Test, pk=test_id)
        if test.owner == request.user:
            if test.date_open is None:
                test.date_open = localtime()
                test.save()
                return Response({"details": "Test is ready for submission now."}, status=status.HTTP_200_OK)
            else:
                return Response({"details": "Test is already opened."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"details": "You are not owner of this test to open it."},
                            status=status.HTTP_400_BAD_REQUEST)


class TestSubmissionClose(GenericAPIView):
    """
    Close test submission view class.

    post:
    Close submission.
    """
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get_serializer_class(self):
        pass

    def post(self, request, test_id):
        """
        Closes test submission.

        :param request: test submission close initiator.
        :param test_id: test id to open.
        :return: HTTP response with operation result code.
        """
        test = get_object_or_404(Test, pk=test_id)
        if test.owner == request.user:
            if test.date_open is None:
                return Response({"details": "Test is not even opened to be closed."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                if test.date_close is None:
                    test.date_close = localtime()
                    test.save()
                    return Response({"details": "Test submission is closed now."}, status=status.HTTP_200_OK)
                else:
                    return Response({"details": "Test is already closed."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"details": "You are not owner of this test to close it."},
                            status=status.HTTP_400_BAD_REQUEST)
