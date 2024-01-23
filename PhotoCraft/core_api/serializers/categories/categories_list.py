from rest_framework import serializers

from models_app.models.categories.model import Categories


class CategoriesSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    sum = serializers.SerializerMethodField()

    @staticmethod
    def get_sum(self, obj):
        return sum(Categories.objects.filter(id=obj.id))
