from django.shortcuts import render
from .models import PromotionFramework
from .api.views import PromotionListView

def list_view(request):
    queryset = PromotionFramework.objects.order_by('title','title_hash').values('title','title_hash').distinct()
    return render(request, 'templates/Promotion/list.html', {'list': queryset})

def detail_view(request, id):
    return render(request, 'Promotion/detail.html', {'detail_id': id})
