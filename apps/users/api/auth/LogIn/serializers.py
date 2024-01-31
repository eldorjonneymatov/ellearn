from rest_framework import serializers


class LogInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
