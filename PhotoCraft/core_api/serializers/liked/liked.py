from rest_framework import serializers

from models_app.models.photo.model import Photo
from models_app.models.users.model import User


class LikedSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    photo_id = serializers.PrimaryKeyRelatedField(queryset=Photo.objects.all())
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
