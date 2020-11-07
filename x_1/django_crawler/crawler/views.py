from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from crawler.models import Commodity
from crawler.models import Category

import csv


def home_page(request):
    category_list = Category.objects.filter(status='1')

    return render(request, 'home.html', {'category_list': category_list})

def commodity_api_page(request, category_id):
    response = HttpResponse(content_type='text/csv')

    #commodity_list = list(Commodity.objects.all()[1:100].values())
    #commodity_list = list(Commodity.objects.all().values())
    commodity_list = list(Category.objects.filter(
                              category_id=category_id,
                              status=1
                          )[0].commoditys.all().values())

    writer = csv.writer(response)
    writer.writerow(['title', 'price', 'discount_type', 'url'])

    for commodity in commodity_list:
        title = commodity['title']
        price = commodity['price']
        discount_type = commodity['discount_type']
        url = commodity['url']

        writer.writerow([title, price, discount_type, url])

    return response
