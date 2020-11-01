import os
import platform

import selenium
from selenium import webdriver
from urllib.parse import urljoin
from time import sleep
from bs4 import BeautifulSoup
import json


from .models import Bank_card
from .models import Limited_time_sale


from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent  # -> projname/projname/


def wc(url):
    print(' 2wc', url)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(
        'User-Agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"')
    if os.name == 'nt':
        Chrome_driver_path = r'chromedriver_86.0.4240.22_win32.exe'
        chrome_options.add_argument("headless")
        browser = webdriver.Chrome(
            executable_path=Chrome_driver_path,
            chrome_options=chrome_options)
    elif 'inux' in platform.system():
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-dev-shm-usage')
        browser = webdriver.Chrome(chrome_options=chrome_options)
    else:
        print('sorry please check os & selenium browser driver!')

    browser.get(url)
    js = "var action=document.documentElement.scrollTop=10000"
    browser.execute_script(js)
    sleep(40)
    tmp = browser.page_source
    browser.close()  # close tab not quit
    print(' 3wcok', url)
    return tmp


def par_bank_card():
    fn_prefix = 'cache_bank_card'
    url = 'https://www.momoshop.com.tw/edm/cmmedm.jsp?lpn=O0Y2mh4ttZH&n=1&art_page=9'
    tmp = wc(url)
    tmp = BeautifulSoup(tmp, "html.parser")  # lxml
    bank = tmp.find('div', id='Area_bankList',
                    class_='Area_bankList').find('ul').find_all('li')
    bank_card = []
    dict_keys = ['bank_name', 'date', 'suffice', 'discount']
    for b in bank:
        for _ in b.find('div', class_='bankcard_group_box').find_all('p'):
            bank_card.append(
                dict(zip(dict_keys, [b.get('data-name')]+list(_.stripped_strings))))

    if len(bank_card):
        save_cache(fn_prefix, bank_card)
        # save to db
        for row in bank_card:
            obj = Bank_card.objects
            if not obj.filter(**row):
                tmp = obj.create(**row)
                tmp.save()
    print(' 4save', url)
    return bank_card


def par_limited_time_sale():
    fn_prefix = 'cache_limited_sale'
    url = 'https://www.momoshop.com.tw/main/Main.jsp'
    html = wc(url)
    html = BeautifulSoup(html, "lxml")  # html.parser
    html = html.find_all('li', class_='rankingList')
    dict_timesale = []
    keys = ['href', 'imgsrc', 'prdname', 'discount',
            'g_discount', 'prdprice', 'g_prdprice']
    for _ in html:
        href = urljoin(url, (_.find('a').get('href')))
        imgsrc = _.find('img').get('src').rsplit('?', 1)[0]
        prdname = _.find('p', class_='prdname').text
        discount = _.find('span', class_='prdprice_box01').find('b').text
        g_discount = 100-int(float(format(discount.rstrip('折'), '0<2')))

        prdprice = _.find('span', class_='prdprice_box02').text
        g_prdprice = int(prdprice.lstrip('$').replace(',', ''))

        dict_timesale.append(
            dict(zip(keys, [href, imgsrc, prdname, discount, g_discount, prdprice, g_prdprice])))

    if len(dict_timesale):
        save_cache(fn_prefix, dict_timesale)

        # 不比對之欄位
        uf = ['href', 'imgsrc']
        # to db
        for row in dict_timesale:
            row_rm_url = dict(row)
            for _ in uf:
                row_rm_url.pop(_, None)

            obj = Limited_time_sale.objects
            if not obj.filter(**row_rm_url):
                tmp = obj.create(**row)
                tmp.save()

    print(' 4save', url)
    return dict_timesale


def save_cache(fn_prefix, obj):
    with open(str(BASE_DIR/fn_prefix)+'.json', mode='w', errors='ignore', encoding='utf-8') as f:
        json.dump(obj, f, indent=4, ensure_ascii=False)
