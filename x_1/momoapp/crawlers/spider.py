from bs4 import BeautifulSoup
import requests
import time

class spiders:
    date = time.strftime("%Y/%m/%d")
    RootUrl = 'https://m.momoshop.com.tw/'
    URL = 'https://m.momoshop.com.tw/events.momo'
    list = []
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/86.0.4240.75 Safari/537.36'
    }

    def __init__(self):
        resp = requests.get(self.URL,headers=self.headers)
        soup = BeautifulSoup(resp.text, 'html.parser')
        # print(soup)
        articles = soup.find('article','moreprdsArea').select('a')
        for article in articles:
            print('id: ' + article['href'].split('cn=')[1])
            print('url: ' + self.RootUrl + article['href'])
            print('title: ' + article.text.strip().split('\xa0>\xa0')[0])
            print('article: ' + article.text.strip().split('\xa0>\xa0')[1])
            print('=================================================')

            self.list.append({
                'id':article['href'].split('cn=')[1],
                'url':self.RootUrl + article['href'],
                'title':article.text.strip().split('\xa0>\xa0')[0],
                'article':article.text.strip().split('\xa0>\xa0')[1],
            })