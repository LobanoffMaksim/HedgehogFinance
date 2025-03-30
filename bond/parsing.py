from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import os
import openpyxl
import pandas as pd
import time

import requests
from bs4 import BeautifulSoup
from getuseragent import UserAgent
from random import randint as rand
from googlesearch import search

from bond.models import *
from HF.settings import BASE_DIR
from bond.config import *


def get_browser():
    # Get selenium browser.
    options = webdriver.ChromeOptions()
    service = Service(executable_path=driver_path)
    browser = webdriver.Chrome(service=service, options=options)

    return browser


def parse_e_id(link):
    """
    Getting id of emitter from link
    :param link:
    :return:
    """
    ind1 = link.find('id=')
    ind2 = link.find('&')
    if ind1 == -1:
        return -1
    if ind2 == -1:
        ind2 = len(link)
    return int(link[ind1 + 3:ind2])


def get_e_id():
    """
    Getting id of emitter on e-disclosure by googling it by title.
    :return:
    """
    for emitter in Emitter.objects.filter(need_add_fin_data=1):
        try:
            if emitter.title is None or (emitter.e_id is not None and emitter.e_id > 0):
                continue
            time.sleep(1)
            title = emitter.title.replace('"', '')
            query = f'{title} e-disclosure'
            ans = -1
            for j in search(query, tld="co.in", num=10, stop=10, pause=2):
                ans = max(ans, parse_e_id(j))
                if ans > 0:
                    break
            emitter.e_id = ans
            print(emitter.title, ans)
            emitter.save()

        except Exception as ex:
            print("get_e_id_error", emitter.moex_id, emitter.title, ex)

            # break


def get_e_id2():
    """
    Getting id of emitter on e-dislcosure by searching it in e-disclosure search by inn.
    :return:
    """

    browser = get_browser()

    browser.get('https://www.e-disclosure.ru/poisk-po-kompaniyam')
    browser.maximize_window()

    for emitter in Emitter.objects.filter(inn__isnull=False, e_id__isnull=True):
        if emitter.inn < 10 ** 9:
            continue
        print("start to search e_id for", emitter.inn)
        elem = browser.find_element(By.XPATH, '//*[@id="textfield"]')
        elem.clear()
        elem.send_keys(f'{emitter.inn}\n', Keys.RETURN)
        try:
            time.sleep(4)
            browser.implicitly_wait(10)
            elem = browser.find_element(By.XPATH, '//*[@id="cont_wrap"]/table/tbody/tr[2]/td[1]/a')
            link = elem.get_attribute("href")
            title = elem.get_attribute("innerHTML")
            print(title, link)
            emitter.e_id = parse_e_id(link)
            emitter.title = title

            emitter.save()
        except:
            browser.get('https://www.e-disclosure.ru/poisk-po-kompaniyam')
            continue


def build_report_links():
    """
    Finding links with emitter reports on e-disclosure by using e_id
    :return:
    """
    for emitter in Emitter.objects.filter(e_id__isnull=False):
        if emitter.e_id == -1:
            continue
        print(emitter.title, 'RSBU')
        emitter.reportlink_set.all().delete()
        link1 = f'https://www.e-disclosure.ru/portal/files.aspx?id={emitter.e_id}&type=3'
        rlink1 = ReportLink(emitter=emitter, link=link1)
        rlink1.save()
        link2 = f'https://www.e-disclosure.ru/portal/files.aspx?id={emitter.e_id}&type=4'
        r = requests.get(link2)
        if r.url != f'https://www.e-disclosure.ru/portal/company.aspx?id={emitter.e_id}':
            print(emitter.title, 'IFRS')
            rlink2 = ReportLink(emitter=emitter, link=link2)
            rlink2.save()
        time.sleep(1)


def find_emitters_with_ifrs_reports():
    """
    Finding emitters who have ifrs reports
    :return:
    """
    cnt = 0
    for emitter in Emitter.objects.filter(e_id__isnull=False, ifrs_exists=False)[28:]:
        flag = 0
        cnt += 1
        print(cnt)
        for link in emitter.reportlink_set.all():
            time.sleep(1)
            r = requests.get(link.link)
            bs = BeautifulSoup(r.text, "lxml")
            temp = bs.find('table', 'files-table')
            if temp is None:
                continue
            temp = temp.find_all('tr')
            for elem in temp[1:]:
                year = elem.find_all('td')
                if len(year) > 2 and 'МСФО' in year[1].text:
                    flag = 1
                    break
        if flag:
            print('success', emitter.title, emitter.inn)
            emitter.ifrs_exists = True
            emitter.save()
        else:
            print('no', emitter.title, emitter.inn)


def get_rusbonds_link(isin):
    """
    Getting emitter page on rusbonds by googling
    :param isin:
    :return:
    """
    time.sleep(1)
    query = f'{isin} rusbonds'
    for j in search(query):
        return j
    return None


def get_rusbonds_data(link):
    """
    Getting such data as sector title and okpo from rusbonds
    :param link:
    :return:
    """
    time.sleep(1)
    r = requests.get(link)
    bs = BeautifulSoup(r.text, "lxml")
    bs = bs.find('div', 'page-wrapper').find('div', 'page').find('div', 'bond-page').find('div', 'bond-overview').find(
        'div', 'container')
    bs = bs.find('div', 'indexes').findAll('section', 'type')[1].find('ul', 'data-group').findAll('div', 'data-item')
    title = bs[0].find('div', 'data-value').text
    sector = bs[2].find('div', 'data-value').text
    okpo = bs[1].find('div', 'data-value').text
    return title, okpo, sector


def get_title_sector(emitter):
    """
    Getting sector title for emitter, but it is not finding it.
    TO DO: find what this do
    :param emitter:
    :return:
    """
    try:
        bond = emitter.bond_set.first()
        link1 = get_rusbonds_link(bond.isin)
        data = get_rusbonds_data(link1)
        title, okpo, sector1 = data
        emitter.title = title
        emitter.save()
    except Exception as ex:
        emitter.save()
        print("Error get_sector_title", emitter.moex_id, ex)


def get_title(emitter):
    """
    Getting title for emitter
    :param emitter:
    :return:
    """
    try:
        bond = emitter.bond_set.first()
        link1 = get_rusbonds_link(bond.isin)
        data = get_rusbonds_data(link1)
        title, okpo, sector1 = data
        print(title)
        emitter.title = title
        emitter.save()
    except Exception as ex:
        emitter.save()
        print("Error get_title", emitter.moex_id, ex)


def get_titles():
    """
    Getting titles for all emitters
    :return:
    """
    x = 0
    for emitter in Emitter.objects.filter(title__isnull=True):
        x += 1
        if emitter.bond_set.all().count() == 0:
            continue
        try:
            get_title(emitter)
            print(x, emitter.title)
        except Exception as ex:
            print('Error get_ls_links', emitter.moex_id, ex)


def get_session():
    """
    Getting session for parsing.
    :return:
    """
    session = requests.Session()
    session.headers = {
        'User-Agent': UserAgent("windows").Random(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'ru,en-US;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache'}
    return cfscrape.create_scraper(sess=session)


def conv_int(val):
    if val == '':
        return 0
    return int(float(val))


def parse_credit_rating(s, possible):
    ans = ''
    for c in s:
        if c in possible:
            ans += c
    return ans


def get_ra_expert_rating(title):
    """
    Getting credit ratings from expert ra by google
    :param title:
    :return:
    """
    try:
        session = get_session()
        title = title.replace('"', '')

        time.sleep(1)
        for j in search(f'{title} Эксперт РА', num=10, stop=10, pause=2):
            link = j
            break
        try:
            response = session.get(link)
        except Exception as ex:
            return []
        bs = BeautifulSoup(response.text, "lxml")
        bs = bs.find('div', 'b-title-rating__rating')
        if bs is None:
            return []
        bs = bs.find('a')
        print(title, bs.text)
        return [(bs.text, 'https://www.raexpert.ru' + bs["href"]), ]
    except Exception as ex:
        print(ex)
        time.sleep(15 * 60)
        return get_ra_expert_rating(title)


def get_ra_expert_rating_without_google(title):
    """
    Getting expert ra rating by searching on their site
    :param title:
    :return:
    """
    browser = get_browser()
    browser.get('https://www.raexpert.ru/search/')
    time.sleep(0.5)
    elem = browser.find_element(By.CLASS_NAME, 'b-search__input')
    elem.send_keys(f'{title}', Keys.RETURN)

    share = browser.find_element(By.CLASS_NAME, 'b-search__submit')
    share.click()
    time.sleep(0.5)
    try:
        elem = browser.find_element(By.ID, 'companies').find_element(By.CLASS_NAME, 'b-table__text')
        elem.click()
        time.sleep(1)
        bs = BeautifulSoup(browser.page_source, 'lxml')
        browser.close()
        bs = bs.find('div', 'b-title-rating__rating')
        if bs is None:
            return []
        bs = bs.find('a')
        print(bs.text, title)
        return [(bs.text, 'https://www.raexpert.ru' + bs["href"]), ]
    except Exception as ex:
        print(ex)
        browser.close()
        return []


def get_akra_rating(title):
    """
    Getting akra ratings by searching on their site by title
    :param title:
    :return:
    """
    browser = get_browser()
    time.sleep(1)
    browser.get('https://www.acra-ratings.ru/')

    elem = browser.find_element(By.CLASS_NAME, 'input__header').find_element(By.TAG_NAME, 'input')
    time.sleep(1)
    elem.send_keys(f'{title}"\n', Keys.RETURN)
    time.sleep(1)
    data = browser.find_elements(By.CLASS_NAME, "search-result__item")
    link = None
    for elem in data:
        if elem.find_element(By.CLASS_NAME, 'tag').text == 'Эмитент':
            link = elem.find_element(By.TAG_NAME, 'a').get_attribute("href")
            break
    if link is not None:
        browser.get(link)
        try:
            elem = browser.find_element(By.CLASS_NAME, 'rating-widget')
            rlink = browser.find_element(By.CLASS_NAME, 'rating-item').find_element(By.TAG_NAME, 'a').get_attribute(
                'href')
        except Exception as ex:
            return []
        print(elem.text, rlink)
        return [(elem.text, rlink), ]
    else:
        return []


def get_nkr_rating(title):
    """
    Getting nkr ratings by searching on their site.
    :param title:
    :return:
    """
    browser = get_browser()
    time.sleep(1)
    browser.get('https://ratings.ru/search')

    elem = browser.find_element(By.TAG_NAME, 'input')
    time.sleep(1)
    elem.send_keys(f'{title}\n', Keys.RETURN)
    time.sleep(1)
    try:
        if browser.find_element(By.CLASS_NAME, 's_page-category').text == "Эмитенты":
            elem = browser.find_element(By.CLASS_NAME, 's_page-item')
            elem.click()
            elem = browser.find_element(By.CLASS_NAME, 'section-head__content').find_element(By.CLASS_NAME, 'npr-class')
            browser.close()
            return elem.text
        else:
            browser.close()
            return None
    except Exception as ex:
        print(ex)
        browser.close()
        return None


def upd_raex_ratings():
    """
    Updating expert ra ratings for all emitters
    :return:
    """
    for emitter in Emitter.objects.filter(title__isnull=False, credit_level__isnull=True):
        if emitter.creditrating_set.filter(agency='ra_expert').count() > 0:
            continue
        print(emitter.title)
        data = get_ra_expert_rating_without_google(emitter.title);
        for rating, link in data:
            cr = CreditRating(emitter=emitter, link=link, value=rating, agency='ra_expert')
            cr.save()

        if len(data) == 0:
            cr = CreditRating(emitter=emitter, value='-1', agency='ra_expert')
            cr.save()


def upd_akra_ratings():
    """
    Parsing akra ratings for all emitters.
    :return:
    """
    for emitter in Emitter.objects.filter(title__isnull=False, credit_level__isnull=True):
        if emitter.creditrating_set.filter(agency='akra').count() > 0:
            continue
        print(emitter.title)
        data = get_akra_rating(emitter.title);
        for rating, link in data:
            cr = CreditRating(emitter=emitter, link=link, value=rating, agency='akra')
            cr.save()

        if len(data) == 0:
            cr = CreditRating(emitter=emitter, value='-1', agency='akra')
            cr.save()


def get_creditrating_table(page_num=5):
    """
    Getting emitter rating from rusbonds.
    Now it is not available.
    :param page_num:
    :return:
    """
    browser = get_browser()
    time.sleep(1)
    browser.get('https://rusbonds.ru/filters/bonds/new')
    time.sleep(1)
    # browser.find_element(By.CLASS_NAME, 'close').click()
    elem = browser.find_element(By.CLASS_NAME, 'sign-in')
    elem.click()
    elem = browser.find_element(By.CLASS_NAME, 'login-form')
    login, password = elem.find_elements(By.TAG_NAME, 'input')
    login.send_keys('mlpotato@yandex.ru', Keys.RETURN)
    password.send_keys('November2005\n', Keys.RETURN)
    button = elem.find_elements(By.TAG_NAME, 'button')[1]
    button.click()
    time.sleep(25)
    table = []
    for i in range(page_num):
        browser.execute_script("window.scrollTo(0, 1080)")
        elem = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "el-table__body")))

        for data in elem.find_element(By.TAG_NAME, 'tbody').find_elements(By.CLASS_NAME, 'el-table__row'):
            cur = [smth.text for smth in data.find_elements(By.CLASS_NAME, 'el-table__cell')]
            isin = cur[-1]

            if Bond.objects.filter(isin=isin).exists():
                b = Bond.objects.get(isin=isin)
                if cur[12] != '-':
                    CreditRating.objects.filter(emitter=b.emitter, agency='ra_expert').delete()
                    cr = CreditRating(emitter=b.emitter, value=cur[12], agency='ra_expert')
                    cr.save()
                if cur[13] != '-':
                    CreditRating.objects.filter(emitter=b.emitter, agency='akra').delete()
                    cr = CreditRating(emitter=b.emitter, value=cur[13], agency='akra')
                    cr.save()
                if cur[14] != '-':
                    CreditRating.objects.filter(emitter=b.emitter, agency='nra').delete()
                    cr = CreditRating(emitter=b.emitter, value=cur[14], agency='nra')
                    cr.save()
                if cur[15] != '-':
                    CreditRating.objects.filter(emitter=b.emitter, agency='nkr').delete()
                    cr = CreditRating(emitter=b.emitter, value=cur[15], agency='nkr')
                    cr.save()
        if i != page_num - 1:
            browser.find_element(By.CLASS_NAME, 'table-pagination').find_element(By.CLASS_NAME, 'btn-next').click()


def get_sector_table(page_num=5):
    """
    Getting sectors for all emitters.
    :param page_num: how many pages should we parse
    :return:
    """
    browser = get_browser()
    time.sleep(1)
    browser.get('https://rusbonds.ru/filters/bonds/new')
    time.sleep(1)
    browser.maximize_window()
    time.sleep(5)
    elem = browser.find_element(By.CLASS_NAME, 'sign-in')
    elem.click()
    elem = browser.find_element(By.CLASS_NAME, 'login-form')
    login, password = elem.find_elements(By.TAG_NAME, 'input')
    login.send_keys('mlpotato@yandex.ru', Keys.RETURN)
    password.send_keys('November2005\n', Keys.RETURN)
    button = elem.find_elements(By.TAG_NAME, 'button')[1]
    button.click()
    time.sleep(30)
    table = []
    for i in range(page_num):
        browser.execute_script("window.scrollTo(0, 1080)")
        elem = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "el-table__body")))

        for data in elem.find_element(By.TAG_NAME, 'tbody').find_elements(By.CLASS_NAME, 'el-table__row'):
            cur = [smth.text for smth in data.find_elements(By.CLASS_NAME, 'el-table__cell')]
            isin = cur[-1]

            if Bond.objects.filter(isin=isin).exists():
                b = Bond.objects.get(isin=isin)
                if b.emitter.sector is not None or cur[4] == '-':
                    continue
                b.emitter.sector = Sector.objects.get_or_create(title=cur[4], industry__isnull=True)[0]

                b.emitter.save()
                print(b.emitter.title, b.emitter.sector.title)
        if i != page_num - 1:
            browser.find_element(By.CLASS_NAME, 'table-pagination').find_element(By.CLASS_NAME, 'btn-next').click()


def conv_bo_nalog(s):
    if s == '':
        return ''
    ans = 0
    flag = 1
    for c in s:
        if c == '\n':
            break
        elif c == ' ':
            continue
        elif c == '(' or c == ')':
            flag = -1
        elif '0' <= c <= '9':
            ans *= 10
            ans += int(c)
        else:
            return s
    return ans * flag


def parse_report_data(browser):
    """
    Parsing one report (for 1 year) data from bo.nalog.ru.
    The best solution.
    :param browser:
    :return:
    """
    browser.implicitly_wait(45)
    browser.execute_script("window.scrollTo(0, 0)")
    time.sleep(7)
    for elem in browser.find_elements(By.CLASS_NAME, 'grid-reports-item'):
        if elem.find_element(By.CLASS_NAME, 'grid-reports-item-header').get_attribute('id') in ['balance',
                                                                                                'financialResult',
                                                                                                'fundsMovement']:
            elem.find_element(By.CLASS_NAME, 'button-toggle').click()
            time.sleep(1)
    browser.execute_script("window.scrollTo(0, 300)")
    time.sleep(4)
    elem = browser.find_element(By.CLASS_NAME, 'table-header-group')

    i = 0
    while i <= 4:
        elem = browser.find_elements(By.CLASS_NAME, 'table-header-group')[i]
        print(elem.text)

        elem.click()
        time.sleep(1)
        i += 1

    table = []
    for smth in browser.find_elements(By.CLASS_NAME, 'tabulator-selectable'):
        table.append([])
        for elem in smth.find_elements(By.TAG_NAME, 'div'):
            table[-1].append(elem.text)

    for smth in table:
        for j in range(1, len(smth)):
            smth[j] = conv_bo_nalog(smth[j])

    ans = []
    year = browser.find_element(By.CLASS_NAME, 'grid-reports-header-top__period').find_element(By.CLASS_NAME,
                                                                                               'button_primary').text
    for elem in table:
        if len(elem[0]) == 0:
            continue
        ans.append([year, ])
        for t in elem:
            if t != '':
                ans[-1].append(t)
    return ans


def upd_bo_nalog_data(emitter, browser=None):
    """
    Getting report data from bo.nalog.ru
    :param emitter:
    :param browser:
    :return:
    """
    if browser is None:
        browser = get_browser()
    browser.implicitly_wait(45)
    browser.get('https://bo.nalog.ru/')
    browser.maximize_window()
    time.sleep(3)

    browser.find_element(By.CLASS_NAME, 'input-search').find_element(By.TAG_NAME, 'input').send_keys(f'{emitter.inn}\n',
                                                                                                     Keys.RETURN)
    try:
        browser.find_element(By.CLASS_NAME, 'results-search-tbody').find_elements(By.CLASS_NAME,
                                                                                  'results-search-table-row')[0].click()
    except Exception as ex:
        return 0
    elem = \
    browser.find_element(By.CLASS_NAME, 'header-card-content').find_elements(By.CLASS_NAME, 'header-card-content-box')[
        0].find_elements(By.CLASS_NAME, 'header-card-content-item')[1]
    if elem.find_element(By.CLASS_NAME, 'header-card-content-item__text').find_element(By.TAG_NAME, 'p').text != str(
            emitter.inn):
        return 0
    ans1 = parse_report_data(browser)
    years = browser.find_element(By.CLASS_NAME, 'grid-reports-header-top__period').find_elements(By.TAG_NAME, 'button')
    number_of_reports = 3
    if len(years) >= 3:
        years[-3].click()
        ans2 = parse_report_data(browser)
    elif len(years) >= 2:
        years[-2].click()
        ans2 = parse_report_data(browser)
        number_of_reports = 2
    else:
        ans2 = []
        number_of_reports = 1
    emitter.finindicator_set.filter(report_type='rsbu').delete()
    for elem in ans1:
        if str(elem[2]) in conv_report2 and isinstance(elem[3], int):
            fi = FinIndicator(emitter=emitter, report_type='rsbu', type=conv_report2[str(elem[2])], year='LTM',
                              value=elem[3] * 1000)
            fi.save()
        if (str(elem[2]) in conv_report2) and isinstance(elem[4], int):
            fi = FinIndicator(emitter=emitter, report_type='rsbu', type=conv_report2[str(elem[2])],
                              year=str(int(elem[0]) - 1),
                              value=elem[4] * 1000)
            fi.save()
    for elem in ans2:
        if number_of_reports > 2 and str(elem[2]) in conv_report2 and isinstance(elem[3], int):
            fi = FinIndicator(emitter=emitter, report_type='rsbu', type=conv_report2[str(elem[2])], year=elem[0],
                              value=elem[3] * 1000)
            fi.save()
        if str(elem[2]) in conv_report2 and isinstance(elem[4], int):
            fi = FinIndicator(emitter=emitter, report_type='rsbu', type=conv_report2[str(elem[2])],
                              year=str(int(elem[0]) - 1),
                              value=elem[4] * 1000)
            fi.save()

    for elem in FinIndicator.objects.filter(emitter=emitter, report_type='rsbu', type='non-current-assets'):
        fi = FinIndicator(emitter=emitter, report_type='rsbu', type='amortization',
                          year=elem.year, value=int(elem.value * 0.0906))
        fi.save()
    for elem in FinIndicator.objects.filter(emitter=emitter, report_type='rsbu', type__in=['commercial-expenses',
                                                                                           'interest-payable',
                                                                                           'management-expenses',
                                                                                           'interest-payable',
                                                                                           'other-expenses',
                                                                                           'operation-cash-outflow',
                                                                                           'investing-outflow',
                                                                                           'CAPEX',
                                                                                           'borrow-outflow',
                                                                                           'ICF',
                                                                                           'finance-outflow',
                                                                                           ]):
        elem.value *= -1
        elem.save()
    return 1


def upd_all_reports(inn=-1):
    """
    Updating report data with bo.nalog.ru
    :param inn: if we want to update information only for 1 emitter we should select inn
    :return:
    """

    browser = get_browser()
    cnt = 0
    if inn == -1:
        for emitter in Emitter.objects.filter(report_data_level=0, inn__isnull=False, need_add_fin_data=True,
                                              title__isnull=False):
            print(cnt, emitter.title, emitter.inn, 'start')
            try:
                res = upd_bo_nalog_data(emitter, browser)
                if res:
                    print(cnt, emitter.title, 'succes')
                    emitter.report_data_level = 3
                    emitter.save()
                else:
                    print(cnt, emitter.title, 'not-found')
                    emitter.report_data_level = 4
                    emitter.save()
                cnt += 1
            except Exception as ex:
                raise ex
                break
    else:
        for emitter in Emitter.objects.filter(need_add_fin_data=True, inn=inn):
            print(cnt, emitter.title, emitter.inn, 'start')
            try:
                res = upd_bo_nalog_data(emitter, browser)
                if res:
                    print(cnt, emitter.title, 'succes')
                    emitter.report_data_level = 3
                    emitter.save()
                else:
                    print(cnt, emitter.title, 'not-found')
                    emitter.report_data_level = 4
                    emitter.save()
                cnt += 1
            except Exception as ex:
                raise ex
                break


def get_descriptions():
    """
    Getting descriptions of emitters from rusbonds.ru
    :return:
    """
    driver = get_browser()
    driver.implicitly_wait(45)
    driver.get('https://rusbonds.ru/bonds/174418/')
    driver.maximize_window()
    cnt = 0
    for e in Emitter.objects.filter(inn__isnull=False, title__isnull=False, sector__isnull=False):
        if e.sector.id == 63:
            continue
        if e.description is None or e.description == 'Описание отсутствует...' or len(e.description) < 10:
            print(e.title, e.inn)

            time.sleep(3)
            elem = driver.find_element(By.XPATH, '//*[@id="top"]/div[1]/div/div[4]/div/form/input')
            elem.clear()
            elem.clear()

            time.sleep(1)
            elem.send_keys(f'{e.inn}\n', Keys.RETURN)
            elem.clear()
            elem.clear()
            try:
                driver.find_element(By.XPATH, '//*[@id="top"]/div[1]/div/div[4]/div/form/div/div[2]/div/div[1]').click()
            except:
                continue
            elem.clear()
            elem.clear()
            try:
                text = driver.find_element(By.XPATH,
                                           '//*[@id="__layout"]/div/div/main/div/div/div[2]/section/div/div/div/div[2]/section/div[2]/p').text
                elem.clear()
                elem.clear()
                cnt += 1
                if len(text) == 0:
                    continue
                print(cnt, e.title, text)

                e.description = text
                e.save()
            except:
                continue
