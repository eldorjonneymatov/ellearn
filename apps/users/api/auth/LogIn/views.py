from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .serializers import LogInSerializer

User = get_user_model()


class LogInView(GenericAPIView):
    serializer_class = LogInSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")
            user = User.objects.filter(email=email)
            if not user.exists() or not user.first().check_password(password):
                raise ValidationError({"credentials": "Username or password is wrong."}, code="invalid")
            tokens = user.first().get_tokens()
            return Response(tokens, status=status.HTTP_200_OK)
        else:
            raise ValidationError(serializer.errors, code="invalid")
