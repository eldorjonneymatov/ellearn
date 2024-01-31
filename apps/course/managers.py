from django.db import models

from apps.users.choices import ProfileRoleChoices


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status="published")


class StudentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role=ProfileRoleChoices.STUDENT)


class InstructorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role=ProfileRoleChoices.INSTRUCTOR)
