from rest_framework import serializers

from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Django default User model serializer for registration.

    * Email and password (authentication credentials),
    first and last names (Profile info) are required for registration.
    """

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
            'id':       {'read_only': True}
        }
