from rest_framework import serializers


class VerifySignUpSerializer(serializers.Serializer):
    session = serializers.CharField()
    code = serializers.CharField()
