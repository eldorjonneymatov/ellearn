from typing import List

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField

from apps.common.models import TimeStampedModel
from apps.users.choices import ProfileRoleChoices
from apps.users.managers import CustomUserManager


class User(AbstractUser):
    full_name = models.CharField(_("Full Name"), max_length=255)
    email = models.EmailField(_("email address"), unique=True)

    username = None
    first_name = None
    last_name = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: List[str] = []
    objects = CustomUserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.email


class Profile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = ResizedImageField(
        _("Avatar"), size=[240, 240], crop=["middle", "center"], quality=90, upload_to="profile/avatars"
    )
    role = models.CharField(
        _("Role"), max_length=10, choices=ProfileRoleChoices.choices, default=ProfileRoleChoices.STUDENT
    )
    title = models.CharField(_("Job Title"), max_length=255, blank=True, null=True)
    description = models.TextField(_("Description"))
    website = models.URLField(_("Website"), blank=True, null=True)
    facebook = models.URLField(_("Facebook"), blank=True, null=True)
    twitter = models.URLField(_("Twitter"), blank=True, null=True)
    linkedin = models.URLField(_("Linkedin"), blank=True, null=True)
    telegram = models.URLField(_("Telegram"), blank=True, null=True)
    location = models.CharField(max_length=30, blank=True, null=True)
    total_course_taught = models.PositiveIntegerField(_("Total Course Taught"), null=True, blank=True)

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    def __str__(self):
        return f"{self.user.email} | {self.user.full_name}"


class TemporaryUser(TimeStampedModel):
    email = models.EmailField(_("Email"))
    password = models.CharField(_("Password"), max_length=128, null=True)
    session = models.CharField(_("Session"), max_length=32)
    verification_code = models.CharField(_("Verification Code"), max_length=6)
    full_name = models.CharField(_("Full Name"), max_length=255, null=True)

    class Meta:
        verbose_name = _("Temporary User")
        verbose_name_plural = _("Temporary Users")
        indexes = [models.Index(fields=["email", "session", "verification_code", "created"])]

    def __str__(self):
        return self.email
