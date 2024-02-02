import random
import string

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.users.api.auth.SignUp.serializers import SignUpSerializer
from apps.users.models import TemporaryUser
from apps.users.tasks import send_verification_code

User = get_user_model()


class SignUpView(GenericAPIView):
    serializer_class = SignUpSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")
            full_name = serializer.validated_data.get("full_name")
            password_confirm = serializer.validated_data.get("password_confirm")
            error = self.check_inputs(email, password, password_confirm)
            if error:
                raise ValidationError(error, code="invalid")
            session = "".join(random.choices(string.ascii_uppercase + string.digits, k=32))
            hashed_password = make_password(password)
            code = "".join(random.choices(string.ascii_uppercase, k=6))
            send_verification_code.delay(email, code)
            TemporaryUser.objects.create(
                email=email, password=hashed_password, session=session, verification_code=code, full_name=full_name
            )
            return Response({"session": session}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def check_inputs(self, email, password, password_confirm):
        if User.objects.filter(email=email).exists():
            return {"email": "Email is already used."}
        if password != password_confirm:
            return {"password": "Passwords do not match."}
        return None
