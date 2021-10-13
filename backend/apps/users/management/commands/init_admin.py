import os

from django.core.management.base import BaseCommand

from ...models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        username = os.environ.get('PROD_USER')
        email = os.environ.get('PROD_USER_EMAIL')
        password = os.environ.get('PROD_USER_PASS')

        if username and email and password and not User.objects.filter(
                username=username).exists():
            print('Creating account for %s (%s)' % (username, email))
            User.objects.create_superuser(
                email=email, username=username, password=password)
