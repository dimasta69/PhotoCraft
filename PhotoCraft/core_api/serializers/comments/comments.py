from rest_framework import serializers

from models_app.models.photo.model import Photo
from models_app.models.users.model import User
from models_app.models.comments.model import Comments


class CommentsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    photo_id = serializers.PrimaryKeyRelatedField(queryset=Photo.objects.all())
    reply_id = serializers.PrimaryKeyRelatedField(queryset=Comments.objects.all(), allow_null=True, required=False)
    text = serializers.CharField()
    publicated_at = serializers.DateTimeField()
    updated_at = serializers.BooleanField()
