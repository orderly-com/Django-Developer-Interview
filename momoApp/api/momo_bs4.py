# coding:utf-8
import json
import time
import requests
from bs4 import BeautifulSoup

from momoApp.models import MoMo


def sleeptime(hour, min, sec):
    return hour * 3600 + min * 60 + sec


def start():
    print("start")
    tStart = time.time()  # 計時開始

    headers = {
        'user-agent': '"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/47.0.2526.106 Safari/537.36'}
    response = requests.get("https://www.momoshop.com.tw/main/Main.jsp", headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")
    # print(soup.prettify())  # 輸出排版後的HTML內容

    data = soup.find('div', {'class': 'boxcontent'}, 'li').find_all('a')

    list_result = []
    for a in data:
        MoMo.objects.create(type='Test', title=a['title'])
        list_result.append(a['title'])
        # time.sleep(sleeptime(0, 1, 0))
    dict_result = {
        'title': list_result
    }

    tEnd = time.time()  # 計時結束
    print("It cost %f sec" % (tEnd - tStart))  # 會自動做近位

    return json.dumps(dict_result)
