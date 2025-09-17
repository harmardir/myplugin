from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Say hello from MyPlugin"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Hello from MyPlugin!"))
