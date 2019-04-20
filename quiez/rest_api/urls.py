from django.urls import path, include

from rest_framework.permissions import AllowAny

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views.auth import UserRegistrationView
from .views.test import TestListView, TestDetailView, TestSubmissionView, \
    TestSubmissionOpenView, TestSubmissionCloseView, \
    TestResultOverviewView, UserTestResultView, \
    UserTestSubmissionListView

schema_view = get_schema_view(
   openapi.Info(
      title="QuiEz API",
      default_version='v1',
      description="QuiEz application REST API.",
      contact=openapi.Contact(email="valera071998@gmail.com"),
   ),
   public=True,
   permission_classes=(AllowAny,),
)

urlpatterns = [
    # docs
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # browsable API autharization
    path('auth-rest/', include('rest_framework.urls', namespace='rest_framework')),
    # authorization stuff provided by rest_auth
    path('auth/', include('rest_auth.urls')),
    # registration
    path('auth/register/', UserRegistrationView.as_view()),

    # test
    path('test', TestListView.as_view()),
    path('test/<int:test_id>', TestDetailView.as_view()),
    path('test/<int:test_id>/open', TestSubmissionOpenView.as_view()),
    path('test/<int:test_id>/close', TestSubmissionCloseView.as_view()),
    path('test/<int:test_id>/submit', TestSubmissionView.as_view()),
    path('test/<int:test_id>/result', TestResultOverviewView.as_view()),
    path('test/<int:test_id>/result/<int:user_id>', UserTestResultView.as_view()),
    path('test/submission/<int:user_id>', UserTestSubmissionListView.as_view()),
]
