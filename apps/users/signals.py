from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.users.choices import ProfileRoleChoices
from apps.users.models import Profile, User


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser:
            Profile.objects.create(user=instance, role=ProfileRoleChoices.ADMIN)
        else:
            Profile.objects.create(user=instance, role=ProfileRoleChoices.STUDENT)


# from django.db.models.signals import post_delete
# from django.dispatch import receiver
# @receiver(post_delete, sender=User)
# def delete_user_profile(sender, instance, **kwargs):
#     instance.profile.delete()
