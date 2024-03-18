import json

from rest_framework import serializers


class CommentsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()
    reply = serializers.SerializerMethodField()
    text = serializers.CharField()
    publicated_at = serializers.DateTimeField()
    updated_at = serializers.BooleanField()

    def get_user(self, obj) -> json:
        return {
            'id': obj.user.id,
            'is_superuser': obj.user.is_superuser,
            'username': obj.user.username,
        }

    def get_photo(self, obj) -> json:
        return {
            'id': obj.photo.id,
        }

    def get_reply(self, obj) -> json:
        if obj.reply:
            return {
                'id': obj.reply.id
            }
        return None


