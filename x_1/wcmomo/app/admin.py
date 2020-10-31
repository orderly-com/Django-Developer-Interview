from django.contrib import admin


# admin.site.register(Bank_card)
# admin.site.register(Bank_card, Bank_cardAdmin)
from .models import Bank_card
from .models import Limited_time_sale


# for filter
# https://github.com/silentsokolov/django-admin-rangefilter/blob/master/rangefilter/filter.py
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter


@admin.register(Bank_card)
class Bank_cardAdmin(admin.ModelAdmin):
    list_display = [
        f.name
        for f in Bank_card._meta.fields
        if f.name not in ['id']
    ]
    list_filter = [
        ('par_time', DateTimeRangeFilter),
        'bank_name'
    ]
    date_hierarchy = 'par_time'
    list_per_page = 15


@admin.register(Limited_time_sale)
class Limited_time_saleAdmin(admin.ModelAdmin):
    list_display = ['prdname', 'g_discount', 'g_prdprice', 'par_time']
    list_filter = [
        ('par_time', DateTimeRangeFilter),
        # 'g_discount',
        # 'g_prdprice'
    ]
    date_hierarchy = 'par_time'
    list_per_page = 15
