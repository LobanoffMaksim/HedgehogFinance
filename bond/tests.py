from django.test import SimpleTestCase
from django.urls import reverse
from bond.models import *

from requests import head


def test_bond():
    for emitter in Emitter.objects.all():
        if not emitter.bond_set.count():
            continue
        bond = emitter.bond_set.first()

        response = head(f'https://hedgehog-finance.ru/bond/{bond.isin}/')

        if response.status_code != 200:
            print(emitter.title, bond.isin, "Статус",  response.status_code)
        else:
            print(emitter.title, bond.isin, "Успех")
