from rest_framework import serializers


class VerifyChangePasswordSerializer(serializers.Serializer):
    session = serializers.CharField()
    code = serializers.CharField()
