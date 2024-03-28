from rest_framework import serializers

from models_app.models.photo.model import Photo


class CategoriesSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    count_photo = serializers.SerializerMethodField()

    def get_count_photo(self, obj) -> int:
        return Photo.objects.filter(category=obj.id).count()
