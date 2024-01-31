import random
import string

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from apps.users.models import TemporaryUser


def send_verification_code(email):
    verification_code = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    subject = "Verification Code"
    message = f"Your verification code is {verification_code}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
    return verification_code


def get_user_via_session_and_code(session, code):
    time_threshold = timezone.now() - timezone.timedelta(minutes=settings.OTP_VALIDITY)
    instances = TemporaryUser.objects.filter(session=session, verification_code=code, created__gte=time_threshold)
    if instances.exists():
        return instances.first()
    return None
