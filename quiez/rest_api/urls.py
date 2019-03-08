from django.urls import path, include

from rest_framework_swagger.views import get_swagger_view

from .views.auth import Registration


urlpatterns = [
    # docs
    path('', get_swagger_view(title='QuiEz API')),

    # browsable API autharization
    path('auth-rest/', include('rest_framework.urls', namespace='rest_framework')),
    # authorization stuff provided by rest_auth
    path('auth/', include('rest_auth.urls')),
    # registration
    path('auth/register/', Registration.as_view()),
]
