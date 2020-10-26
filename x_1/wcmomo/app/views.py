from django.shortcuts import render

# Create your views here.


# Michael
from urllib.parse import urljoin
import os
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from pathlib import Path
from time import sleep
import asyncio
# from asgiref.sync import async_to_sync, sync_to_async

import platform


# import datetime
# from apscheduler.schedulers.background import BackgroundScheduler
# from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

# scheduler = BackgroundScheduler()
# scheduler.add_jobstore(DjangoJobStore(), 'default')


Path(__file__).resolve().parent.parent

# register_events(scheduler)
# scheduler.start()


# @register_job(scheduler, "cron", minute='*/2')
# def wc_job():
#     print('JOB_METH02')
#     with open('job2.log', 'a', errors='ignore', encoding='utf-8') as f:
#         f.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'\n')

#     urls = ['https://www.momoshop.com.tw/edm/cmmedm.jsp?lpn=O0Y2mh4ttZH&n=1&art_page=9',
#             'https://www.momoshop.com.tw/main/Main.jsp']
#     fns = ['cache_bank.html', 'cache_limited_sale.html']

#     asyncio.set_event_loop(asyncio.new_event_loop())
#     loop = asyncio.get_event_loop()
#     tasks = wc(urls[0], fns[0]), wc(urls[1], fns[1])
#     bank_card, ltsale = loop.run_until_complete(asyncio.gather(*tasks))
#     loop.close()


def get_cache(fn):
    if os.path.isfile(fn):
        with open(fn, mode='r', errors='ignore', encoding='utf-8') as f:
            re = eval(f.read())
        return re


# async
async def wc(url):
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
    # await asyncio.
    sleep(40)
    tmp = browser.page_source
    browser.close()  # close tab not quit
    return tmp


async def par_limited_time_sale(fn, url):
    tmp = await wc(url)
    # tmp = wc(url)

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
    # Decimal
    keys = ['discount', 'prdname', 'href',
            'prdprice', 'g_price', 'g_discount']
    re = list(
        map(list, zip(discount, prdname, href, prdprice, g_price, g_discount)))
    re.sort(key=lambda e: e[0])
    re = [{keys[i]: _[i] for i in range(len(keys))} for _ in re]
    if len(re):  # 有抓到更新
        with open(fn, mode='w', errors='ignore', encoding='utf-8') as f:
            f.write(str(re))
    return re


#
async def par_bank(fn, url):
    tmp = await wc(url)
    # tmp = wc(url)

    tmp = BeautifulSoup(tmp, "html.parser")  # lxml
    bank = tmp.find('div', id='Area_bankList',
                    class_='Area_bankList').find('ul').find_all('li')
    bank_card = []
    for b in bank:
        bank_card.append({b.get('data-name'): []})
        for _ in b.find('div', class_='bankcard_group_box').find_all('p'):
            bank_card[-1][b.get('data-name')
                          ].append(list(_.stripped_strings))
    if len(bank_card):  # 有抓到更新
        with open(fn, mode='w', errors='ignore', encoding='utf-8') as f:
            f.write(str(bank_card))
    return bank_card


async def upd_cache():
    await par_limited_time_sale('cache_limited_sale.txt',
                          'https://www.momoshop.com.tw/main/Main.jsp')
    await par_bank('cache_bank.txt',
             'https://www.momoshop.com.tw/edm/cmmedm.jsp?lpn=O0Y2mh4ttZH&n=1&art_page=9')

    # # for "now" event
    # asyncio.set_event_loop(asyncio.new_event_loop())

    # loop = asyncio.get_event_loop()
    # tasks = par_limited_time_sale('https://www.momoshop.com.tw/main/Main.jsp'), par_bank(
    #     'https://www.momoshop.com.tw/edm/cmmedm.jsp?lpn=O0Y2mh4ttZH&n=1&art_page=9')
    # bank_card, ltsale = loop.run_until_complete(asyncio.gather(*tasks))
    # loop.close()


def home(request):
    template_name = 'app/home.html'
    # for "now" event
    # asyncio.set_event_loop(asyncio.new_event_loop())

    # loop = asyncio.get_event_loop()
    # tasks = bank(), limited_time_sale()
    # bank_card, ltsale = loop.run_until_complete(asyncio.gather(*tasks))
    # loop.close()
    bank_card = get_cache('cache_bank.txt')
    ltsale = get_cache('cache_limited_sale.txt')

    return render(request, template_name, locals())
