from .models import *
import openpyxl
import pandas as pd
from bond.parsing import *
from bond.config import interesting_years, conv_report, credit_ratings
import json
from collections import defaultdict
from bs4 import BeautifulSoup


def get_years_number(data):
    """
    :param data: list with finance data
    :return: number of years of reporting in file
    """

    for i in range(1, 100):
        if data[i][0] is None:
            return i


def get_dividing_index(data):
    """
    :param data: list with finance data
    :return: index of line which separates rsbu and ifrs reports
    """
    for i in range(100):
        if data[0][i] is None:
            return i


def convert_report_to_int(data, year_cnt, dividing_ind):
    for i in range(1, year_cnt - 1):
        data[i][0] = int(data[i][0])
    for i in range(1, year_cnt):
        for j in range(16, len(data[i])):
            if j != dividing_ind and str(data[i][j]) != 'nan':
                    data[i][j] = int(data[i][j])


def convert_units_of_measurement(data, year_cnt, dividing_ind):
    """
    Integers in reports could be given in thousans or millions.
    Therefore, this function converts all of them in 1.
    """
    for i in range(1, year_cnt):
        for j in range(16, dividing_ind):
            if data[i][j] is not None:
                data[i][j] *= int(data[year_cnt + 1][16])
        for j in range(dividing_ind + 1, len(data[i])):
            if data[i][j] is not None:
                data[i][j] *= int(data[year_cnt + 1][dividing_ind + 1])


def check_data_exists(data, i, j, dividing_ind, year_cnt):
    if data[i][j] is None:
        return False

    if j < dividing_ind:
        return data[i][16] > data[year_cnt + 1][16]
    else:
        return data[i][dividing_ind + 1] > data[year_cnt + 1][dividing_ind + 1]


def get_report_type(j, dividing_ind):

    if j < dividing_ind:
        return 'rsbu'
    else:
        return 'ifrs'


def parse_xslx(finf):
    """
    Collects all data about emitter from .xlsx file made by admins.
    :param finf: EmitterFinFile object.
    :return:
    """
    book = openpyxl.open(finf.fin_file, data_only=True)
    sheet = book.active
    data = pd.DataFrame(sheet.values)
    emitter = Emitter.objects.get(moex_id=data[1][8])
    emitter.title = data[1][1]
    emitter.description = data[1][2]
    emitter.ceo = data[1][3]
    emitter.website1 = data[1][6]
    emitter.website2 = data[1][7]
    emitter.is_system_important = bool(data[1][9])

    year_cnt = get_years_number(data)
    dividing_ind = get_dividing_index(data)

    convert_report_to_int(data, year_cnt, dividing_ind)

    convert_units_of_measurement(data, year_cnt, dividing_ind)

    for i in range(1, year_cnt):
        year = str(data[i][0])
        if year != 'LTM' and year[-2] == '.':
            year = year[:-2]
        for j in range(16, len(data[i])):
            if data[i][j] is None:
                continue
            if j == dividing_ind:
                continue

            if check_data_exists(data, i, j, dividing_ind, year_cnt):
                if data[0][j] is None:
                    print(j, data[0])
                    continue

                fin_indicator = FinIndicator.objects.get_or_create(emitter=emitter,
                                                                   report_type=get_report_type(j, dividing_ind),
                                                                   type=data[0][j],
                                                                   year=year)[0]


                fin_indicator.value = data[i][j]
                fin_indicator.save()

    emitter.fin_file = finf
    emitter.save()


def upload_finfile(user, f):
    """
    Saves file and parse all report data from file.
    :param user: user who submited this file.
    :param f: file
    :return:
    """
    finf = EmitterFinFile(updated_by=user, fin_file=f)
    finf.save()
    parse_xslx(finf)


def convert_int(s):
    """
    Converts ints in different variants to ordinary int
    :param s: string with number
    :return:
    """
    ans = 0
    flag = 0
    s = str(s)
    for c in s:
        if c == '-':
            return 0
        elif c == '(' or c == ')':
            flag = 1
        elif c in '0123456789':
            ans *= 10
            ans += int(c)
    if flag:
        ans = -ans
    return ans


def clear_credit_rating(rating):
    """
    Converts credit rating to normal variant.
    :param rating:
    :return:
    """
    possible = ['A', 'B', 'C', 'D', '+', '-']
    ans = ''
    for c in rating:
        if c in possible:
            ans += c
    return ans


def count_credit_level():
    for emitter in Emitter.objects.all():
        for rating in emitter.creditrating_set.all():
            val = clear_credit_rating(rating.value)
            if val in credit_ratings:
                emitter.credit_level = credit_ratings.index(val)
                emitter.save()


def check_report_exists(link, report_title='2022'):
    """
    Check if the report is already exists on e-disclosure.com
    :param link: link on the page of emitter
    :param report_title:
    :return:
    """
    time.sleep(1)
    r = requests.get(link)
    bs = BeautifulSoup(r.text)
    temp = bs.find('table', 'files-table')
    if temp is None:
        return 0
    temp = temp.find_all('tr')
    for elem in temp[1:]:
        year = elem.find_all('td')
        if len(year) >= 3 and year[2].text == report_title:
            return 1
    return 0


def delete_bad_years():
    """
    Delete FinIndicators with non-correct information.
    :return:
    """

    titles = ['net-profit', 'ebt', 'operation-profit', 'revenue']

    for emitter in Emitter.objects.filter(ceo='???'):
        for title in titles:
            for year in interesting_years:
                if emitter[('rsbu', title, year)] == 0 and year != '2022':
                    emitter.finindicator_set.filter(year=year).delete()


def clear_credit_ratings():
    """
    Delete all dublicate credit ratings
    :return:
    """
    for emitter in Emitter.objects.all():
        j = defaultdict(str)
        for cr in emitter.creditrating_set.all():
            if cr.value is None or cr.value == '' or cr.agency is None or cr.value == '-1':
                continue
            j[cr.agency] = cr.value
        emitter.creditrating_set.all().delete()
        for key in j:
            cr = CreditRating(emitter=emitter, agency=key, value=j[key])
            cr.save()


def check_creditratings_ok():
    for emitter in Emitter.objects.filter(credit_level__isnull=False):
        if emitter.creditrating_set.count() == 0:
            print(emitter.title)
