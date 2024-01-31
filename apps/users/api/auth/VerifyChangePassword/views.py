from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.users.utils import get_user_via_session_and_code

from .serializers import VerifyChangePasswordSerializer

User = get_user_model()


class VerifyChangePasswordView(GenericAPIView):
    serializer_class = VerifyChangePasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            session = serializer.validated_data.get("session")
            code = serializer.validated_data.get("code")
            temp_user = get_user_via_session_and_code(session, code)
            if temp_user is None:
                raise ValidationError({"code": "Invalid code."}, code="invalid")
            email = temp_user.email
            user = User.objects.filter(email=email)
            if not user.exists():
                raise ValidationError({"email": "User does not exist."}, code="invalid")
            user = user.first()
            user.password = temp_user.password
            user.save()
            temp_user.delete()
            return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)
        else:
            raise ValidationError(serializer.errors, code="invalid")
