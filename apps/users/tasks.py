from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_verification_code(email, verification_code):
    subject = "Verification Code"
    message = f"Your verification code is {verification_code}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
