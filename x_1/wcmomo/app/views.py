import os
from pathlib import Path
from django.shortcuts import render


from .tasks import par_bank, par_limited_time_sale
from django_q.models import Schedule


BASE_DIR = Path(__file__).resolve().parent.parent  # -> projname/projname/


def get_cache(fn):
    if os.path.isfile(fn):
        with open(fn, mode='r', errors='ignore', encoding='utf-8') as f:
            re = eval(f.read())
        return re


def home(request):
    template_name = 'app/home.html'

    bank_card = get_cache(BASE_DIR/'cache_bank.txt')
    ltsale = get_cache(BASE_DIR/'cache_limited_sale.txt')

    if not Schedule.objects.filter(func='app.tasks.par_limited_time_sale').exists():
        Schedule.objects.create(func='app.tasks.par_limited_time_sale',
                                schedule_type='I',  # M(I)nutes
                                minutes=3,
                                )

    if not Schedule.objects.filter(func='app.tasks.par_bank').exists():
        Schedule.objects.create(func='app.tasks.par_bank',
                                schedule_type='I',  # M(I)nutes
                                minutes=3,
                                )

    return render(request, template_name, locals())
