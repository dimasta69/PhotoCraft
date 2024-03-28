from rest_framework import serializers


class ProfileSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    is_active = serializers.BooleanField(required=False)
    date_joined = serializers.DateTimeField(required=False)
