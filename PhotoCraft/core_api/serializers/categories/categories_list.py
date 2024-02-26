from rest_framework import serializers

from models_app.models.photo.model import Photo


class CategoriesSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    count = serializers.SerializerMethodField()

    def get_count(self, obj):
        return Photo.objects.filter(category_id=obj.id).count()
