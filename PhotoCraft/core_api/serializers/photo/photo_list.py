from rest_framework import serializers

from models_app.models.liked.model import Liked
from models_app.models.comments.model import Comments
from models_app.models.categories.model import Categories


class PhotoListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    photo_space = serializers.ImageField()
    category_id = serializers.PrimaryKeyRelatedField(queryset=Categories.objects.all(), allow_null=True, required=False)
    number_of_likes = serializers.SerializerMethodField()
    number_of_comments = serializers.SerializerMethodField()

    def get_number_of_likes(self, obj):
        return Liked.objects.filter(photo_id=obj.id).count()

    def get_number_of_comments(self, obj):
        return Comments.objects.filter(photo_id=obj.id).count()

    class Meta:
        ref_name = 'core_api_photo_list_serializer'


