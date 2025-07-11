from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Creates the default user groups (Admin, Accountant, Site Staff) if they do not already exist.'

    DEFAULT_GROUPS = [
        'Admin',
        'Accountant',
        'Site Staff',
    ]

    def handle(self, *args, **options):
        created = 0
        for group_name in self.DEFAULT_GROUPS:
            group, was_created = Group.objects.get_or_create(name=group_name)
            if was_created:
                created += 1
                self.stdout.write(self.style.SUCCESS(f"Created group: {group_name}"))
            else:
                self.stdout.write(f"Group already exists: {group_name}")
        self.stdout.write(self.style.SUCCESS(f"Initialization complete. {created} new groups created."))
