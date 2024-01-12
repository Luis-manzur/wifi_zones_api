"""Create Pago Movil Permissions"""
# Django
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission, ContentType



class Command(BaseCommand):
    help = "Create Pago Movil permissions"

    def handle(self, *args, **options):
        content_type = ContentType.objects.get(id=1)
        permission = Permission.objects.create(
            codename='can_do_pago_movil_permission',
            name='Can do pago movil',
            content_type=content_type
        )

        permission.save()

        self.stdout.write("permission created successfully")
