from rest_framework import serializers


class LikedSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    photo_id = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()

    def get_user_id(self, obj):
        return {
            'id': obj.user_id.id,
            }

    def get_photo_id(self, obj):
        return {
            'id': obj.photo_id.id,
            }
