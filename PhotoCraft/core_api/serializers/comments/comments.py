import json

from rest_framework import serializers


class CommentsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user_id = serializers.SerializerMethodField()
    photo_id = serializers.SerializerMethodField()
    reply_id = serializers.SerializerMethodField()
    text = serializers.CharField()
    publicated_at = serializers.DateTimeField()
    updated_at = serializers.BooleanField()

    def get_user_id(self, obj) -> json:
        return {
            'id': obj.user_id.id,
            'is_superuser': obj.user_id.is_superuser,
            'username': obj.user_id.username,
        }

    def get_photo_id(self, obj) -> json:
        return {
            'id': obj.photo_id.id,
        }

    def get_reply_id(self, obj) -> json:
        if obj.reply_id:
            return {
                'id': obj.reply_id.id
            }
        return None


