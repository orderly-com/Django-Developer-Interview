# coding:utf-8
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore

from momoApp.api.momo_bs4 import start

scheduler = BackgroundScheduler()

try:
    scheduler.add_jobstore(DjangoJobStore(), "default")

    scheduler.add_job(
        func=start,
        trigger='interval',
        seconds=10,
        start_date='2021-01-29 20:27:00',
        end_date='2021-01-29 20:28:00'
    )

    scheduler.start()
except Exception as e:
    print(e)
    scheduler.shutdown()
