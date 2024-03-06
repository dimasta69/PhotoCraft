from rest_framework import serializers

from models_app.models.liked.model import Liked
from models_app.models.comments.model import Comments


class PhotoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    description = serializers.CharField()
    user_id = serializers.SerializerMethodField()
    photo = serializers.ImageField()
    category_id = serializers.SerializerMethodField()
    status = serializers.CharField()
    number_of_likes = serializers.SerializerMethodField()
    number_of_comments = serializers.SerializerMethodField()

    def get_number_of_likes(self, obj):
        return Liked.objects.filter(photo_id=obj.id).count()

    def get_number_of_comments(self, obj):
        return Comments.objects.filter(photo_id=obj.id).count()

    def get_user_id(self, obj):
        return {
            'id': obj.user_id.id,
            'is_superuser': obj.user_id.is_superuser,
            'username': obj.user_id.username,
            }

    def get_category_id(self, obj):
        if obj.category_id:
            return {
                'id': obj.category_id.id,
                'title': obj.category_id.title,
            }
        return None

    class Meta:
        ref_name = 'core_api_photo_serializer'
