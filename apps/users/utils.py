from django.conf import settings
from django.utils import timezone

from apps.users.models import TemporaryUser


def get_user_via_session_and_code(session, code):
    time_threshold = timezone.now() - timezone.timedelta(minutes=settings.OTP_VALIDITY)
    instances = TemporaryUser.objects.filter(session=session, verification_code=code, created__gte=time_threshold)
    if instances.exists():
        return instances.first()
    return None
