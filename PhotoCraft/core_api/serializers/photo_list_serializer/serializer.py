from rest_framework import serializers

from models_app.models.Liked.model import Liked
from models_app.models.Comments.model import Comments


class PhotoListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    photo_space = serializers.ImageField()
    category_id = serializers.IntegerField()
    number_of_likes = serializers.SerializerMethodField()
    number_of_comments = serializers.SerializerMethodField()

    @staticmethod
    def get_number_of_likes(self, obj):
        return Liked.objects.filter(photo_id=obj.photo_id).count()

    @staticmethod
    def get_number_of_comments(self, obj):
        return Comments.objects.filter(photo_id=obj.photo_id).count()

    class Meta:
        ref_name = 'core_api_photo_list_serializer'


