from django.db import models


class MoMo(models.Model):
    type = models.CharField(u'type', max_length=50)
    title = models.CharField(u'Title', max_length=50)

    def __unicode__(self):
        return self.title
