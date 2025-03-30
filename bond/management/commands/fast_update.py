from django.core.management.base import BaseCommand

from bond.moex import fast_update


class Command(BaseCommand):
    help = 'Updating only prices and yields of bonds.'

    def handle(self, *args, **kwargs):
        fast_update()
        self.stdout.write("Fast update succeeded")
