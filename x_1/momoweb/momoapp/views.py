from django.db.models import Count
from django.db.models.functions import Concat
from rest_framework.response import Response
from rest_framework.views import APIView

from momoapp.models import LimitTimeSale, BankDiscount


class DuplicateLimitTimeSaleAPIView(APIView):

    def get(self, request, format=None):
        data = LimitTimeSale.objects.values(name=Concat('brand', 'title')) \
            .annotate(count=Count('id')) \
            .filter(count__gt=1)

        return Response(data)


class BankDiscountFilter(APIView):

    def get(self, request, format=None):
        data = BankDiscount.objects.values_list('begin_date', flat=True).order_by('-begin_date').distinct()
        return Response(data)


class BankDiscountAPIView(APIView):

    def get(self, request, format=None):
        params = request.query_params
        year = params.get('year')
        month = params.get('month')
        if year and month:
            data = BankDiscount.objects.filter(
                begin_date__year=params['year'],
                begin_date__month=params['month']
            ).values('bank_name', 'discount_date', 'condition', 'discount')
        else:
            last_date = list(BankDiscount.objects.values_list('begin_date', flat=True).distinct())[-1]
            data = BankDiscount.objects.filter(begin_date=last_date)\
                .values('bank_name', 'discount_date', 'condition', 'discount')

        return Response(data)
