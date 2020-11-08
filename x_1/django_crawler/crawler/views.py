from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from django.views.decorators.http import require_http_methods

from crawler.models import Commodity
from crawler.models import Category

import csv


def home_page(request):
    category_list = Category.objects.filter(status='1')

    return render(request, 'home.html', {'category_list': category_list})


def commodity_api_page(request, category_id):
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(['title', 'price', 'discount_type', 'url'])

    commodity_list = list(Category.objects.filter(
                              category_id=category_id,
                              status=1
                          )[0].commoditys.all().values())

    if 'start' in request.GET and 'end' in request.GET:
        commodity_num = len(commodity_list)
        start = int(request.GET['start'])
        end = int(request.GET['end'])

        if end > commodity_num:
            commodity_list = commodity_list[start:commodity_num]
        elif start > commodity_num:
            commodity_list = []
        else:
            commodity_list = commodity_list[start:end]
 
    for commodity in commodity_list:
        title = commodity['title']
        price = commodity['price']
        discount_type = commodity['discount_type']
        url = commodity['url']

        writer.writerow([title, price, discount_type, url])

    return response
