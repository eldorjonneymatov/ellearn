from rest_framework import serializers


class VerifyChangeEmailSerializer(serializers.Serializer):
    session = serializers.CharField()
    code = serializers.CharField()
