import telebot
from .models import *
import matplotlib
from .emitter import check_report_exists
import matplotlib.pyplot as plt
import numpy as np
import os
import shutil
from scipy import interpolate
token = '5339884342:AAF-gXeLq_nDYz9LF2VApPT01DTrE1hJUPI'
bot = telebot.TeleBot(token)
chat_id = '420921755'
#chat_id = '845661032' //Витя


def hello_world():
    text = 'Hello python'
    bot.send_message(chat_id, text)


def get_beautiful_int(x):
    smth = [' руб', ' тыс. руб', ' млн. руб', ' млрд. руб', ' трлн. руб']
    ind = 0
    while abs(x) > 1000:
        x /= 1000
        ind += 1
    x = round(x, 1)
    ans = str(x) + smth[ind]
    return ans


def get_unit(x):
    smth1 = [' руб', ' тыс. руб', ' млн. руб', ' млрд. руб', ' трлн. руб']
    smth2 = [1, 1000, 1000000, 1000000000, 1000000000000]
    ind = 0
    while abs(x) > 1000:
        x /= 1000
        ind += 1
    return smth1[ind], smth2[ind]


def delta(x1, x2):
    if x1 > x2:
        x = x1 / x2 - 1
        x *= 100
        x = int(x)
        return '+' + str(x) + '%'
    else:
        if x2 == 0:
            x2 = 0.01
        x = (x2 - x1) / x2
        x *= 100
        x = int(x)
        return '-' + str(x) + '%'


def get_percent(x):
    x *= 100
    x = int(x)
    return str(x) + '%'


def make_picture_revenue(e, report_type='rsbu'):
    can = ['2017', '2018', '2019', '2020', '2021', 'LTM']
    g1 = []
    g2 = []
    cat_par = []
    unit, iunit = get_unit(e.fin_data[report_type]['revenue']['LTM'])
    if report_type == 'ifrs':
        can.pop(0)
    for year in can:
        if e.fin_data[report_type]['revenue'][year] != 0:
            cat_par.append(year)
            g1.append(e.fin_data[report_type]['revenue'][year] / iunit)
            g2.append(e.fin_data[report_type]['net-profit'][year] / iunit)
    width = 0.45
    x = np.arange(len(cat_par))
    fig, ax = plt.subplots()
    ax.grid(alpha=0.3)
    rects1 = ax.bar(x - width / 2, g1, width, alpha=1, color='#6B8E23', edgecolor='#FFFFFF', linewidth=2,
                    label='выручка')
    rects2 = ax.bar(x + width / 2, g2, width, alpha=1, color="#9ACD32", edgecolor='#FFFFFF', linewidth=2,
                    label='прибыль')
    ax.set_title('Выручка и прибыль')
    ax.set_xticks(x)
    ax.set_xticklabels(cat_par)
    plt.ylabel(unit)
    ax.legend()
    fig.savefig(f'{e.moex_id}/выручка и прибыль.png')
    plt.clf()
    plt.cla()


def make_picture_assets(e, report_type='rsbu'):
    cat_par = ['краткосрочные', 'долгосрочные']
    unit, iunit = get_unit(e.fin_data[report_type]['non-current-assets']['LTM'])
    g1 = [e.fin_data[report_type]['current-assets']['LTM'] / iunit, e.fin_data[report_type]['non-current-assets']['LTM'] / iunit]
    g2 = [e.fin_data[report_type]['short-liabilities']['LTM'] / iunit, e.fin_data[report_type]['long-liabilities']['LTM'] / iunit]
    width = 0.45
    x = np.arange(len(cat_par))
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, g1, width, alpha=1, color='#6B8E23', edgecolor='#FFFFFF', linewidth=2,
                    label='активы')
    rects2 = ax.bar(x + width / 2, g2, width, alpha=1, color="#9ACD32", edgecolor='#FFFFFF', linewidth=2,
                    label='обязательства')
    ax.set_title('Активы и обязательства')
    ax.set_xticks(x)
    ax.set_xticklabels(cat_par)
    plt.ylabel(unit)
    ax.legend()
    fig.savefig(f'{e.moex_id}/Активы и обязательства.png')
    plt.clf()
    plt.cla()


def make_picture_equity(e, report_type='rsbu'):
    can = [2017, 2018, 2019, 2020, 2021, 2022]
    if report_type == 'ifrs':
        can.pop(0)
    x = []
    y1 = []
    y2 = []
    unit, iunit = get_unit(e.fin_data[report_type]['equity']['LTM'])
    for i in can:
        if i != 2022:
            year = str(i)
        else:
            year = 'LTM'
        if e.fin_data[report_type]['assets'][year] != 0:
            y1.append(e.fin_data[report_type]['equity'][year] / iunit)
            y2.append((e.fin_data[report_type]['long-debt'][year] + e.fin_data[report_type]['short-debt'][year]) / iunit)
            x.append(i)

    xnew = np.linspace(int(x[0]), 2022, 100)

    bspline1 = interpolate.make_interp_spline(x, y1)
    y_smoothed1 = bspline1(xnew)
    plt.plot(xnew, y_smoothed1, '-g', label='Собственный капитал', alpha=0.7)
    bspline2 = interpolate.make_interp_spline(x, y2)
    y_smoothed2 = bspline2(xnew)
    plt.plot(xnew, y_smoothed2, '-r', label='Долг', alpha=0.7)
    plt.legend()
    plt.ylabel(unit)
    plt.savefig(f'{e.moex_id}/Долг и капитал.png')
    plt.clf()
    plt.cla()


def make_picture_ebitda(e, report_type='rsbu'):
    labels = ['Прибыль', 'Налоги', 'Амортизация', 'Проценты к уплате']
    unit, iunit = get_unit(e.fin_data[report_type]['equity']['LTM'])
    values = [e.fin_data[report_type]['net-profit']['LTM'], e.fin_data[report_type]['ebit']['LTM'] - e.fin_data[report_type]['net-profit']['LTM'],
              e.fin_data[report_type]['amortization']['LTM'], e.fin_data[report_type]['interest-payable']['LTM']]
    for i in range(len(values)):
        if values[i] < 0:
            values[i] = 0
    fig1, ax1 = plt.subplots()
    ax1.pie(values, labels=labels, autopct='%1.1f%%', wedgeprops=dict(width=0.55),
            colors=['#9ACD32', '#00FA9A', '#3CB371', '#2E8B57'], )
    ax1.set_title('Cтруктура EBITDA')
    fig1.savefig(f'{e.moex_id}/Структура EBITDA.png')
    plt.clf()
    plt.cla()


def send_pictures(chat_id, e, report_type='rsbu'):

    os.mkdir(f'{e.moex_id}')
    #make_picture_equity(e, report_type)
    make_picture_revenue(e, report_type)
    make_picture_ebitda(e, report_type)
    make_picture_assets(e, report_type)
    bot.send_media_group(chat_id, [telebot.types.InputMediaPhoto(open(f'{e.moex_id}/выручка и прибыль.png', 'rb')),
                                   telebot.types.InputMediaPhoto(open(f'{e.moex_id}/Активы и обязательства.png', 'rb')),
                                   #telebot.types.InputMediaPhoto(open(f'{e.moex_id}/Долг и капитал.png', 'rb')),
                                   telebot.types.InputMediaPhoto(open(f'{e.moex_id}/Структура EBITDA.png', 'rb')),
                                   ])
    shutil.rmtree(f'{e.moex_id}')


def get_emoji(x, l, r):
    if l <= x <= r:
        return '✅'
    elif x <= l:
        if l == 0:
            return '❓'
        elif x / l >= 0.75:
            return '⚠️'
        else:
            return '❌'
    else:
        if x / r <= 1.25:
            return '⚠️'
        else:
            return '❌'


def get_analysis(e_id, last='2021', report_type='rsbu'):
    e = Emitter.objects.get(moex_id=e_id)
    ans = ''
    ans += f'*Анализ эмитента {e.title}:*\n\n'
    ans += '----------------\n'
    ans += f'🔍*Об эмитенте*:\n----------------\n\n{e.description}\n'
    ans += f'*Руководитель*: {e.ceo}\n'
    ans += f'*Сайт компании*: {e.website1}\n\n'
    if e.is_system_important:
        ans += '*Компания является системообразующим предприятием*\n\n'
    ans += '----------------\n'
    ans += f'🔍*Выпуски эмитента:*\n'
    ans += '----------------\n\n'
    bonds = Bond.objects.filter(moex_id=e_id)
    for b in bonds:
        ans += f'    ${b.isin}\n'
    ans += '\n'
    ans += '----------------\n'
    ans += '🔍*Кредитные рейтинги:*\n'
    ans += '----------------\n\n'
    if e.akra is not None: ans += f'Агентство АКРА:* {e.akra}*\n'
    if e.fitch is not None: ans += f'Агентство FITCH:* {e.fitch}*\n'
    if e.ra_expert is not None: ans += f'Агентство Эксперт РА:* {e.ra_expert}*\n'
    if e.sp is not None: ans += f'Агентство S&P:* {e.sp}*\n'
    if e.moodys is not None: ans += f'Агентство Moodys:* {e.moodys}*\n'
    if e.akra is None and e.fitch is None and e.ra_expert is None and e.sp is None and e.moodys is None:
        ans += f'Отсутствуют...\n'
    ans += '\n'

    ans += '----------------\n\n'
    if report_type == 'rsbu':
        ans += 'Данные представлены за последние 12 месяцев по отчетности РСБУ(последний отчет за 2022)\n\n'
    else:
        ans += 'Данные представлены за последние 12 месяцев по отчетности МСФО(последний отчет за 2022)\n\n'
    ans += '🔍*Выручка и прибыль*:\n'
    ans += '----------------\n\n'
    revenueLTM = e[(report_type, 'revenue', 'LTM')]
    revenue2020 = e[(report_type, 'revenue', last)]
    operationLTM = e[(report_type, 'operation-profit', 'LTM')]
    operation2020 = e[(report_type, 'operation-profit', last)]
    ebitLTM = e[(report_type, 'ebt', 'LTM')]
    ebit2020 = e[(report_type, 'ebt', last)]
    ebitdaLTM = ebitLTM + e[(report_type, 'interest-payable', 'LTM')] - e[(report_type, 'interest-receivable', 'LTM')] + e[(report_type, 'amortization', 'LTM')]
    ebitda2020 = ebit2020 + e[(report_type, 'interest-payable', last)] - e[(report_type, 'interest-receivable', last)] + e[(report_type, 'amortization', last)]
    incomeLTM = e[(report_type, 'net-profit', 'LTM')]
    income2020 = e[(report_type, 'net-profit', last)]
    assetsLTM = e[(report_type, 'assets', 'LTM')]
    assets2020 = e[(report_type, 'assets', last)]
    equityLTM = e[(report_type, 'equity', 'LTM')]
    equity2020 = e[(report_type, 'equity', last)]
    liabilitiesLTM = e[(report_type, 'long-liabilities', 'LTM')] + e[(report_type, 'short-liabilities', 'LTM')]
    liabilities2020 = e[(report_type, 'long-liabilities', last)] + e[(report_type, 'short-liabilities', last)]

    ans += f'*Выручка:* {get_beautiful_int(revenueLTM)} ({delta(revenueLTM, revenue2020)})\n'
    ans += f'*Операционная прибыль:* {get_beautiful_int(operationLTM)} ({delta(operationLTM, operation2020)})\n'
    ans += f'*EBITDA:* {get_beautiful_int(ebitdaLTM)} ({delta(ebitdaLTM, ebitda2020)})\n'
    ans += f'*Прибыль до налогов:* {get_beautiful_int(ebitLTM)} ({delta(ebitLTM, ebit2020)})\n'
    ans += f'*Чистая прибыль:* {get_beautiful_int(incomeLTM)} ({delta(incomeLTM, income2020)})\n'
    ans += '\n'

    if e.sector.title == 'Фин.сервис - Лизинг':
        ans += f'{get_emoji(incomeLTM / equityLTM, 0.14, 100)}*Рентабельность капитала:* {get_percent(incomeLTM / equityLTM)}' \
               f'\n\n'
        ans += f'{get_emoji(incomeLTM / assetsLTM, 0.03, 100)}*Рентабельность активов:* {get_percent(incomeLTM / assetsLTM)}\n\n'

    ans += '----------------\n'
    ans += f'🔍*Финансовое здоровье:*\n'
    ans += '----------------\n\n'
    ans += f'*Активы:* {get_beautiful_int(assetsLTM)} ({delta(assetsLTM, assets2020)})\n'
    ans += f'*Собственный капитал:* {get_beautiful_int(equityLTM)} ({delta(equityLTM, equity2020)})\n'
    ans += f'*Обязательства:* {get_beautiful_int(liabilitiesLTM)} ({delta(liabilitiesLTM, liabilities2020)})\n'

    short_assetsLTM = e[(report_type, 'current-assets', 'LTM')]
    long_assetsLTM = e[(report_type, 'non-current-assets', 'LTM')]
    short_liabilitiesLTM = e[(report_type, 'short-liabilities', 'LTM')]
    long_liabilitiesLTM = e[(report_type, 'long-liabilities', 'LTM')]
    netdebtLTM = e[(report_type, 'long-debt', 'LTM')] + e[(report_type, 'short-debt', 'LTM')]
    netdebt2020 = e[(report_type, 'long-debt', last)] + e[(report_type, 'short-debt', last)]
    debtLTM = netdebtLTM
    debt2020 = e[(report_type, 'long-debt', last)] + e[(report_type, 'short-debt', last)]
    netdebtLTM -= (e[(report_type, 'cash', 'LTM')] + e[(report_type, 'escrow', 'LTM')])
    netdebt2020 -= (e[(report_type, 'cash', last)] + e[(report_type, 'escrow', last)])
    ans += f'*Долг:* {get_beautiful_int(debtLTM)} ({delta(debtLTM, debt2020)})\n'
    ans += f'*Чистый долг:* {get_beautiful_int(netdebtLTM)} ({delta(netdebtLTM, netdebt2020)})\n'
    ans += '\n'
    if e.sector.title == 'Фин.сервис - Лизинг':
        ans += f'{get_emoji(long_assetsLTM / long_liabilitiesLTM, 0.05, 100000)}' \
               f'*Внеоборотные активы/долгосрочные обязательства:* {get_percent(long_assetsLTM / long_liabilitiesLTM)} (норма >5%)\n\n'
        ans += f'{get_emoji(netdebtLTM / ebitdaLTM, 0, 5.5)}' \
               f'*Чистый долг/EBITDA:* {get_percent(netdebtLTM / ebitdaLTM)} (норма <550%)\n\n'
        ans += f'{get_emoji(assetsLTM / debtLTM, 1.2, 1.8)}' \
               f'*Коэффициент покрытия долга:* {get_percent(assetsLTM / debtLTM)} (норма 120-180%)\n\n'
        ans += f'{get_emoji(equityLTM / assetsLTM, 0.08, 1)}' \
               f'*Коэффициент уровня собственного капитала:* {get_percent(equityLTM / assetsLTM)} (норма >8%)\n\n'
    else:
        ans += f'{get_emoji(long_assetsLTM / long_liabilitiesLTM, 1, 100000)}' \
               f'*Внеоборотные активы/долгосрочные обязательства:* {get_percent(long_assetsLTM / long_liabilitiesLTM)} (норма >100%)\n\n'
        ans += f'{get_emoji(netdebtLTM / assetsLTM, 0, 0.6)}' \
               f'*Чистый долг/активы:* {get_percent(netdebtLTM / assetsLTM)} (норма <60%)\n\n'
        ans += f'{get_emoji(netdebtLTM / equityLTM, 0, 1)}' \
               f'*Чистый долг/собственный капитал:* {get_percent(netdebtLTM / equityLTM)} (норма <100%)\n\n'
        ans += f'{get_emoji(netdebtLTM / ebitdaLTM, 0, 3)}' \
               f'*Чистый долг/EBITDA:* {get_percent(netdebtLTM / ebitdaLTM)} (норма <300%)\n\n'

    debitorkaLTM = e[(report_type, 'accounts-receivable', 'LTM')]
    cashLTM = e[(report_type, 'cash', 'LTM')]
    debtpayLTM = e[(report_type, 'interest-payable', 'LTM')]
    ans += '----------------\n'
    ans += f'🔍*Обслуживание текущих обязательств:*\n'
    ans += '----------------\n\n'
    ans += f'{get_emoji(short_assetsLTM / short_liabilitiesLTM, 1.5, 100000)}' \
           f'*Коэффициент текущей ликвидности:* {get_percent(short_assetsLTM / short_liabilitiesLTM)} (норма >150%)\n\n'
    ans += f'{get_emoji(cashLTM / short_liabilitiesLTM, 0.2, 100000)}' \
           f'*Коэффициент абсолютной ликвидности:* {get_percent(cashLTM / short_liabilitiesLTM)} (норма >20%)\n\n'
    ans += f'{get_emoji((cashLTM + debitorkaLTM) / short_liabilitiesLTM, 1.0, 100000)}' \
           f'*Коэффициент быстрой ликвидности:*' \
           f' {get_percent((cashLTM + debitorkaLTM) / short_liabilitiesLTM)} (норма >100%)\n\n'
    ans += f'{get_emoji(debtpayLTM / operationLTM, 0, 0.33)}' \
           f'*Проценты к уплате/EBITDA:* {get_percent(debtpayLTM / ebitdaLTM)} (норма <33%)\n\n'
    ans += '----------------\n'
    ans += f'🔍*Вывод:*\n'
    #bot.send_message(chat_id, ans)
    bot.send_message(chat_id, ans, parse_mode="Markdown")
    #send_pictures(chat_id, e, report_type)


def send_report2022(report_title='2022', report_type='all'):
    ans = ''
    ans1 = ''
    x = 1
    for rlink in ReportLink.objects.all():
        print(x, rlink.emitter.title)
        x += 1
        if rlink.link[-1] == '3' and report_type == 'IFRS':
            continue
        if rlink.link[-1] == '4' and report_type == 'RSBU':
            continue
        if check_report_exists(rlink.link, report_title):
            emitter = rlink.emitter

            report_type = ''
            if rlink.link[-1] == '3':
                report_type += 'RSBU'

            else:
                report_type += 'IFRS'

            res = f"{emitter.title} <a href='{rlink.link}'>{report_type}</a>\n"
            ans1 += f"{emitter.title} {report_type}"
            ans += res
        if len(ans1) > 2900:
            bot.send_message(chat_id, ans, parse_mode='HTML')
            ans = ''
            ans1 = ''
    bot.send_message(chat_id, ans, parse_mode='HTML')


def send_link():
    link = 'https://www.e-disclosure.ru/portal/files.aspx?id=37964&type=3'
    title = 'ООО "Элемент Лизинг"'
    ans = ''
    for i in range(10):
        text = f"{title} <a href='{link}'>RSBU</a>\n"
        ans += text
    bot.send_message(chat_id, ans, parse_mode="HTML")

