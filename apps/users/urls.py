from django.urls import path

from apps.users.api import auth

app_name = "users"

urlpatterns = [
    path("SignUp/", auth.SignUpView.as_view(), name="SignUp"),
    path("VerifySignUp/", auth.VerifySignUpView.as_view(), name="VerifySignUp"),
    path("LogIn/", auth.LogInView.as_view(), name="LogIn"),
    path("ChangePassword/", auth.ChangePasswordView.as_view(), name="ChangePassword"),
    path("VerifyChangePassword/", auth.VerifyChangePasswordView.as_view(), name="VerifyChangePassword"),
    path("ChangeEmail/", auth.ChangeEmailView.as_view(), name="ChangeEmail"),
    path("VerifyChangeEmail/", auth.VerifyChangeEmailView.as_view(), name="VerifyChangeEmail"),
]
