from django.urls import path, include

from .views.auth import Registration
from .views.test import TestList


urlpatterns = [
    # browsable API autharization
    path('auth-rest/', include('rest_framework.urls', namespace='rest_framework')),
    # authorization stuff provided by rest_auth
    path('auth/', include('rest_auth.urls')),
    # registration
    path('auth/register/', Registration.as_view()),

    # test
    path('test', TestList.as_view()),
]
