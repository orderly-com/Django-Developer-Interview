import os
import platform


import selenium
from selenium import webdriver
from urllib.parse import urljoin
from time import sleep
from bs4 import BeautifulSoup


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
    elif 'inux' in platform.system():
        Chrome_driver_path = r'/usr/local/share/chromedriver'
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-dev-shm-usage')
    else:
        print('sorry please check os & selenium browser driver!')
    browser = webdriver.Chrome(
        executable_path=Chrome_driver_path,
        chrome_options=chrome_options)
    browser.get(url)
    js = "var action=document.documentElement.scrollTop=10000"
    browser.execute_script(js)
    sleep(40)
    tmp = browser.page_source
    browser.close()  # close tab not quit
    print(' 3wcok', url)
    return tmp


def par_bank():
    fn = BASE_DIR/'cache_bank.txt'
    url = 'https://www.momoshop.com.tw/edm/cmmedm.jsp?lpn=O0Y2mh4ttZH&n=1&art_page=9'
    # print('1', url)
    tmp = wc(url)
    tmp = BeautifulSoup(tmp, "html.parser")  # lxml
    bank = tmp.find('div', id='Area_bankList',
                    class_='Area_bankList').find('ul').find_all('li')
    bank_card = []
    for b in bank:
        bank_card.append({b.get('data-name'): []})
        for _ in b.find('div', class_='bankcard_group_box').find_all('p'):
            bank_card[-1][b.get('data-name')
                          ].append(list(_.stripped_strings))
    # 有抓到更新
    if len(bank_card):
        with open(fn, mode='w', errors='ignore', encoding='utf-8') as f:
            f.write(str(bank_card))
    print('4', url)
    return bank_card


def par_limited_time_sale():
    fn = BASE_DIR/'cache_limited_sale.txt'
    url = 'https://www.momoshop.com.tw/main/Main.jsp'
    # print('1', url)
    tmp = wc(url)
    tmp = BeautifulSoup(tmp, "lxml")  # html.parser
    tmp = tmp.find_all('li', class_='rankingList')
    href = [urljoin(url, _.find('a').get('href')) for _ in tmp]
    tmp = [_.find('a') for _ in tmp]
    prdname = [_.find('p', class_='prdname').text for _ in tmp]
    prdprice = [_.find('p', class_='prdprice').find(
        'span', class_='prdprice_box02').text for _ in tmp]
    discount = [_.find('p', class_='prdprice').find(
        'span', class_='prdprice_box01').find('b', class_='discount').text for _ in tmp]
    g_price = [int(x.replace('$', '').replace(',', '')) for x in prdprice]
    g_discount = [format(_.replace('折', ''), '0<2') for _ in discount]
    g_discount = [100-int(float(_)) for _ in g_discount]

    keys = ['discount', 'prdname', 'href',
            'prdprice', 'g_price', 'g_discount']
    re = list(
        map(list, zip(discount, prdname, href, prdprice, g_price, g_discount)))
    re.sort(key=lambda e: e[0])
    re = [{keys[i]: _[i] for i in range(len(keys))} for _ in re]
    # 有抓到更新
    if len(re):
        with open(fn, mode='w', errors='ignore', encoding='utf-8') as f:
            f.write(str(re))
    print(' 4save', url)
    return re
