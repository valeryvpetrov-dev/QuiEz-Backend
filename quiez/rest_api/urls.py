from django.urls import path, include

from rest_framework.permissions import AllowAny

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views.auth import Registration
from .views.test import TestList, TestDetail

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
    path('auth/register/', Registration.as_view()),

    # test
    path('test', TestList.as_view()),
    path('test/<int:test_id>', TestDetail.as_view()),
]
