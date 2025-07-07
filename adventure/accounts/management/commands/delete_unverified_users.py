from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import timedelta

class Command(BaseCommand):
    # Deletes users who haven't verified their email within 2 minutes.

    def handle(self, *args, **kwargs):
        cutoff_time = timezone.now() - timedelta(minutes=2)
        users_to_delete = User.objects.filter(is_active=False, date_joined__lt=cutoff_time)

        count = users_to_delete.count()
        users_to_delete.delete()

        self.stdout.write(self.style.SUCCESS(f"Deleted {count} unverified users."))