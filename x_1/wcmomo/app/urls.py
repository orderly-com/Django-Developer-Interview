# Michael
# from django.contrib import admin
from django.urls import path
# from django.conf.urls import include
from .views import home
urlpatterns = [
    path('', home, name='Home'),
]
