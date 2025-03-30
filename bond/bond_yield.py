from pyxirr import xirr

from bond.models import *
from datetime import datetime


def get_yield_xirr():

    """
    Calculating xirr yield for all bonds.
    :return:
    """
    for bond in Bond.objects.all():
        try:
            start = datetime.now().date()
            start_price = bond.price * bond.facevalue / 100 + bond.coupon.aci
            dates = [start, ]
            amounts = [-start_price]
            amortization_exists = 0
            end_exists = 0
            for event in Payment.objects.filter(bond=bond, date__gt=start, date__lte=bond.end_date).order_by('date',
                                                                                                             'type_id'):
                if event.type.id == 1:
                    amortization_exists = 1
                if event.type.id in [1, 2]:
                    if event.type_id == 2 and (event.date - datetime.now().date()).days <= 3 and bond.coupon.aci == 0:
                        continue
                    dates.append(event.date)
                    amounts.append(event.size)
                else:
                    if amortization_exists:
                        break
                    end_exists = 1
                    dates.append(event.date)
                    amounts.append(bond.facevalue)
                    break
            if amortization_exists == 0 and end_exists == 0:
                dates.append(bond.end_date)
                amounts.append(bond.facevalue)
            bond.yield_to_maturity = round(xirr(dates, amounts) * 100, 2)
            bond.save()
        except Exception as ex:
            print('get_yield_xirr', bond.isin, ex)
