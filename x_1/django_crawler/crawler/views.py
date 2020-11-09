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


def category_quantity_api_page(request):
    response = dict()
    response['data'] = list()

    category_list = Category.objects.filter(status=1)

    for category in category_list:
        quantity_data = dict()
        quantity_data['category_id'] = category.category_id
        quantity_data['name'] = category.name
        quantity_data['value'] = category.commoditys.all().count()

        response['data'].append(quantity_data)

    return JsonResponse(response)


def category_price_api_page(request):
    price_range = 500
    column_list = list()

    response = dict()
    response['data'] = list()
    response_range = response['range'] = list()

    category_list = Category.objects.filter(status=1)

    for category in category_list:
        price_data = dict()
        price_data['name'] = category.name
        price_data['category_id'] = category.category_id

        commodity_list =  category.commoditys.all()

        for commodity in commodity_list:
            price = int(commodity.price.replace(',', ''))

            min_range = price - (price%price_range)
            max_range = min_range + price_range - 1

            _range = '{}-{}'.format(min_range, max_range)

            if not _range in column_list:
                column_list.append(_range)

            if not _range in price_data:
                price_data[_range] = 0
            else:
                price_data[_range] = price_data[_range] + 1
        response['data'].append(price_data)

    response['range'] = column_list


    return JsonResponse(response)
