from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='bobr@kurwa.kek',
            first_name='Bobr',
            last_name='Kurwa',
            is_superuser=True,
            is_staff=True,
            is_active=True,
        )
        user.set_password('1111')
        user.save()
