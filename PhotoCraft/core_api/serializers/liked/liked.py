import json

from rest_framework import serializers


class LikedSerializer(serializers.Serializer):
    photo_id = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()

    def get_user_id(self, obj) -> json:
        return {
            'id': obj.user.id,
            }

    def get_photo_id(self, obj) -> json:
        return {
            'id': obj.photo.id,
            }
