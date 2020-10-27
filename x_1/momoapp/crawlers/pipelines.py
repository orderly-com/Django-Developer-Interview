# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from promotion.models import PromotionFramework
import threading
from .spider import spiders
from django.shortcuts import render, HttpResponse
import hashlib, base64
import zlib

def celeryTask(request=None):
    t = threading.Thread(target=Run)
    t.start()
    print('celeryTask done')
    return HttpResponse('done')

def Run():
    t = threading.Thread(target=spiders)
    t.start()
    t.join()

    items = spiders.list
    try:
        for item in items:
            th = zlib.adler32(item['title'].encode('utf-8'))
            promotion = PromotionFramework()
            promotion.cnid = item['id']
            promotion.title = item['title']
            promotion.title_hash = th
            promotion.url = item['url']
            promotion.content = item['article']

            existed = PromotionFramework.objects.filter(cnid=item['id'])
            if not existed:
                promotion.save()

        print('Promotion already exist')
    except Exception as e:
        print(e)