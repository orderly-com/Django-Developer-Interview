from django.db.models import Count
from django.db.models.functions import Concat
from rest_framework.response import Response
from rest_framework.views import APIView

from momoapp.models import LimitTimeSale


class DuplicateLimitTimeSaleAPIView(APIView):

    def get(self, request, format=None):
        data = LimitTimeSale.objects.values(name=Concat('brand', 'title'))\
            .annotate(count=Count('id'))\
            .filter(count__gt=1)

        return Response(data)

