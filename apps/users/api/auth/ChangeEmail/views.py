import random
import string

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.users.models import TemporaryUser
from apps.users.utils import send_verification_code

from .serializers import ChangeEmailSerializer

User = get_user_model()


class ChangeEmailView(GenericAPIView):
    serializer_class = ChangeEmailSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = request.user
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")
            if not user.check_password(password):
                raise ValidationError({"password": "Password is wrong."}, code="invalid")
            if User.objects.filter(email=email).exists():
                raise ValidationError({"email": "Email is already taken."}, code="invalid")
            session = "".join(random.choices(string.ascii_uppercase + string.digits, k=18))
            code = send_verification_code(email)
            TemporaryUser.objects.create(
                session=session,
                verification_code=code,
                email=email,
            )
            return Response({"session": session}, status=status.HTTP_200_OK)
        else:
            raise ValidationError(serializer.errors, code="invalid")
