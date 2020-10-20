from rest_framework import generics, viewsets
from ..serializers import PromotionFrameworkSerializer,RawStateSerializer
from ..models import PromotionFramework
from rest_framework.response import Response
from rest_framework.views import APIView

class PromotionListView(generics.ListAPIView):
    queryset = PromotionFramework.objects.order_by('title','title_hash').values('title','title_hash').distinct()
    serializer_class = RawStateSerializer

class PromotionDetailView(generics.RetrieveAPIView):
    queryset = PromotionFramework.objects.all().order_by('-publish_date')
    print(queryset)
    serializer_class = PromotionFrameworkSerializer

class PromotionDetail(APIView):
    def get(self, request, *args, **kwargs):
        print(kwargs['pk'])
        queryset = PromotionFramework.objects.filter(title_hash=kwargs['pk']).order_by('-publish_date')
        # serializer_class = PromotionFrameworkSerializer
        print(queryset)
        ser = PromotionFrameworkSerializer(queryset,many=True)
        print(ser.data)
        return Response(ser.data)

class PromotionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PromotionFramework.objects.all().order_by('-publish_date')
    serializer_class = PromotionFrameworkSerializer