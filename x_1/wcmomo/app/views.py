import os

from django.shortcuts import render

from .models import Bank_card
from .models import Limited_time_sale

import json
from django.core import serializers
from django.forms.models import model_to_dict
from django_q.models import Schedule


from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent  # -> projname/projname/


def get_cache(fn):
    if os.path.isfile(fn):
        with open(fn, mode='r', errors='ignore', encoding='utf-8') as f:
            re = json.load(f)
        return re


def obj_to_dict(model_instance):
    serial_obj = serializers.serialize('json', [model_instance])
    obj_as_dict = json.loads(serial_obj)[0]['fields']
    obj_as_dict['pk'] = model_instance.pk
    return obj_as_dict


def home(request):
    template_name = 'app/home.html'

    tmp = Limited_time_sale.objects.all()
    ltsale = []
    for _ in tmp:
        _ = model_to_dict(_, fields=['href', 'imgsrc', 'prdname', 'discount',
                                     'g_discount', 'prdprice', 'g_prdprice'])
        # 給JS(瀏覽器)處理
        # _['g_discount'] = int(_['g_discount'])
        # _['g_prdprice'] = int(_['g_prdprice'])
        ltsale.append(_)
    if not len(ltsale):
        ltsale = get_cache(BASE_DIR/'cache_limited_sale.json')

    bank_card = Bank_card.objects.all()
    if not len(bank_card):
        bank_card = get_cache(BASE_DIR/'cache_bank_card.json')

    if not Schedule.objects.filter(func='app.tasks.par_limited_time_sale').exists():
        Schedule.objects.create(func='app.tasks.par_limited_time_sale',
                                schedule_type='I',  # M(I)nutes
                                minutes=3,
                                )

    if not Schedule.objects.filter(func='app.tasks.par_bank_card').exists():
        Schedule.objects.create(func='app.tasks.par_bank_card',
                                schedule_type='I',  # M(I)nutes
                                minutes=3,
                                )

    return render(request, template_name, locals())
