from .config import downloads_dir, reports_dir, report_images_dir
from .models import Emitter, Report
from .parsing import get_browser

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from pdf2image import convert_from_path
from PyPDF2 import PdfReader

import time
import os
import shutil
import zipfile

def get_download_links(emitter, report_type='rsbu'):

    if emitter.e_id is None:
        return
    report_type_conv = {'rsbu': 3, 'ifrs': 4}
    link = f'https://e-disclosure.ru/portal/files.aspx?id={emitter.e_id}&type={report_type_conv[report_type]}'
    print(emitter.title, 'start')
    browser = get_browser()
    try:
        browser.get(link)
    except Exception as ex:
        print(f"Emitter {emitter.title} has no report page")
        browser.close()
        report = Report(emitter=emitter, type=report_type, status='ER')
        report.save()
        return
    browser.maximize_window()
    try:
        elem = browser.find_element(By.XPATH, '//*[@id="cont_wrap"]/div[2]/table')
        report_lines = elem.find_elements(By.TAG_NAME, 'tr')
        for line in report_lines[1:]:
            cells = line.find_elements(By.TAG_NAME, 'td')
            download_link = cells[5].find_element(By.CLASS_NAME, 'file-link').get_attribute('href')
            description = cells[2].get_attribute("innerHTML")
            report = Report(emitter=emitter, type=report_type, status='ST', description=description,
                            download_link=download_link, )
            report.save()
            # print(emitter.title, cells[2].get_attribute("innerHTML"), download_link)
        print(emitter.title, 'success')
    except Exception as ex:
        print('Error with', emitter.title, 'link=', link)
        print(ex)
        report = Report(emitter=emitter, type=report_type, status='ER')
        report.save()
        browser.close()
    time.sleep(5)


def get_all_download_links():
    for emitter in Emitter.objects.filter(e_id__isnull=False):
        if emitter.report_set.count():
            continue
        get_download_links(emitter)


def get_recently_downloaded_file():
    files = os.listdir(downloads_dir)
    files.sort(key=lambda x: -os.path.getmtime(downloads_dir + '/' + x))
    return downloads_dir + '/' + files[0]


def download_report(browser, link):
    try:
        prev_file = get_recently_downloaded_file()
        browser.get(link)
        time.sleep(2)
        file = get_recently_downloaded_file()
        while 'crdownload' in file:
            time.sleep(3)
            file = get_recently_downloaded_file()

        return file
    except Exception as ex:
        print("Error with downloading report from link", link, ex)
        return None


def download_emitter_reports(emitter, report_type='rsbu'):
    browser = get_browser()
    for report in emitter.report_set.filter(status='ST', type=report_type):
        time.sleep(1)
        file = download_report(browser, report.download_link)
        if file is None:
            continue # ???
        report.file_path = file
        print(report.download_link, file)
        report.status = 'DW'
        report.save()
    browser.close()


def unzip_file(file_path, dir_to_save):
    with zipfile.ZipFile(file_path, "r") as zip_ref:
        return zip_ref.extractall(dir_to_save)


def get_pages_num(pdf_file_path):
    with open(pdf_file_path, "rb") as pdf_file:
        pdf_reader = PdfReader(pdf_file)
        return len(pdf_reader.pages)


def find_report_file(report_dir):
    files = os.listdir(report_dir)
    files.sort(key=lambda x: -get_pages_num(report_dir + '/' + x))
    return files[0]


def unzip_emitter_reports(emitter):
    emitter_reports_dir = reports_dir + '/' + emitter.title

    if not os.path.isdir(emitter_reports_dir):
        os.mkdir(emitter_reports_dir)
    for report in emitter.report_set.filter(status='DW'):
        report_dir = emitter_reports_dir + '/' + f'{report.description} {report.type}'
        if not os.path.isdir(report_dir):
            os.mkdir(report_dir)
        unzip_file(report.file_path, report_dir)
        report_file = report_dir + '/' + find_report_file(report_dir)
        report.file_path = report_file
        report.status = 'UZ'
        report.save()


def convert_to_images(file_path):
    name = os.path.basename(file_path)
    dir_to_save = f'{report_images_dir}/{name}'
    if os.path.isdir(dir_to_save):
        shutil.rmtree(dir_to_save)

    os.mkdir(dir_to_save)

    pages = convert_from_path(file_path)
    for count, page in enumerate(pages):
        page.save(f'{dir_to_save}/page_{count}.jpg', 'JPEG')

    return dir_to_save


def image_emitter_reports(emitter):
    for report in emitter.report_set.filter(status='UZ'):
        report.images_dir = convert_to_images(report.file_path)
        print(report.images_dir)
        report.status = 'IM'
        report.save()


def get_page_num(p):
    return int(p[p.find('_') + 1:p.find('.')])


def parse_raw_data():
    report = Report.objects.get(id=12494)
    images = os.listdir(report.images_dir)
    images = sorted(images, key=lambda p: get_page_num(p))

    for image in images:
        if get_page_num(image) < len(images) // 5:
            continue
        print(image)
