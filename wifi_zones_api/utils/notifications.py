"""Notification FCM"""
from fcm_django.models import FCMDevice


def send_push_notification(device_id, title, body):
    device = FCMDevice.objects.get(id=device_id)
    device.send_message(title=title, body=body)
