import datetime
from django_q.models import Schedule
from .tasks import par_bank, par_limited_time_sale
from django_q.tasks import async_task

import os
from pathlib import Path
from django.shortcuts import render


Path(__file__).resolve().parent.parent


def get_cache(fn):
    if os.path.isfile(fn):
        with open(fn, mode='r', errors='ignore', encoding='utf-8') as f:
            re = eval(f.read())
        return re


def add_task():
    pass
    Schedule.objects.create(name='par_bank',
                            func='app.tasks.par_bank',
                            # schedule_type=Schedule.HOURLY,
                            repeats=1,
                            next_run=datetime.datetime.now()
                            )

    Schedule.objects.create(name='par_limited_time_sale',
                            func='app.tasks.par_limited_time_sale',
                            # schedule_type=Schedule.HOURLY,
                            repeats=1,
                            next_run=datetime.datetime.now()
                            )


def home(request):
    template_name = 'app/home.html'

    bank_card = get_cache('cache_bank.txt')
    ltsale = get_cache('cache_limited_sale.txt')

    par_bank()
    par_limited_time_sale()

    # add_task()
    return render(request, template_name, locals())
