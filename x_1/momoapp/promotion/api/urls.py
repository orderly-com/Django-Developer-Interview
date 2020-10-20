from django.conf.urls import url, include
from rest_framework import routers
from . import views
from django.urls import re_path,path

router = routers.DefaultRouter()
router.register('promotion', views.PromotionViewSet)

urlpatterns = [
    url(r'^Promotion/$', views.PromotionListView.as_view(), name='Promotion_list_api'),
    url(r'^Promotion/(?P<pk>\d+)/$', views.PromotionDetailView.as_view(), name='Promotion_detail_api'),
    url(r'^PromotionDetail/(?P<pk>\d+)/$', views.PromotionDetail.as_view(), name='Promotion_list_detail_api'),
    url(r'^', include(router.urls), name='Promotion_route_api'),

    # path('PromotionDetail/<int:year>', views.PromotionDetail.as_view()),
]