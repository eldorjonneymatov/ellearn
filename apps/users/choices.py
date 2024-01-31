from django.db import models
from django.utils.translation import gettext_lazy as _


class ProfileRoleChoices(models.TextChoices):
    STUDENT = "student", _("Student")
    INSTRUCTOR = "instructor", _("Instructor")
    ADMIN = "admin", _("Admin")
