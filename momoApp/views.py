from django.http import HttpResponse
from django.views import View

from momoApp.api.momo_bs4 import start
from momoApp.api.scheduler import scheduler


def view_bs4(request):
    return HttpResponse(start())


# class view_momo(View):
#     def get(self, request):
#         pass
