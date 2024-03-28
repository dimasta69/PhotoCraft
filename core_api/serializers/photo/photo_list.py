import json

from rest_framework import serializers

from models_app.models.liked.model import Liked
from models_app.models.comments.model import Comments


class PhotoListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    title = serializers.CharField()
    photo_space = serializers.ImageField()
    status = serializers.CharField()
    number_of_likes = serializers.SerializerMethodField()
    number_of_comments = serializers.SerializerMethodField()


    def get_number_of_likes(self, obj) -> int:
        return Liked.objects.filter(photo_id=obj.id).count()

    def get_number_of_comments(self, obj) -> int:
        return Comments.objects.filter(photo_id=obj.id).count()

    def get_user(self, obj) -> json:
        return {
            'id': obj.user.id,
            'is_superuser': obj.user.is_superuser,
            'username': obj.user.username,
            }

    def get_category(self, obj) -> json:
        if obj.category:
            return {
                'id': obj.category.id,
                'title': obj.category.title,
            }

    class Meta:
        ref_name = 'core_api_photo_list_serializer'


