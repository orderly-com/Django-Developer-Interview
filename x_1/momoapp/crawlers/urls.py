from django.conf.urls import url
from . import pipelines

urlpatterns = [
    url(r'^celerytask/$', pipelines.celeryTask, name='celerytask'),
]