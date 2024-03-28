from rest_framework import serializers


class CreateCommentsSerializer(serializers.Serializer):
    photo_id = serializers.IntegerField()
    reply_id = serializers.IntegerField()
    text = serializers.CharField()



