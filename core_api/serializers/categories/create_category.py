from rest_framework import serializers


class CreateCategoriesSerializer(serializers.Serializer):
    title = serializers.CharField()
