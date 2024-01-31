from rest_framework import serializers


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    password_confirm = serializers.CharField()
    full_name = serializers.CharField()
