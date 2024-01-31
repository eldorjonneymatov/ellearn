from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.users.utils import get_user_via_session_and_code

from .serializers import VerifyChangeEmailSerializer

User = get_user_model()


class VerifyChangeEmailView(GenericAPIView):
    serializer_class = VerifyChangeEmailSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = request.user
            session = serializer.validated_data.get("session")
            code = serializer.validated_data.get("code")
            temp_user = get_user_via_session_and_code(session, code)
            if temp_user is None:
                raise ValidationError({"code": "Invalid code."}, code="invalid")
            if User.objects.filter(email=temp_user.email).exists():
                raise ValidationError({"email": "Email is already taken."}, code="invalid")
            user.email = temp_user.email
            user.save()
            temp_user.delete()
            return Response({"message": "Email changed successfully."}, status=status.HTTP_200_OK)
        else:
            raise ValidationError(serializer.errors, code="invalid")
