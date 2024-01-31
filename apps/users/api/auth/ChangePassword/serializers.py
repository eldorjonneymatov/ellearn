from rest_framework import serializers


class ChangePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    password_confirm = serializers.CharField()
