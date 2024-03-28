import json

from rest_framework import serializers


class CommentsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user = serializers.SerializerMethodField()
    photo_id = serializers.SerializerMethodField()
    reply_id = serializers.SerializerMethodField()
    text = serializers.CharField()
    publicated_at = serializers.DateTimeField()
    updated_at = serializers.BooleanField()

    def get_user(self, obj) -> json:
        return {
            'id': obj.user.id,
            'is_superuser': obj.user.is_superuser,
            'username': obj.user.username,
        }

    def get_photo_id(self, obj) -> int:
        return obj.photo.id

    def get_reply_id(self, obj) -> int:
        if obj.reply:
            return obj.reply.id
        return None
