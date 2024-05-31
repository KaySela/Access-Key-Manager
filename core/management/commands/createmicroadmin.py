from django.core.management.base import BaseCommand
from core.models import School
from django.core.exceptions import ValidationError
import os
from dotenv import load_dotenv


load_dotenv()

class Command(BaseCommand):
    help = 'Create micro-focus admin user'

    def handle(self, *args, **options):
        email = os.getenv('MICRO_ADMIN_USER')
        password = os.getenv('MICRO_ADMIN_PASSWORD')

        if not School.objects.filter(email=email).exists():
            try:
                School.objects.create_superuser(username="microadmin", email=email, password=password)
                self.stdout.write(self.style.SUCCESS('Successfully created micro-focus admin'))
            except ValidationError as e:
                self.stdout.write(self.style.ERROR('Error creating superuser: {}'.format(e)))
        else:
            self.stdout.write(self.style.WARNING('Superuser already exists'))