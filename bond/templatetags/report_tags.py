from django import template

from bond.models import *
from django.core.cache import cache
from bond.config import *
from bond.templatetags.bond_tags import get_beautiful_int

register = template.Library()


@register.simple_tag()
def conv_round(data, iunit, round_to):
    return [round(item / iunit, round_to) for item in data]


@register.simple_tag()
def get_revenue_data(e, report_type, round_to=2):
    unit, iunit = get_unit(e[(report_type, 'revenue', 'LTM')])

    labels = e.interesting_years(report_type)
    revenue = conv_round(e[(report_type, 'revenue', 'all')], iunit, round_to)
    net_profit = conv_round(e[(report_type, 'net-profit', 'all')], iunit, round_to)
    operation_profit = conv_round(e[(report_type, 'operation-profit', 'all')], iunit, round_to)
    ebitda = conv_round(e[(report_type, 'ebitda', 'all')], iunit, round_to)
    assets = conv_round(e[(report_type, 'assets', 'all')], iunit, round_to)
    equity = conv_round(e[(report_type, 'equity', 'all')], iunit, round_to)
    short_assets = conv_round(e[(report_type, 'current-assets', 'all')], iunit, round_to)
    short_liabilities = conv_round(e[(report_type, 'short-liabilities', 'all')], iunit, round_to)
    long_assets = conv_round(e[(report_type, 'non-current-assets', 'all')], iunit, round_to)
    long_liabilities = conv_round(e[(report_type, 'long-liabilities', 'all')], iunit, round_to)
    net_debt = conv_round(e[(report_type, 'net_debt', 'all')], iunit, round_to)
    cash = conv_round(e[(report_type, 'cash', 'all')], iunit, round_to)
    fast_liquidity = conv_round(e[(report_type, 'fast-liquidity', 'all')], iunit, round_to)
    ebit = conv_round(e[(report_type, 'ebt', 'all')], iunit, round_to)
    amortization = conv_round(e[(report_type, 'amortization', 'all')], iunit, round_to)
    interest_payable = conv_round(e[(report_type, 'interest-payable', 'all')], iunit, round_to)

    return [unit, labels, revenue, net_profit, operation_profit, ebitda, assets, equity,
            short_assets, short_liabilities, long_assets, long_liabilities, net_debt, cash,
            fast_liquidity, ebit, amortization, interest_payable]
    # last - 7
    # last - 13


@register.simple_tag()
def get_fin_indicators(e, report_type, title, round_to=2):
    unit, iunit = get_unit(e[(report_type, 'revenue', 'LTM')])

    return conv_round(e[(report_type, title, 'all')], iunit, round_to)


def calc_cagr(start_val, finish_val, number_of_years):
    if start_val < 0 and finish_val < 0:
        start_val, finish_val = -finish_val, -start_val
    if finish_val < 0:
        return -100
    if start_val < 0:
        return 100
    if start_val == 0:
        return 100

    return round(((finish_val / start_val) ** (1 / number_of_years) - 1) * 100, 1)


@register.simple_tag()
def get_revenue_cagr(e, report_type):
    return [e[(report_type, 'cagr-1-revenue', 'LTM')], e[(report_type, 'cagr-3-revenue', 'LTM')],
            e[(report_type, 'cagr-5-revenue', 'LTM')]]


@register.simple_tag()
def get_income_cagr(e, report_type):

    return [e[(report_type, 'cagr-1-net-profit', 'LTM')], e[(report_type, 'cagr-3-net-profit', 'LTM')], e[(report_type, 'cagr-5-net-profit', 'LTM')]]


def conv_precents(data, round_to):
    return [round(x * 100, round_to) for x in data]


@register.simple_tag()
def get_margin(e, report_type, round_to=1):
    return [conv_precents(e[(report_type, 'net-profit/revenue', 'all')], round_to),
            conv_precents(e[(report_type, 'operation-profit/revenue', 'all')], round_to),
            conv_precents(e[(report_type, 'ebitda/revenue', 'all')], round_to)]


@register.simple_tag()
def get_profitability(e, report_type, round_to=1):
    return [conv_precents(e[(report_type, 'net-profit/assets', 'all')], round_to),
            conv_precents(e[(report_type, 'net-profit/equity', 'all')], round_to)]


@register.simple_tag()
def get_assets_and_liabilities(e, report_type):
    assets = [get_fin_indicators(e, report_type, 'current-assets')[-1],
              get_fin_indicators(e, report_type, 'non-current-assets')[-1]]
    liabilities = [get_fin_indicators(e, report_type, 'short-liabilities')[-1],
                   get_fin_indicators(e, report_type, 'long-liabilities')[-1]]
    return [assets, liabilities]


@register.simple_tag()
def get_liquidity(e, report_type):
    short_liabilities = get_fin_indicators(e, report_type, 'short-liabilities')[-1]
    short_assets = get_fin_indicators(e, report_type, 'current-assets')[-1]
    cash = get_fin_indicators(e, report_type, 'cash')[-1]
    fast_liquidity = get_fin_indicators(e, report_type, 'fast_liquidity')[-1]

    return [short_liabilities, short_assets, fast_liquidity, cash]


@register.simple_tag()
def get_ebitda(e, report_type):
    net_profit = e[(report_type, 'net-profit', 'LTM')]
    taxes = e[(report_type, 'ebt', 'LTM')] - net_profit
    amortization = e[(report_type, 'amortization', 'LTM')]
    interest_payble = e[(report_type, 'interest-payable', 'LTM')]

    ans = [net_profit, taxes, amortization, interest_payble]
    for i in range(len(ans)):
        ans[i] = max(ans[i], 0)
    ebitda = net_profit + taxes + amortization + interest_payble
    titles = ['Прибыль', 'Налоги', 'Амортизация', 'Проценты к уплате']
    return [ans, titles, get_beautiful_int(ebitda, 'млн. руб')]


@register.simple_tag()
def get_net_debt_ebitda(e, report_type):
    ebitda = get_fin_indicators(e, report_type, 'ebitda', 10)[-1]
    net_debt = get_fin_indicators(e, report_type, 'net_debt', 10)[-1]
    equity = get_fin_indicators(e, report_type, 'equity', 10)[-1]
    return [round(net_debt / ebitda, 2), round(net_debt / equity, 2)]


@register.simple_tag()
def get_leasing_debt_data(e, report_type):
    assets = get_fin_indicators(e, report_type, 'assets', 10)[-1]
    net_debt = get_fin_indicators(e, report_type, 'net_debt', 10)[-1]
    equity = get_fin_indicators(e, report_type, 'equity', 10)[-1]
    return [round(assets / net_debt, 2), int(round(equity / assets, 2) * 100)]


def clean_credit_rating(rating):
    if rating is None:
        return ''
    need = ['A', 'B', 'C', 'D', 'a', 'b', 'c', 'd', '+', '-']
    ans = ''
    for c in rating:
        if c in need:
            ans += c
    return ans


@register.simple_tag()
def get_credit_rating(e):
    if e.credit_level is None:
        return -2
    if e.credit_level < 12:
        return -1
    if e.credit_level < 15:
        return 0
    else:
        return 1

