from django import template

from bond.models import *
from django.core.cache import cache
from bond.config import *
from bond.templatetags.report_tags import *
from bond.templatetags.score_tags import business_score, get_score
register = template.Library()


@register.simple_tag()
def get_short_beautiful_int(x, currency):
    smth = [f' {currency}', f' тыс. {currency}', f'm {currency}', f'b {currency}', f't {currency}']
    ind = 0
    while abs(x) > 1000:
        x /= 1000
        ind += 1
    x = round(x, 1)
    ans = str(x) + smth[ind]
    return ans


@register.simple_tag()
def get_credit_rating_text(e, report_type):
    x = get_credit_rating(e)
    ans = [[]]
    if x == -2:
        ans[0].append('danger')
        ans[0].append('Кредитный рейтинг:')
        ans[0].append(f'у компании отсутствует кредитный рейтинг.')
    elif x == -1:
        ans[0].append('danger')
        ans[0].append('Кредитный рейтинг:')
        ans[0].append(f'рейтинговые агентства оценивают кредитное качество компании как низкое.')
    elif x == 0:
        ans[0].append('warning')
        ans[0].append('Кредитный рейтинг:')
        ans[0].append(f'рейтинговые агентства оценивают кредитное качество компании как нормальное.')
    else:
        ans[0].append('success')
        ans[0].append('Кредитный рейтинг:')
        ans[0].append(f'рейтинговые агентства оценивают кредитное качество компании как высокое.')
    return ans


@register.simple_tag()
def get_income_revenue_text(e, report_type):
    unit, iunit = get_unit(e[(report_type, 'revenue', 'LTM')])
    revenue = get_fin_indicators(e, report_type, 'revenue', 10)
    net_income = get_fin_indicators(e, report_type, 'net-profit', 10)
    cur_revenue = revenue[-1]
    last_revenue = revenue[-2]
    if revenue[-1] == revenue[-2] and len(revenue) > 2:
        last_revenue = revenue[-3]
    cur_income = net_income[-1]
    last_income = net_income[-2]
    if net_income[-1] == net_income[-2] and len(net_income) > 2:
        last_income = net_income[-3]
    ans = [[], []]
    if cur_revenue >= last_revenue:
        percent = round((cur_revenue / last_revenue - 1) * 100, 1)
        ans[0].append('success')
        ans[0].append('Выручка выросла:')
        ans[0].append(f'за последние 12 месяцев выручка компании выросла на {percent}%')
    else:
        percent = round((1 - cur_revenue / last_revenue) * 100, 1)
        ans[0].append('danger')
        ans[0].append('Выручка упала:')
        ans[0].append(f'за последние 12 месяцев выручка компании сократилась на {percent}%')

    if cur_income > 0:
        if last_income < 0:
            ans[1].append('success')
            ans[1].append('Компания вышла в прибыль:')
            ans[1].append(f'компания показала прибыль в {cur_income} {unit} против убытка {last_income} {unit} годом ранее')
        else:
            if cur_income > last_income:
                percent = round((cur_income / last_income - 1) * 100, 1)
                ans[1].append('success')
                ans[1].append('Прибыль выросла:')
                ans[1].append(f'за последние 12 месяцев прибыль выросла на {percent}%')
            else:
                percent = round((1 - cur_income / last_income) * 100, 1)
                ans[1].append('danger')
                ans[1].append('Прибыль упала:')
                ans[1].append(f'за последние 12 месяцев прибыль упала на {percent}%')
    else:
        if last_income > 0:
            ans[1].append('danger')
            ans[1].append('Компания показала убыток:')
            ans[1].append(f'компания показала убыток {cur_income}{unit} против прибыли в {last_income}{unit} годом ранее')
        else:
            if cur_income > last_income:
                percent = round(abs(cur_income / last_income) * 100, 1)
                ans[1].append('success')
                ans[1].append('Компания сократила убыток:')
                ans[1].append(f'компания сократила убыток на {percent}% до {cur_income}{unit}')
            else:
                ans[1].append('danger')
                ans[1].append('Компания нарастила убытки:')
                ans[1].append(f'компания нарастила убыток до {cur_income}{unit}')
    return ans


@register.simple_tag()
def get_cagr_text(e, report_type, text_type=0):
    val1 = round(e[(report_type, 'cagr-3-revenue', 'LTM')], 1)
    val2 = round(e[(report_type, 'cagr-3-net-profit', 'LTM')], 1)
    val3 = round(e[(report_type, 'cagr-3-ebitda', 'LTM')], 1)
    if text_type == 0:
        ans = [[], []]
        if val1 < 0:
            ans[0].append('danger')
            ans[0].append('Выручка сокращается:')
            ans[0].append(f'за 3 года выручка в среднем сокращалась на {val1}%')
        elif val1 <= 9:
            ans[0].append('warning')
            ans[0].append('Низкие темпы роста выручки:')
            ans[0].append(f'за 3 года выручка в среднем росла на {val1}%')
        else:
            ans[0].append('success')
            ans[0].append('Высокие темпы роста выручки:')
            ans[0].append(f'за 3 года выручка в среднем росла на {val1}%')

        if val2 < 0:
            ans[1].append('danger')
            ans[1].append('Прибыль сокращается:')
            ans[1].append(f'за 3 года прибыль в среднем сокращалась на {val2}%')
        elif val2 <= 9:
            ans[1].append('warning')
            ans[1].append('Низкие темпы роста прибыли:')
            ans[1].append(f'за 3 года прибыль в среднем росла на {val2}%')
        else:
            ans[1].append('success')
            ans[1].append('Высокие темпы роста прибыли:')
            ans[1].append(f'за 3 года прибыль в среднем росла на {val2}%')
    else:

        ans = [[], [], []]
        nval1 = MedianValue.objects.get(report_type=report_type, title='cagr-3-revenue', sector=e.sector).value
        nval2 = MedianValue.objects.get(report_type=report_type, title='cagr-3-net-profit', sector=e.sector).value
        nval3 = MedianValue.objects.get(report_type=report_type, title='cagr-3-ebitda', sector=e.sector).value
        if val1 < 0:
            ans[0].append('danger')
            ans[0].append('Выручка сокращается:')
            ans[0].append(f'за 3 года выручка в среднем сокращалась на {val1}%')
        elif val1 < nval1 * 0.75:
            ans[0].append('danger')
            ans[0].append('Низкие темпы роста выручки:')
            ans[0].append(f'за 3 года выручка в среднем росла на {val1}%')
        elif val1 < nval1 * 1.25:
            ans[0].append('warning')
            ans[0].append('Средние темпы роста выручки:')
            ans[0].append(f'за 3 года выручка в среднем росла на {val1}%')
        else:
            ans[0].append('success')
            ans[0].append('Высокие темпы роста выручки:')
            ans[0].append(f'за 3 года выручка в среднем росла на {val1}%')

        if val2 < 0:
            ans[1].append('danger')
            ans[1].append('Прибыль сокращается:')
            ans[1].append(f'за 3 года прибыль в среднем сокращалась на {val2}%')
        elif val2 < nval2 * 0.75:
            ans[1].append('danger')
            ans[1].append('Низкие темпы роста прибыли:')
            ans[1].append(f'за 3 года прибыль в среднем росла на {val2}%')
        elif val2 < nval2 * 1.25:
            ans[1].append('warning')
            ans[1].append('Средние темпы роста прибыли:')
            ans[1].append(f'за 3 года прибыль в среднем росла на {val2}%')
        else:
            ans[1].append('success')
            ans[1].append('Высокие темпы роста прибыли:')
            ans[1].append(f'за 3 года прибыль в среднем росла на {val2}%')

        if val3 < 0:
            ans[2].append('danger')
            ans[2].append('EBITDA сокращается:')
            ans[2].append(f'за 3 года EBITDA в среднем сокращалась на {val3}%')
        elif val3 < nval3 * 0.75:
            ans[2].append('danger')
            ans[2].append('Низкие темпы роста EBITDA:')
            ans[2].append(f'за 3 года EBITDA в среднем росла на {val3}%')
        elif val3 < nval3 * 1.25:
            ans[2].append('warning')
            ans[2].append('Средние темпы роста EBITDA:')
            ans[2].append(f'за 3 года EBITDA в среднем росла на {val3}%')
        else:
            ans[2].append('success')
            ans[2].append('Высокие темпы роста EBITDA:')
            ans[2].append(f'за 3 года EBITDA в среднем росла на {val3}%')
    return ans


@register.simple_tag()
def get_turnover_text(e, report_type):
    val1 = round(e[(report_type, 'turnover-accounts-receivable', 'LTM')], 1)
    val2 = round(e[(report_type, 'turnover-inventories', 'LTM')], 1)
    val3 = round(e[(report_type, 'turnover-current-assets', 'LTM')], 1)

    nval1 = MedianValue.objects.get(report_type=report_type, title='turnover-accounts-receivable', sector=e.sector).value
    nval2 = MedianValue.objects.get(report_type=report_type, title='turnover-inventories', sector=e.sector).value
    nval3 = MedianValue.objects.get(report_type=report_type, title='turnover-current-assets', sector=e.sector).value
    ans = [[], [], []]
    titles = ['Дебиторская задолженность:', 'Запасы:', 'Оборотные активы:']
    titles2 = ['дебиторской задолженности', 'запасов', 'оборотных активов']
    val = [val1, val2, val3]
    nval = [nval1, nval2, nval3]
    for i in range(3):
        if val[i] > 1.25 * nval[i]:
            ans[i].append('danger')
            ans[i].append(titles[i])
            ans[i].append(f'оборачиваемость {titles2[i]} хуже среднеотраслевого уровня.')
        elif val[i] > 0.75 * nval[i]:
            ans[i].append('warning')
            ans[i].append(titles[i])
            ans[i].append(f'оборачиваемость {titles2[i]} находится на среднеотраслевом уровне.')
        else:
            ans[i].append('success')
            ans[i].append(titles[i])
            ans[i].append(f'оборачиваемость {titles2[i]} лучше среднеотраслевого уровня.')
    return ans


@register.simple_tag()
def get_margin_text(e, report_type, text_type=0):
    if text_type == 0:
        data = get_margin(e, report_type, 10)
        cur_net_margin = data[0][-1]
        cur_operation_margin = data[1][-1]
        nv = e.normal_values
        if nv is None:
            nv = NormalValues.objects.get(id=29)
        ans = [[], []]

        if cur_net_margin >= nv.net_margin1:
            ans[0].append('success')
            ans[0].append('Чистая маржинальность:')
            ans[0].append(f'чистая маржинальность находится на высоком уровне {round(cur_net_margin, 1)}%')
        elif cur_net_margin >= nv.net_margin2:
            ans[0].append('warning')
            ans[0].append('Чистая маржинальность:')
            ans[0].append(f'чистая маржинальность находится на среднем уровне {round(cur_net_margin, 1)}%')
        else:
            ans[0].append('danger')
            ans[0].append('Чистая маржинальность:')
            ans[0].append(f'чистая маржинальность находится на низком уровне {round(cur_net_margin, 1)}%')

        if cur_operation_margin >= nv.operation_margin1:
            ans[1].append('success')
            ans[1].append('Операционная маржинальность:')
            ans[1].append(f'операционная маржинальность находится на высоком уровне {round(cur_operation_margin, 1)}%')
        elif cur_operation_margin >= nv.operation_margin2:
            ans[1].append('warning')
            ans[1].append('Операционная маржинальность:')
            ans[1].append(f'операционная маржинальность находится на среднем уровне {round(cur_operation_margin, 1)}%')
        else:
            ans[1].append('danger')
            ans[1].append('Операционная маржинальность:')
            ans[1].append(f'операционная маржинальность находится на низком уровне {round(cur_operation_margin, 1)}%')

        return ans
    else:
        val = [e[(report_type, 'net-profit/revenue', 'LTM')], e[(report_type, 'ebitda/revenue', 'LTM')],
               e[(report_type, 'OCF/revenue', 'LTM')]]
        nval = [MedianValue.objects.get(report_type=report_type, sector=e.sector, title='net-profit/revenue').value,
                MedianValue.objects.get(report_type=report_type, sector=e.sector, title='ebitda/revenue').value,
                MedianValue.objects.get(report_type=report_type, sector=e.sector, title='OCF/revenue').value,]
        ans = [[], [], []]
        titles1 = ['Чистая маржинальность:', 'Маржинальность по EBITDA:', 'Маржинальность по OCF:']
        titles2 = ['чистая маржинальность', 'маржинальность по EBITDA', 'маржинальность по OCF']
        for i in range(3):
            c1 = 1.25
            c2 = 0.75
            if nval[i] < 0:
                c1, c2 = c2, c1
            if val[i] > c1 * nval[i]:
                ans[i].append('success')
                ans[i].append(titles1[i])
                ans[i].append(f'{titles2[i]} находится на высоком уровне {round(val[i]*100, 1)}%')
            elif val[i] > c2 * nval[i]:
                ans[i].append('warning')
                ans[i].append(titles1[i])
                ans[i].append(f'{titles2[i]} находится на среднем уровне {round(val[i]*100, 1)}%')
            else:
                ans[i].append('danger')
                ans[i].append(titles1[i])
                ans[i].append(f'{titles2[i]} находится на низком уровне {round(val[i]*100, 1)}%')
        return ans


@register.simple_tag()
def get_margin_growth_text(e, report_type):
    data = get_margin(e, report_type, 10)
    cur_net_margin = data[0][-1]
    prev_net_margin = data[0][-2]
    if cur_net_margin == prev_net_margin:
        prev_net_margin = data[0][-3]

    cur_operation_margin = data[1][-1]
    prev_operation_margin = data[1][-2]
    if cur_operation_margin == prev_operation_margin:
        prev_operation_margin = data[1][-3]

    ans = [[], []]
    if cur_net_margin >= prev_net_margin:
        ans[0].append('success')
        ans[0].append('Маржинальность по чистой прибыли выросла:')
        ans[0].append(f'за последние 12 месяцев маржинальность по чистой прибыли выросла на {round(cur_net_margin - prev_net_margin, 1)} п.')
    else:
        ans[0].append('danger')
        ans[0].append('Маржинальность по чистой прибыли упала:')
        ans[0].append(f'за последние 12 месяцев маржинальность по чистой прибыли упала на {round(cur_net_margin - prev_net_margin, 1)} п.')

    if cur_operation_margin >= prev_operation_margin:
        ans[1].append('success')
        ans[1].append('Маржинальность по операцинной прибыли выросла:')
        ans[1].append(f'за последние 12 месяцев маржинальность по операцинной прибыли выросла на {round(cur_operation_margin - prev_operation_margin, 1)} п.')
    else:
        ans[1].append('danger')
        ans[1].append('Маржинальность упала по операцинной прибыли:')
        ans[1].append(f'за последние 12 месяцев  маржинальность по операцинной прибыли упала на {round(cur_operation_margin - prev_operation_margin, 1)} п.')

    return ans


@register.simple_tag()
def get_profitability_text(e, report_type):
    data = get_profitability(e, report_type, 10)
    nv = e.normal_values
    if nv is None:
        nv = NormalValues.objects.get(id=29)
    cur_roa = data[0][-1]
    cur_roe = data[1][-1]
    ans = [[], []]

    if cur_roa >= nv.roa1:
        ans[0].append('success')
        ans[0].append('Рентабельность активов:')
        ans[0].append(f'рентабельность активов находится на высоком уровне {round(cur_roa, 1)}%')
    elif cur_roa >= nv.roa2:
        ans[0].append('warning')
        ans[0].append('Рентабельность активов:')
        ans[0].append(f'рентабельность активов находится на среднем уровне {round(cur_roa, 1)}%')
    else:
        ans[0].append('danger')
        ans[0].append('Рентабельность активов:')
        ans[0].append(f'рентабельность активов находится на низком уровне {round(cur_roa, 1)}%')

    if cur_roe >= nv.roe1:
        ans[1].append('success')
        ans[1].append('Рентабельность капитала:')
        ans[1].append(f'рентабельность капитала находится на высоком уровне {round(cur_roe, 1)}%')
    elif cur_roe >= nv.roe2:
        ans[1].append('warning')
        ans[1].append('Рентабельность капитала:')
        ans[1].append(f'рентабельность капитала находится на среднем уровне {round(cur_roe, 1)}%')
    else:
        ans[1].append('danger')
        ans[1].append('Рентабельность капитала:')
        ans[1].append(f'рентабельность капитала находится на низком уровне {round(cur_roe, 1)}%')

    return ans


@register.simple_tag()
def get_profitability_growth_text(e, report_type):
    data = get_profitability(e, report_type, 10)
    cur_roa = data[0][-1]
    prev_roa = data[0][-2]
    if cur_roa == prev_roa:
        prev_roa = data[0][-3]

    cur_roe = data[1][-1]
    prev_roe = data[1][-2]
    if cur_roe == prev_roe:
        prev_roe = data[1][-3]

    ans = [[], []]
    if cur_roa >= prev_roa:
        ans[0].append('success')
        ans[0].append('Рентабельность активов выросла:')
        ans[0].append(f'за последние 12 месяцев рентабельность активов выросла на {round(cur_roa - prev_roa, 1)} п.')
    else:
        ans[0].append('danger')
        ans[0].append('Рентабельность активов упала:')
        ans[0].append(f'за последние 12 месяцев рентабельность активов упала на {round(cur_roa - prev_roa, 1)} п.')

    if cur_roe >= prev_roe:
        ans[1].append('success')
        ans[1].append('Рентабельность капитала выросла:')
        ans[1].append(f'за последние 12 месяцев рентабельность капитала выросла на {round(cur_roe - prev_roe, 1)} п.')
    else:
        ans[1].append('danger')
        ans[1].append('Рентабельность капитала упала:')
        ans[1].append(f'за последние 12 месяцев рентабельность капитала упала на {round(cur_roe - prev_roe, 1)} п.')

    return ans


@register.simple_tag()
def get_debt_ebitda_text(e, report_type):
    nv = e.normal_values
    if nv is None:
        nv = NormalValues.objects.get(id=29)

    net_debt = get_fin_indicators(e, report_type, 'net_debt', 2)
    ebitda = get_fin_indicators(e, report_type, 'ebitda', 2)
    cur_nd_ebitda = round(net_debt[-1] / ebitda[-1], 1)
    if len(net_debt) >= 4 and ebitda[-4] != 0:
        prev_nd_ebitda = round(net_debt[-4] / ebitda[-4], 1)
        start = 'за поседние 3 года Чистый долг/EBITDA '
    else:
        prev_nd_ebitda = round(net_debt[-2] / ebitda[-2], 1)
        start = 'за поседние 12 месяцев Чистый долг/EBITDA '
    ans = [[]]

    if cur_nd_ebitda <= prev_nd_ebitda:
        if cur_nd_ebitda <= nv.nd_to_ebitda2:
            ans[0].append('success')
        else:
            ans[0].append('warning')
        ans[0].append('Динамика долговой нагрузки:')
        ans[0].append(start + f'уменьшился с {prev_nd_ebitda} до {cur_nd_ebitda}')
    else:
        if cur_nd_ebitda <= nv.nd_to_ebitda1:
            ans[0].append('warning')
        else:
            ans[0].append('danger')
        ans[0].append('Динамика долговой нагрузки:')
        ans[0].append(start + f'увеличился с {prev_nd_ebitda} до {cur_nd_ebitda}')
    return ans


@register.simple_tag()
def get_assets_liabilities_text(e, report_type):
    data = get_assets_and_liabilities(e, report_type)
    unit, iunit = get_unit(e[(report_type, 'revenue', 'LTM')])

    assets = data[0]
    liabilities = data[1]
    ans = [[], []]

    if assets[0] < liabilities[0]:
        ans[0].append('danger')
        ans[0].append('Краткосрочные обязательства:')
        ans[0].append(f'краткосрочные обязательства {liabilities[0]}{unit} превышают краткосрочные активы {assets[0]}{unit}')
    else:
        ans[0].append('success')
        ans[0].append('Краткосрочные обязательства:')
        ans[0].append(f'краткосрочные активы {assets[0]}{unit} превышают краткосрочные обязательства {liabilities[0]}{unit}')

    if assets[1] < liabilities[1]:
        ans[1].append('danger')
        ans[1].append('Долгосрочные обязательства:')
        ans[1].append(f'долгосрочные обязательства {liabilities[1]}{unit} превышают долгосрочные активы {assets[1]}{unit}')
    else:
        ans[1].append('success')
        ans[1].append('Долгосрочные обязательства:')
        ans[1].append(f'долгосрочные активы {assets[1]}{unit} превышают долгосрочные обязательства {liabilities[1]}{unit}')

    return ans


@register.simple_tag()
def get_debt_level_text(e, report_type, text_type=0):
    if text_type == 0:
        data = get_net_debt_ebitda(e, report_type)
        nd_to_ebitda = data[0]
        ans = [[], []]

        nv = e.normal_values
        if nv is None:
            nv = NormalValues.objects.get(id=29)
        flag = 0
        if e.sector.title == 'Фин.сервис - Лизинг':
            equity_level = get_leasing_debt_data(e, report_type)[1]
            if equity_level >= nv.equity_level1:
                flag = 0
            elif equity_level >= nv.equity_level2:
                flag = 1
            else:
                flag = 2
        else:
            if nd_to_ebitda <= nv.nd_to_ebitda1:
                flag = 0
            elif nd_to_ebitda <= nv.nd_to_ebitda2:
                flag = 1
            else:
                flag = 2
        if flag == 0:
            ans[0].append('success')
            ans[0].append('Уровень долга:')
            ans[0].append('долговая нагрузка эмитента находится на низком уровне.')
        elif flag == 1:
            ans[0].append('warning')
            ans[0].append('Уровень долга:')
            ans[0].append('долговая нагрузка эмитента находится на умеренном уровне.')
        else:
            ans[0].append('danger')
            ans[0].append('Уровень долга:')
            ans[0].append('долговая нагрузка эмитента находится на высоком уровне и значительно выходит за границы нормы.')

        return ans
    else:
        val = [e[(report_type, 'net_debt/ebitda', 'LTM')], e[(report_type, 'interest-payable/ebitda', 'LTM')]]
        nval = [MedianValue.objects.get(report_type=report_type, sector=e.sector, title='net_debt/ebitda').value,
                MedianValue.objects.get(report_type=report_type, sector=e.sector, title='interest-payable/ebitda').value]
        ans = [[], []]
        titles1 = ['Уровень долга:', 'Процентная нагрузка:']
        titles2 = ['долговая нагрузка', 'процентная нагрузка']
        for i in range(2):
            if val[i] < 0.75 * nval[i]:
                ans[i].append('success')
                ans[i].append(titles1[i])
                ans[i].append(f'{titles2[i]} находится на низком уровне.')
            elif val[i] < 1.25 * nval[i]:
                ans[i].append('warning')
                ans[i].append(titles1[i])
                ans[i].append(f'{titles2[i]} находится на среднем уровне.')
            else:
                ans[i].append('danger')
                ans[i].append(titles1[i])
                ans[i].append(f'{titles2[i]} находится на высоком уровне.')
        return ans


@register.simple_tag()
def get_liquidity_text(e, report_type):
    data = get_liquidity(e, report_type)
    nv = e.normal_values

    cur_liquidity = round((data[1] / data[0]) * 100, 1)
    fast_liquidity = round((data[2] / data[0]) * 100, 1)
    absolute_liquidity = round((data[3] / data[0]) * 100, 1)

    ans = [[], [], []]
    if nv is None:
        nv = NormalValues.objects.get(id=29)
    if cur_liquidity < nv.cur_liquidity2 * 100:
        ans[0].append('danger')
        ans[0].append('Текущая ликвидность:')
        ans[0].append(f'коэффициент текущей ликвидности {cur_liquidity}% ниже критического уровня в {round(nv.cur_liquidity2*100, 1)}%')
    elif cur_liquidity < nv.cur_liquidity1 * 100:
        ans[0].append('warning')
        ans[0].append('Текущая ликвидность:')
        ans[0].append(
            f'коэффициент текущей ликвидности {cur_liquidity}% ниже нормального значения в {round(nv.cur_liquidity1 * 100, 1)}%')
    else:
        ans[0].append('success')
        ans[0].append('Текущая ликвидность:')
        ans[0].append(f'коэффициент текущей ликвидности {cur_liquidity}% выше нормы в {round(nv.cur_liquidity1 * 100, 1)}%')

    if fast_liquidity < nv.fast_liquidity2 * 100:
        ans[1].append('danger')
        ans[1].append('Быстрая ликвидность:')
        ans[1].append(f'коэффициент быстрой ликвидности {fast_liquidity}% ниже критического уровня в {round(nv.fast_liquidity2*100, 1)}%')
    elif fast_liquidity < nv.fast_liquidity1 * 100:
        ans[1].append('warning')
        ans[1].append('Быстрая ликвидность:')
        ans[1].append(f'коэффициент быстрой ликвидности {fast_liquidity}% ниже нормы в {round(nv.fast_liquidity1*100, 1)}%')
    else:
        ans[1].append('success')
        ans[1].append('Быстрая ликвидность:')
        ans[1].append(f'коэффициент быстрой ликвидности {fast_liquidity}% выше нормы в {round(nv.fast_liquidity2*100, 1)}%')

    if absolute_liquidity < nv.absolute_liquidity2 * 100:
        ans[2].append('danger')
        ans[2].append('Абсолютная ликвидность:')
        ans[2].append(f'коэффициент абсолютной ликвидности {absolute_liquidity}% ниже критического уровня в {round(nv.absolute_liquidity2*100, 1)}%')
    elif absolute_liquidity < nv.absolute_liquidity1 * 100:
        ans[2].append('warning')
        ans[2].append('Абсолютная ликвидность:')
        ans[2].append(f'коэффициент абсолютной ликвидности {absolute_liquidity}% ниже нормы в {round(nv.absolute_liquidity1*100, 1)}%')
    else:
        ans[2].append('success')
        ans[2].append('Абсолютная ликвидность:')
        ans[2].append(f'коэффициент абсолютной ликвидности {absolute_liquidity}% выше нормы в {round(nv.absolute_liquidity2*100, 1)}%')
    return ans


@register.simple_tag()
def get_tooltip_text(title):

    if title == 0:
        return 'Срок облигации равен количеству дней до ближайшей оферты или погашения'
    elif title == 1:
        return 'Доходность в процентах годовых отражает доходность с учетом цены, НКД, купонов, оферт и амортизационных' \
               ' выплат'
    elif title == 2:
        return 'Купон равен сумме всех купонных выплат за год'
    elif title == 3:
        return 'Цена в процентнах от текущего номинала облигации'
    elif title == 4:
        return 'Кредитный рейтинг оценивает надежность заёмщика'
    elif title == 5:
        return 'Ликвидность равна объему сделок по облигации за 1 рабочий день в млн. руб'
    elif title == 6:
        return 'Доступна только квалифицированным инвесторам'
    return '555'


@register.simple_tag()
def get_small_comments(e, report_type):
    ans = []
    b_scores = business_score(e, report_type, 2)
    if b_scores[1] != 100:
        val = e[(report_type, 'financial-investments', 'LTM')]
        if val > 10 ** 6:
            ans.append(['danger', f'На балансе присутствуют финансовые вложения в {get_short_beautiful_int(val, "₽")}'])

    if b_scores[1] < 50:
        val = e[(report_type, 'ebitda', 'LTM')]
        ans.append(['danger', f'Малый размер бизнеса. EBITDA: {get_short_beautiful_int(val, "₽")}'])
    elif b_scores[1] == 75:
        val = e[(report_type, 'ebitda', 'LTM')]
        ans.append(['success', f'Размер бизнеса выше среднего. EBITDA: {get_short_beautiful_int(val, "₽")}'])
    elif b_scores[1] == 100:
        val = e[(report_type, 'ebitda', 'LTM')]
        ans.append(['success', f'Очень крупный размер бизнеса. EBITDA: {get_short_beautiful_int(val, "₽")}'])

    if e.sector.risk_level > 3:
        ans.append(['danger', f'Высокие отраслевые риски.'])
    elif e.sector.risk_level < 3:
        ans.append(['success', f'Низкие отраслевые риски.'])

    val1 = e[(report_type, 'ebitda/revenue', 'LTM')]
    val2 = MedianValue.objects.get(report_type=report_type, sector=e.sector, title='ebitda/revenue').value
    if val1 > val2:
        ans.append(['success', 'Маржинальность выше среднеотралевых уровней.'])
    elif val1 < 0.5 * val2:
        ans.append(['danger', f'Маржинальность ниже среднеотралевой на {100-round(val1 / val2 * 100)}%'])
    elif val1 < 0.8 * val2:
        ans.append(['danger', 'Маржинальность ниже среднеотралевых уровней.'])

    val = e[(report_type, 'OCF/revenue', 'LTM')]
    if val < 0:
        ans.append(['danger', 'Отрицательный операционный денежный поток.'])
    elif val > 0:
        ans.append(['success', 'Положительный операционный денежный поток.'])

    val1 = e[(report_type, 'net_debt/ebitda', 'LTM')]
    val2 = MedianValue.objects.get(report_type=report_type, sector=e.sector, title='net_debt/ebitda').value
    if val1 < 0.5 * val2:
        ans.append(['success', 'Очень низкая долговая нагрузка.'])
    elif val1 < val2:
        ans.append(['success', 'Низкая долговая нагрузка.'])
    elif val1 > val2 * 1.5:
        ans.append(['danger', 'Высокая долговая нагрузка.'])
    elif val1 > val2 * 2:
        ans.append(['danger', 'Критическая долговая нагрузка.'])

    titles = ['current-assets/short-liabilities', 'fast_liquidity/short-liabilities', 'cash/short-liabilities',
              'OCF/short-liabilities', 'operating-working-capital/assets']
    liquidity_score = get_score(e, report_type, titles=titles)
    if liquidity_score < 40:
        ans.append(['danger', 'Слабая позиция по ликвидности.'])
    elif liquidity_score > 60:
        ans.append(['success', 'Сильная позиция по ликвидности.'])

    titles = ['cagr-3-revenue', 'cagr-3-net-profit', 'cagr-3-ebitda', 'CAPEX/ebitda']
    growth_score = get_score(e, report_type, titles=titles)
    if growth_score < 40:
        ans.append(['danger', 'Низкие темпы роста бизнеса.'])
    elif growth_score > 60:
        ans.append(['success', 'Высокие темпы роста бизнеса.'])
    ans.sort()
    return ans
