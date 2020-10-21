from django.shortcuts import render

# Create your views here.


# Michael
from urllib.parse import urljoin
import pprint
import os
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from pathlib import Path
from time import sleep
import asyncio


Path(__file__).resolve().parent.parent


async def wc(url, fn):
    if os.path.isfile(fn):
        with open(fn, 'r', errors='ignore', encoding='utf-8') as f:
            tmp = f.read()
    else:
        # if os.name == 'nt':
        Chrome_driver_path = r'chromedriver_86.0.4240.22_win32.exe'  # TODO

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("headless")
        chrome_options.add_argument(
            'User-Agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"')
        browser = webdriver.Chrome(
            executable_path=Chrome_driver_path, chrome_options=chrome_options)

        browser.get(url)
        js = "var action=document.documentElement.scrollTop=10000"
        browser.execute_script(js)
        await asyncio.sleep(20)
        tmp = browser.page_source
        browser.close()  # close tab not quit
        print(len(tmp), url)

        with open(fn, 'w', errors='ignore', encoding='utf-8') as f:
            f.write(tmp)

    return tmp


async def bank():
    url = 'https://www.momoshop.com.tw/edm/cmmedm.jsp?lpn=O0Y2mh4ttZH&n=1&art_page=9'
    fn = 'cache_bank.html'

    tmp = await wc(url, fn)

    tmp = BeautifulSoup(tmp, "html.parser")  # lxml
    bank = tmp.find('div', id='Area_bankList',
                    class_='Area_bankList').find('ul').find_all('li')
    bank_card = []
    for b in bank:
        bank_card.append({b.get('data-name'): []})
        for _ in b.find('div', class_='bankcard_group_box').find_all('p'):
            bank_card[-1][b.get('data-name')].append(list(_.stripped_strings))
    return bank_card


async def limited_time_sale():
    url = 'https://www.momoshop.com.tw/main/Main.jsp'
    fn = 'cache_limited_sale.html'

    tmp = await wc(url, fn)

    tmp = BeautifulSoup(tmp, "html.parser")  # lxml

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
    g_discount = [100-int(_) for _ in g_discount]

    keys = ['discount', 'prdname', 'href', 'prdprice', 'g_price', 'g_discount']
    re = list(map(list, zip(discount, prdname, href, prdprice, g_price, g_discount)))
    re.sort(key=lambda e: e[0])

    re = [{keys[i]: _[i] for i in range(len(keys))} for _ in re]

    return re


def home(request):

    template_name = 'app/home.html'

    # for "now" event
    asyncio.set_event_loop(asyncio.new_event_loop())

    loop = asyncio.get_event_loop()
    tasks = bank(), limited_time_sale()
    bank_card, ltsale = loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()


    return render(request, template_name, locals())
