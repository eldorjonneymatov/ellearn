from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.api.auth.VerifySignUp.serializers import VerifySignUpSerializer
from apps.users.models import User
from apps.users.utils import get_user_via_session_and_code


class VerifySignUpView(GenericAPIView):
    serializer_class = VerifySignUpSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            session = serializer.validated_data.get("session")
            code = serializer.validated_data.get("code")
            temp_user = get_user_via_session_and_code(session, code)
            if temp_user is None:
                raise ValidationError({"code": "Invalid code."}, code="invalid")
            user = User.objects.create_user(
                email=temp_user.email, password=temp_user.password, full_name=temp_user.full_name
            )
            temp_user.delete()
            refresh = RefreshToken.for_user(user)
            return Response({"refresh": str(refresh), "access": str(refresh.access_token)}, status=status.HTTP_200_OK)
        else:
            raise ValidationError(serializer.errors, code="invalid")
