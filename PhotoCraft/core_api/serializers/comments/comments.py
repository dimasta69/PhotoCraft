from rest_framework import serializers

from models_app.models.photo.model import Photo
from models_app.models.users.model import User


class CommentsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    photo_id = serializers.PrimaryKeyRelatedField(queryset=Photo.objects.all())
    reply_id = serializers.IntegerField()
    text = serializers.CharField()
    publicated_at = serializers.DateTimeField()
    updated_at = serializers.BooleanField()
