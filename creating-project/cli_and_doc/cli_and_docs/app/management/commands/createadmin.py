import hashlib
import re

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.UserModel = get_user_model()
        self.username_field = self.UserModel._meta.get_field(self.UserModel.USERNAME_FIELD)

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        while True:
            username = input("Username (leave blank to use 'admin'): ").strip()
            username = 'admin' if not username else username

            if username in [user.__dict__[self.username_field.attname] for user in self.UserModel.objects.all()]:
                self.stderr.write('Error: That username is already taken.')
                continue
            else:
                break

        while True:
            email_check = r'(?P<name>^[A-Za-z0-9\-_]+)@(?P<mail>[A-Za-z0-9\-_]+).(?P<domain>\w+)$'
            email = input('Email address: ').strip()
            if email and not re.match(email_check, email):
                self.stderr.write('Error: Enter a valid email address.')
                continue
            break

        while True:
            pwd = input('Password: ').strip()
            pwd2 = input('Password (again): ').strip()
            if not pwd2:
                self.stderr.write("Error: Blank passwords aren't allowed.")
            elif pwd != pwd2:
                self.stderr.write("Error: Your passwords didn't match.")
            else:
                pwd_md5 = hashlib.md5(pwd.encode()).hexdigest()
                break

        new_admin = self.UserModel(username=username, email=email, password=pwd_md5, is_superuser=True, is_staff=True)
        new_admin.save()

        self.stdout.write(self.style.SUCCESS(f'Success! New superuser {new_admin.username} was created.'))
