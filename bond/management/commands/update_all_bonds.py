from django.core.management.base import BaseCommand
from django.utils import timezone

from bond.moex import update_all_bonds


class Command(BaseCommand):
    help = 'Updating all bonds data.'

    def add_arguments(self, parser):
        parser.add_argument('moex_info', type=bool, default=False,
                            help='1 if we want to update moex_info for all bonds. 0 if we want to update only new ones')
        parser.add_argument('payments', type=bool, default=False,
                            help='1 if we want to update payments for all bonds. 0 if we want to update only new ones')

    def handle(self, *args, **kwargs):
        moex_info = kwargs['moex_info']
        add_payments = kwargs['payments']
        update_all_bonds(moex_info, add_payments)
        self.stdout.write("Updating all bonds data succeeded")
