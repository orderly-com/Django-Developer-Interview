from django.contrib import admin
from crawler.models import Commodity
from crawler.models import Category


class CommodityAdmin(admin.ModelAdmin):
    list_display = ['title',
                    'category',
                    'price',
                    'discount_type',
                    'status',
                    'created_on']

    list_filter = ['category', 'discount_type', 'status']


admin.site.register(Commodity, CommodityAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_id', 'name', 'url', 'status', 'created_on']
    list_filter = ['status']

admin.site.register(Category, CategoryAdmin)
