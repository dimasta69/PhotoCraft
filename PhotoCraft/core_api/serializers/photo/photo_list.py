from rest_framework import serializers

from models_app.models.liked.model import Liked
from models_app.models.comments.model import Comments
from models_app.models.categories.model import Categories
from models_app.models.users.model import User


class PhotoListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    category_id = serializers.PrimaryKeyRelatedField(queryset=Categories.objects.all(), allow_null=True, required=False)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), allow_null=True, required=False)
    title = serializers.CharField()
    photo_space = serializers.ImageField()
    status = serializers.CharField()
    number_of_likes = serializers.SerializerMethodField()
    number_of_comments = serializers.SerializerMethodField()


    def get_number_of_likes(self, obj):
        return Liked.objects.filter(photo_id=obj.id).count()

    def get_number_of_comments(self, obj):
        return Comments.objects.filter(photo_id=obj.id).count()

    class Meta:
        ref_name = 'core_api_photo_list_serializer'


