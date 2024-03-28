from rest_framework import serializers


class CreatePhotoSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    photo = serializers.ImageField()
    category_id = serializers.IntegerField()
    status = serializers.CharField()
