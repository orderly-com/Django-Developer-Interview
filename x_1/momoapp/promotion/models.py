from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone

# Create your models here.
class PromotionFramework(models.Model):
    cnid = models.IntegerField()
    title = models.CharField(max_length=120)
    title_hash = models.IntegerField()
    slug = models.CharField(max_length=100, unique=True)
    publish_date = models.DateTimeField(default=timezone.now)
    url = models.CharField(max_length=1024, blank=True, null=True)
    content = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'promotion'
        ordering = ('publish_date',)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.publish_date)
        super(PromotionFramework, self).save(*args, **kwargs)