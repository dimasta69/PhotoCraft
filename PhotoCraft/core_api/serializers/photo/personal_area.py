from rest_framework import serializers

from models_app.models.categories.model import Categories


class PersonalAreaSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Categories.objects.all(), required=False)

    title = serializers.CharField(required=True)
    description = serializers.CharField(required=False)
    photo_space = serializers.ImageField(required=True)
    status = serializers.CharField(required=True)

    publicated_at = serializers.DateTimeField(required=False)
    deleted_at = serializers.DateTimeField(required=False)
    updated_at = serializers.DateTimeField(required=False)
    first_request_at = serializers.DateTimeField(required=True)

