import json

from rest_framework import serializers


class PersonalAreaSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    category_id = serializers.SerializerMethodField()

    title = serializers.CharField(required=True)
    description = serializers.CharField(required=False)
    photo_space = serializers.ImageField(required=True)
    status = serializers.CharField(required=True)

    publicated_at = serializers.DateTimeField(required=False)
    deleted_at = serializers.DateTimeField(required=False)
    updated_at = serializers.DateTimeField(required=False)
    first_request_at = serializers.DateTimeField(required=True)

    def get_category_id(self, obj) -> json:
        if obj.category_id:
            return {
                'id': obj.category_id.id,
                'title': obj.category_id.title,
            }
        return None
