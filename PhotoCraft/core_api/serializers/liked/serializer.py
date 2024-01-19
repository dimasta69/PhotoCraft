from rest_framework import serializers


class LikedSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    photo_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
