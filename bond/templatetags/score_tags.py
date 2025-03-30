from django import template

from bond.models import *
from django.core.cache import cache
from bond.config import *
from bond.templatetags.bond_tags import get_beautiful_int
from bond.templatetags.report_tags import get_fin_indicators

register = template.Library()


@register.simple_tag()
def get_score(e, report_type, titles):

    scores = []
    for title in titles:
        if title[0] == '-':
            flag = 1
            title = title[1:]
        else:
            flag = 0
        if 'LTM' not in e.interesting_years(report_type):
            continue
        x = e[(report_type, title, 'LTM')]
        if title == 'cnt-default-scores':
            scores.append(100 - 20 * x)
            continue
        if x == 0:
            continue
        y = MedianValue.objects.get(sector=e.sector, title=title, report_type=report_type).value


        if x > y * 2:
            scores.append(100)
        elif x < y / 2:
            scores.append(0)
        elif x < y:
            scores.append((x - y / 2) / (y / 2) * 50)
        else:
            scores.append(x / y * 50)
        if flag:
            scores[-1] = 100 - scores[-1]

    if len(scores) == 0:
        return 0
    score = sum(scores) / len(scores)
    return round(score, 2)


def business_score(e, report_type, answer_type=1):
    scores = []
    scores.append(100 - e.sector.risk_level * 20)
    x = e[(report_type, 'ebitda', 'LTM')]
    if x < 10**8:
        scores.append(0)
    elif x < 10**9:
        scores.append(25)
    elif x < 5 * 10**9:
        scores.append(50)
    elif x < 10 * 10 ** 9:
        scores.append(75)
    else:
        scores.append(100)

    x = 0
    if sum(e[(report_type, 'financial-investments/ebitda', 'all')]) < 0.6:
        x += 40
    if sum(e[(report_type, 'borrow-outflow/ebitda', 'all')]) < 0.25:
        x += 20
    if e.ifrs_exists:
        x += 10
    if e[(report_type, 'cash', 'LTM')] > 5 * 10**6:
        x += 20
    if e[(report_type, 'other-income/revenue', 'LTM')] < 0.1:
        x += 10
    scores.append(x)
    if scores[1] == 100:
        scores[2] = 100
    if answer_type == 1:
        return round(scores[0] * 0.2 + scores[1] * 0.4 + scores[2] * 0.4, 2)
    else:
        return scores


@register.simple_tag()
def get_all_scores(e, report_type):
    titles = ['cagr-3-revenue', 'cagr-3-net-profit', 'cagr-3-ebitda', 'CAPEX/ebitda']
    growth_score = get_score(e, report_type, titles=titles)
    titles = ['net-profit/revenue', 'operation-profit/revenue', 'ebitda/revenue', '-turnover-accounts-receivable',
              '-turnover-inventories', '-turnover-current-assets', 'OCF/revenue', 'FCF/revenue']
    efficiency_score = get_score(e, report_type, titles=titles)
    titles = ['-net_debt/ebitda', '-interest-payable/ebitda', '-equity/assets', 'cnt-default-scores']
    health_score = get_score(e, report_type, titles=titles)
    titles = ['current-assets/short-liabilities', 'fast_liquidity/short-liabilities', 'cash/short-liabilities',
              'OCF/short-liabilities', 'operating-working-capital/assets']
    liquidity_score = get_score(e, report_type, titles=titles)
    transparency_score = business_score(e, report_type)
    # print(growth_score, efficiency_score, health_score, liquidity_score, transparency_score)
    return [transparency_score, health_score, efficiency_score, liquidity_score, growth_score]


@register.simple_tag()
def get_color(e, report_type):
    scores = get_all_scores(e, report_type)
    score = sum(scores[1:]) * scores[0] / 100
    if score < 60:
        return ['rgb(255, 51, 36)', 'rgba(255, 51, 36, 0.5)']
    elif score < 100:
        return ['rgb(255, 101, 37)', 'rgba(255, 101, 37, 0.5)']
    elif score < 180:
        return ['rgb(174, 214, 71)', 'rgba(174, 214, 71, 0.5)']
    else:
        return ['rgb(144, 184, 129)', 'rgba(144, 184, 129, 0.5)']


@register.simple_tag()
def get_growth(e, report_type):
    return [[round(e[(report_type, 'cagr-3-revenue', 'LTM')], 1), round(e[(report_type, 'cagr-3-ebitda', 'LTM')], 1), round(e[(report_type, 'cagr-3-net-profit', 'LTM')], 1)],
            [MedianValue.objects.get(report_type=report_type, sector=e.sector, title='cagr-3-revenue').value,
             MedianValue.objects.get(report_type=report_type, sector=e.sector, title='cagr-3-ebitda').value,
             MedianValue.objects.get(report_type=report_type, sector=e.sector, title='cagr-3-net-profit').value,]]


@register.simple_tag()
def get_margin_gradient(e, report_type, opacity):
    val = max(e[(report_type, 'net-profit/revenue', 'all')])
    mv = MedianValue.objects.get(report_type=report_type, sector=e.sector, title='net-profit/revenue').value
    ans = []
    ans.append([0, f'rgba(255, 0, 0, {opacity})'])
    if val > mv / 2:
        ans.append([(mv / 2) / val, f'rgba(255, 0, 0, {opacity})'])
        if val > mv:
            ans.append([mv / val, f'rgba(255, 191, 0, {opacity})'])
            if val > mv * 2:
                ans.append([mv * 2 / val, f'rgba(0, 191, 82, {opacity})'])
                ans.append([1, f'rgba(0, 191, 82, {opacity})'])
            else:
                ans.append([1, f'rgba({255 - int(val / (mv * 2) * 255)}, 191, 82, {opacity})'])
        else:
            ans.append([1, f'rgba(255, {int(val / mv * 191)}, 0, {opacity}'])

    else:
        ans.append([1, f'rgba(255, 0, 0, {opacity})'])
    return ans


@register.simple_tag()
def get_median_values(e, report_type):
    titles = ['net-profit/revenue', 'ebitda/revenue', 'OCF/revenue', 'turnover-accounts-receivable',
              'turnover-inventories', 'turnover-current-assets', 'Altman-score', 'Springate-score',
              'Lis-score', 'Taffler-score', 'current-assets/short-liabilities', 'fast_liquidity/short-liabilities',
              'cash/short-liabilities', 'operating-working-capital/assets', ]
    ans = []
    for title in titles:
        num = len(e.interesting_years(report_type))
        if 'score' not in title:
            val = MedianValue.objects.get(report_type=report_type, sector=e.sector, title=title).value
        if 'revenue' in title:
            ans.append([val * 100 for i in range(num)])
        elif 'turnover' in title:
            ans.append([val for i in range(num - 1)])
        elif title == 'Altman-score':
            ans.append([1.23 for i in range(num)])
        elif title == 'Springate-score':
            ans.append([0.865 for i in range(num)])
        elif title == 'Lis-score':
            ans.append([0.037 for i in range(num)])
        elif title == 'Taffler-score':
            ans.append([0 for i in range(num)])
        else:
            ans.append([val for i in range(num)])
    return ans


@register.simple_tag()
def get_margin_values(e, report_type):
    titles = ['net-profit/revenue', 'ebitda/revenue', 'OCF/revenue', 'turnover-accounts-receivable',
              'turnover-inventories', 'turnover-current-assets', 'Altman-score', 'Springate-score',
              'Lis-score', 'Taffler-score', 'current-assets/short-liabilities', 'fast_liquidity/short-liabilities',
              'cash/short-liabilities', 'operating-working-capital/assets', 'financial-investments', 'cash']
    ans = []
    for title in titles:
        if 'revenue' in title:
            ans.append([val * 100 for val in e[(report_type, title, 'all')]])
        elif title == 'financial-investments' or title == 'cash':
            ans.append(get_fin_indicators(e, report_type, title))
        else:
            ans.append([round(val, 2) for val in e[(report_type, title, 'all')]])

    return ans


@register.simple_tag()
def get_turnover_labels(e, report_type):
    return e.interesting_years(report_type)[1:]


@register.simple_tag()
def get_interest_to_ebitda(e, report_type):
    return round(e[(report_type, 'interest-payable/ebitda', 'LTM')], 2)