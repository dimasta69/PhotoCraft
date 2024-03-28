from rest_framework import serializers


class CreateLikedSerializer(serializers.Serializer):
    photo_id = serializers.IntegerField()
