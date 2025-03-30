from django import template

from bond.models import *
from django.db.models import Count, F
from django.core.cache import cache
from datetime import datetime
from bond.config import *
register = template.Library()


@register.simple_tag()
def get_currency(bond):
    if bond.currency is None:
        return ''
    c = bond.currency.title

    if c == 'SUR' or c == 'RUB':
        return '₽'
    elif c == 'USD':
        return '$'
    elif c == 'EUR':
        return '€'
    else:
        return 'ед. '


def convert_currency(currency):
    if currency == '₽':
        return 'руб'
    elif currency == '$':
        return 'дол'
    elif currency == '€':
        return 'евро'
    else:
        return 'ед.'


@register.simple_tag()
def get_beautiful_int(x, currency):
    smth = [f' {currency}', f' тыс. {currency}', f' млн. {currency}', f' млрд. {currency}', f' трлн. {currency}']
    ind = 0
    while abs(x) > 1000:
        x /= 1000
        ind += 1
    x = round(x, 1)
    ans = str(x) + smth[ind]
    return ans


@register.simple_tag()
def get_issue_volume(bond):
    if bond.start_facevalue is not None and bond.issue_volume is not None:
        x = bond.start_facevalue * bond.issue_volume
        return get_beautiful_int(x, convert_currency(get_currency(bond)))
    else:
        return '---'


@register.simple_tag()
def get_liquidity_size(bond):
    if bond.liquidity is not None:
        return round(bond.liquidity / 1000000, 1)
    else:
        return '---'


@register.simple_tag()
def get_credit_rating_value(bond):
    if bond.emitter.credit_level is not None:
        return credit_ratings[bond.emitter.credit_level]
    else:
        return '---'


@register.simple_tag()
def get_line_color(bond):
    if bond.emitter.credit_level is None:
        return 'level-0'
    elif bond.emitter.credit_level <= 8:
        return 'level-1'
    elif bond.emitter.credit_level < 12:
        return 'level-2'
    elif bond.emitter.credit_level <= 14:
        return 'level-3'
    elif bond.emitter.credit_level <= 18:
        return 'level-4'
    else:
        return 'level-5'


@register.simple_tag()
def get_liquidity_color(bond):
    if bond.liquidity is None:
        return 'level-1'
    elif bond.liquidity <= 200000:
        return 'level-1'
    elif bond.liquidity < 1000000:
        return 'level-2'
    elif bond.liquidity <= 2000000:
        return 'level-3'
    elif bond.liquidity <= 5000000:
        return 'level-4'
    else:
        return 'level-5'


@register.simple_tag()
def get_time(bond):
    now = datetime.now().date()

    if bond.end_date is not None:
        delta = bond.end_date - now
        return delta.days
    else:
        return '---'


@register.simple_tag()
def get_ifrs_exists(bond, report_type):
    if report_type == 'ifrs':
        return 0
    if bond.emitter[('ifrs', 'assets', 'LTM')] > 1000000:
        return 1
    return 0


@register.simple_tag()
def get_rsbu_exists(bond, report_type):
    if report_type == 'rsbu':
        return 0
    if bond.emitter[('rsbu', 'assets', 'LTM')] > 1000000:
        return 1
    return 0


@register.simple_tag()
def get_ifrs_link(bond):
    url = f'/{bond.isin}/?report_type=ifrs'
    return url


@register.simple_tag()
def get_rsbu_link(bond):
    url = f'/{bond.isin}/?report_type=rsbu'
    return url


@register.simple_tag()
def get_time2(bond):
    now = datetime.now().date()

    if bond.end_date is not None:
        delta = bond.end_date - now
        return delta.days
    else:
        return -1


@register.simple_tag()
def get_offer_exist(bond):
    now = datetime.now().date()
    if Payment.objects.filter(bond=bond, date__gt=now, type__pk__in=[3, 4, 6, 7, 8, 9]).exists():
        return 1
    else:
        return 0


@register.simple_tag()
def get_offer(bond):
    now = datetime.now().date()
    return Payment.objects.filter(bond=bond, date__gt=now, type__pk__in=[3, 4, 6, 7, 8, 9]).first().date


@register.simple_tag()
def get_amortization_exist(bond):
    if Payment.objects.filter(bond=bond, type__pk=1).exists():
        return 1
    else:
        return 0


@register.simple_tag()
def get_payments(bond):
    p = Payment.objects.filter(bond=bond).order_by('date', 'type__order_id')
    return p


@register.simple_tag()
def get_zero():
    return 0


@register.simple_tag()
def get_pasted_date(p):
    now = datetime.now().date()
    if p.date < now:
        return 1
    else:
        return 0


@register.simple_tag()
def get_cache_name(emitter, report_type):
    print(emitter, emitter.id, report_type)
    print(f'emitter-info-{emitter.id}-{report_type}')
    return f'emitter-info-{emitter.id}-{report_type}'







