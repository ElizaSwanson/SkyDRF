from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import timedelta


@shared_task
def send_email_task(user_email, subject, message):
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user_email])


@shared_task
def deactivate_inactive_users():
    one_month_ago = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=one_month_ago, is_active=True)
    inactive_users.update(is_active=False)
