from django.contrib import admin
from .models import PromotionFramework

class RegNewsModelAdmin(admin.ModelAdmin):
    # display attributes in admin page
    list_display = ['id','cnid', 'title', 'title_hash','publish_date', 'created', 'read']
    # filter list
    list_filter = ('read','cnid', 'title_hash', 'created', 'publish_date')
    # search by *
    search_fields = ('title','title_hash' ,'content')
    ordering = ['publish_date', 'read']

admin.site.register(PromotionFramework, RegNewsModelAdmin)