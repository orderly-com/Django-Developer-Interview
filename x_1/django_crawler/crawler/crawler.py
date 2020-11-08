import requests
import asyncio
import time

from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from crawler.models import Commodity
from crawler.models import Category

loop = asyncio.get_event_loop()
ua = UserAgent()


def assignment_group(_list, step):
    return [_list[i:i+step] for i in range(0,len(_list),step)]


def get_request(url):
    headers = {'user-agent': ua.random}
    while True:
        try:
            res = requests.get(url, headers=headers, timeout=10)
            return res
        except:
            time.sleep(10)


def get_category():
    category_data_list = list()
    home_url = 'https://www.momoshop.com.tw/main/Main.jsp'
    res = get_request(home_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    category_list = soup.select('.menuList .ulli')

    category_id = 0

    for category in category_list:
        category_group = category.select('a')
        category_name = "".join([str(_category.text) for _category in category_group])

        url = category_group[0].get('href')

        category_data = [category_name, url]
        category_data_list.append(category_data)

        Category.objects.create(category_id=category_id,
                                name=category_name,
                                url=url)

        category_id = category_id + 1

    return category_data_list


async def get_commodity(category, url):
    discount_type_list = ['SALE', 'CPHOT']
    for discount_type in discount_type_list:
        discount_url = '{}&{}=Y&flag=L'.format(url, discount_type)

        res = await loop.run_in_executor(None, get_request, discount_url)
        soup = BeautifulSoup(res.text, 'html.parser')
        page_el = soup.select('.pageArea.topEnPageArea')[0]
        page_number = page_el.select('a')[-1].get('page')
        page_list = list(range(1, int(page_number)+1))

        for page in page_list:
            page_url = '{}&pageNum={}'.format(discount_url, page)
            res = await loop.run_in_executor(None, get_request, page_url)
            soup = BeautifulSoup(res.text, 'html.parser')
            commodity_data_list = soup.select('.eachGood')

            for commodity_data in commodity_data_list:
                title = commodity_data.select('.prdName')[0].get('title')
                #price = commodity_data.select('.prdPrice.bsprdPrice')[0].select('b')[0].text
                price = commodity_data.select('.prdPrice')[0].select('b')[0].text

                main_url = 'https://www.momoshop.com.tw'
                commodity_url = main_url + commodity_data.select('a')[0].get('href')

                #print('Title: {}, Price: {}, Url: {}'.format(title, price, commodity_url))
                _category = Category.objects.filter(name=category, status='0')

                while True:
                    try:
                        _category[0].commoditys.create(
                            title=title,
                             price=price,
                             discount_type=discount_type,
                             url=commodity_url
                        )
                        break
                    except:
                        time.sleep(1)


def crawl():
    tasks = list()
    category_list_group = assignment_group(get_category(), 5)

    for category_list in category_list_group:
        for category_data in category_list:
            category, url = category_data

            task = loop.create_task(get_commodity(category, url))
            tasks.append(task)

        loop.run_until_complete(asyncio.wait(tasks))

    Commodity.objects.filter(status='1').update(status='2')
    Commodity.objects.filter(status='0').update(status='1')

    Category.objects.filter(status='1').update(status='2')
    Category.objects.filter(status='0').update(status='1')


if __name__ == '__main__':
        crawl()