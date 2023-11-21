"""Celery tasks."""

from __future__ import absolute_import, unicode_literals

from datetime import timedelta

import jwt
from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

from wifi_zones_api.users.models import User


def gen_verification_token(user, payload_type):
    """Create JWT token that the user can use to verify its account."""
    exp_date = timezone.now() + timedelta(days=3)
    payload = {
        "user": user.username,
        "exp": int(exp_date.timestamp()),
        "type": payload_type,
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token


@shared_task()
def send_confirmation_email(user_pk):
    """Send account verification link to given user."""
    user = User.objects.get(pk=user_pk)
    verification_token = gen_verification_token(user, "email_confirmation")
    subject = "Bienvenido @{}! Verifica tu cuenta antes de empezar a utilizar Datinvoz.".format(user)
    from_email = settings.DEFAULT_FROM_EMAIL
    url = f"{settings.URL}verify/?token={verification_token}"
    content = render_to_string(
        "emails/link.html",
        {"url": url, "message": subject, "title": "Verifica tu cuenta", "button_name": "Verificar"},
    )
    msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
    msg.attach_alternative(content, "text/html")
    msg.send()


@shared_task()
def send_password_recovery_email(user_pk):
    """Send password recovery link to given user."""
    user = User.objects.get(pk=user_pk)
    token = gen_verification_token(user, "password_recovery")
    url = f"{settings.URL}reset-password/?token={token}"
    subject = "Datinvoz reseteo de contraseña."
    message = f" {user} Recientemente solicitaste restablecer la contraseña de tu cuenta de Datinvoz. Para restablecer tu contraseña, haz clic en el siguiente enlace:"
    from_email = settings.DEFAULT_FROM_EMAIL
    content = render_to_string(
        "emails/link.html",
        {"url": url, "message": message, "title": "Reseteo de Contraseña", "button_name": "Cambiar contraseña"},
    )
    msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
    msg.attach_alternative(content, "text/html")
    msg.send()
