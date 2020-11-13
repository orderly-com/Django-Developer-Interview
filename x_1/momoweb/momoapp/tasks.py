import json
import re
from datetime import datetime, date
from re import sub

import demjson
import pytz
import requests
from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta
from fake_useragent import UserAgent

from momoapp.models import LimitTimeSale, BankDiscount


def datetime_format(dt, d_format, time_type=None):
    dt = datetime.strptime(dt, d_format)
    tw = pytz.timezone('Asia/Taipei')
    tw_dt_now = tw.localize(datetime.now())
    dt = dt.replace(year=tw_dt_now.year)
    dt = tw.localize(dt)

    if dt.month == 1 and tw_dt_now.month == 12:
        dt = dt + relativedelta(years=1)
    if time_type == 'end':
        dt = dt + relativedelta(seconds=59)

    return dt


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)


def parse_limited_time_sale():
    url = 'https://www.momoshop.com.tw/ajax/promotionEvent_CustExclbuy.jsp'
    ua = UserAgent()
    headers = {
        'user-agent': ua.random
    }
    post_data = {'showType': '1'}
    res = requests.post(url, headers=headers, data=post_data)
    html = res.text.strip()
    soup = BeautifulSoup(html, 'lxml')
    sale_block = soup.find_all(class_='MENTAL')
    limit_time_sale_list = []
    for sale in sale_block:
        limit_time = sale.find(class_='period').find('span').text
        begin_time, end_time = limit_time.split('~')
        begin_time = datetime_format(begin_time, d_format="%m/%d %H:%M")
        end_time = datetime_format(end_time, d_format="%m/%d %H:%M", time_type='end')

        last_item = LimitTimeSale.objects.last()
        if begin_time <= last_item.begin_time:
            continue

        product_list = sale.find('ul', class_='product_Area').find_all('li')
        for product in product_list:
            brand = product.find('div', class_='brand').text
            title = product.find('div', class_='brand2').text
            old_price = product.find('div', class_='oldPrice').text
            discount = product.find('div', class_='discount').find('span').text
            if len(discount) == 1:
                discount = int(discount) / 10
            elif len(discount) == 2:
                discount = int(discount) / 100
            else:
                discount = None  # 異常
            new_price = product.find('div', class_='price').text
            new_price = sub(r'[^\d.]', '', new_price).replace(',', '')

            data = {
                'begin_time': begin_time,
                'end_time': end_time,
                'brand': brand,
                'title': title,
                'old_price': int(old_price),
                'discount': discount,
                'new_price': int(new_price),
            }

            limit_time_sale_list.append(LimitTimeSale(**data))

    LimitTimeSale.objects.bulk_create(limit_time_sale_list)


def parse_bank_discount():
    url = 'https://www.momoshop.com.tw/edm/cmmedm.jsp?lpn=O0Y2mh4ttZH'
    ua = UserAgent()
    headers = {
        'user-agent': ua.random
    }
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')

    bank_info_url = ''
    for script in soup.find_all('script', {"src": True}):
        if 'bankjs_list' in script.get('src'):
            bank_info_url = 'https:' + script.get('src')
            break
    res = requests.get(bank_info_url, headers=headers)

    begin_text = '<!-- -----------------------------------------------↓總覽↓入稿貼語法從這邊開始' \
                 '----------------------------------------------- -->'
    end_text = '<!-- -----------------------------------------------↑總覽↑入稿貼語法到這邊結束' \
               '----------------------------------------------- -->'
    date_row_data = re.findall(f"button:\t\'詳情 / 登錄\'(.*?){begin_text}", res.text, re.DOTALL)[0]
    date_row_data = re.sub(r'\r|\n|\t|,', '', date_row_data)
    match = re.search(r'(\d+/\d+)-(\d+/\d+)', date_row_data)
    begin_date = datetime_format(match.group(1), d_format="%m/%d").date()
    end_date = datetime_format(match.group(2), d_format="%m/%d").date()

    last_item = BankDiscount.objects.last()
    if begin_date <= last_item.begin_date:
        pass

    else:
        bank_raw_data = re.findall(f'{begin_text}(.*?){end_text}', res.text, re.DOTALL)[0]
        bank_raw_data = re.sub(r'//.*|\r|\n|\t|\u3000', '', bank_raw_data)
        data = demjson.decode(f'{{{bank_raw_data}}}')
        bank_discount_info_list = []
        for bank in data.values():
            bank_name = bank.get('name')
            for info in bank.get('group'):
                bank_data = {
                    'bank_name': bank_name,
                    'discount_date': info[1],
                    'condition': info[2],
                    'discount': info[3],
                    'begin_date': begin_date,
                    'end_date': end_date
                }
                bank_discount_info_list.append(BankDiscount(**bank_data))
        BankDiscount.objects.bulk_create(bank_discount_info_list)
