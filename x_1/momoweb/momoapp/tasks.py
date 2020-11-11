import json
from datetime import datetime, date
from re import sub

import pytz
import requests
from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta
from fake_useragent import UserAgent

from momoapp.models import LimitTimeSale


def datetime_format(dt, time_type=None):
    dt = datetime.strptime(dt, "%m/%d %H:%M")
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
        begin_time = datetime_format(begin_time)
        end_time = datetime_format(end_time, time_type='end')

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
