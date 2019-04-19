from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User
from django.utils.timezone import localtime

from ..serializers.test import TestPostSerializer, TestGetSerializer, TestGetConciseSerializer, \
    TestSubmissionPostSerializer, \
    TestResultOverviewGetSerializer, UserTestResultGetSerializer
from ..models.test import Test
from ..models.test import TestSubmission as TestSubmissionModel


class TestList(GenericAPIView):
    """
    Test view class.

    get:
    Read list of all tests.

    post:
    Create test instance.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TestGetConciseSerializer
        if self.request.method == 'POST':
            return TestPostSerializer
        return None

    def get(self, request):
        """
        Reads lists of all test instances.
        """
        queryset_tests = Test.objects.all()
        serializer = TestGetConciseSerializer(queryset_tests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Creates test instance using passed JSON from request body.
        """
        serializer = TestPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['owner'] = request.user
            test = serializer.create(validated_data=serializer.validated_data)
            return Response({"id": test.id}, status=status.HTTP_201_CREATED)
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
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = TestSubmissionPostSerializer

    def post(self, request, test_id):
        """
        Creates test submission instance using passed JSON from request body.
        """
        test = get_object_or_404(Test, pk=test_id)
        # if test has not been submitted yet
        if not TestSubmissionModel.objects.filter(test__id=test.id, user__id=request.user.id):
            # check if test is opened for submission
            if test.date_open is None:
                return Response({"detail": "Test is not open for submission."}, status=status.HTTP_400_BAD_REQUEST)
            if test.date_open > localtime():
                return Response({"detail": "Test open date is in future."},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            # check if test is not closed for submission
            if test.date_close is not None:
                return Response({"detail": "Test is closed for submission."}, status=status.HTTP_410_GONE)
            else:
                request.data['test_id'] = test_id
                request.data['user_id'] = request.user.id
                serializer = TestSubmissionPostSerializer(data=request.data)
                if serializer.is_valid():
                    test_submission = serializer.create(validated_data=serializer.validated_data)
                    return Response({"id": test_submission.id}, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Test has been already submitted."}, status=status.HTTP_400_BAD_REQUEST)


class TestSubmissionOpen(GenericAPIView):
    """
    Open test submission view class.

    post:
    Open submission.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        pass

    def post(self, request, test_id):
        """
        Opens test submission.
        """
        test = get_object_or_404(Test, pk=test_id)
        if test.owner == request.user:
            if test.date_open is None:
                test.date_open = localtime()
                test.save()
                return Response({"detail": "Test is ready for submission now."}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Test is already opened."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "You are not owner of this test to open it."},
                            status=status.HTTP_400_BAD_REQUEST)


class TestSubmissionClose(GenericAPIView):
    """
    Close test submission view class.

    post:
    Close submission.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        pass

    def post(self, request, test_id):
        """
        Closes test submission.
        """
        test = get_object_or_404(Test, pk=test_id)
        if test.owner == request.user:
            if test.date_open is None:
                return Response({"detail": "Test is not even opened to be closed."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                if test.date_close is None:
                    test.date_close = localtime()
                    test.save()
                    return Response({"detail": "Test submission is closed now."}, status=status.HTTP_200_OK)
                else:
                    return Response({"detail": "Test is already closed."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "You are not owner of this test to close it."},
                            status=status.HTTP_400_BAD_REQUEST)


class TestResultOverview(GenericAPIView):
    """
    Test result view class.

    get:
    Get test result overview.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = TestResultOverviewGetSerializer

    def get(self, request, test_id):
        """
        Returns test result overview.
        """
        test = get_object_or_404(Test, pk=test_id)
        # check if test is opened
        if test.date_open is None:
            return Response({"detail": "Test is not opened."}, status=status.HTTP_400_BAD_REQUEST)
        # check if test is closed to get result
        if test.date_close is None:
            return Response({"detail": "Test is not closed. You can not get result until it is closed."},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = TestResultOverviewGetSerializer()
        return Response(serializer.to_representation(test), status=status.HTTP_200_OK)


class UserTestResult(GenericAPIView):
    """
    User test result view class.

    get:
    Get user test result.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = UserTestResultGetSerializer

    def get(self, request, test_id, user_id):
        """
        Returns test result overview of particular user.
        """
        test = get_object_or_404(Test, pk=test_id)
        user = get_object_or_404(User, pk=user_id)
        # check if test is opened
        if test.date_open is None:
            return Response({"detail": "Test is not opened."}, status=status.HTTP_400_BAD_REQUEST)
        # check if test is closed to get result
        if test.date_close is None:
            return Response({"detail": "Test is not closed. You can not get result until it is closed."},
                            status=status.HTTP_400_BAD_REQUEST)
        test_submission = TestSubmissionModel.objects.get(test__id=test.id, user__id=user_id)
        serializer = UserTestResultGetSerializer()
        return Response(serializer.to_representation(test, test_submission), status=status.HTTP_200_OK)


class UserTestSubmissionList(GenericAPIView):
    """
    User test submission view class.

    get:
    Read list of all tests submitted by user.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TestGetConciseSerializer
        return None

    def get(self, request, user_id):
        """
        Reads lists of all test instances submitted by user.
        """
        list_user_submitted_tests_ids = list(TestSubmissionModel.objects \
                                             .filter(user_id=user_id) \
                                             .distinct("test_id") \
                                             .values_list("test_id", flat=True))
        queryset_user_submitted_tests = Test.objects.filter(id__in=list_user_submitted_tests_ids)
        serializer = TestGetConciseSerializer(queryset_user_submitted_tests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
