from django.db import models


# Create your models here.
class LimitTimeSale(models.Model):
    begin_time = models.DateTimeField()
    end_time = models.DateTimeField()
    brand = models.TextField()
    title = models.TextField()
    old_price = models.IntegerField()
    discount = models.FloatField(null=True)
    new_price = models.IntegerField()

    class Meta:
        unique_together = ['begin_time', 'end_time', 'brand', 'title']

    def __str__(self):
        return f'{self.brand} -- {self.title}'


class BankDiscount(models.Model):
    bank_name = models.CharField(max_length=100)
    discount_date = models.CharField(max_length=100)
    condition = models.CharField(max_length=100)
    discount = models.CharField(max_length=100)
    begin_date = models.DateField()
    end_date = models.DateField()
