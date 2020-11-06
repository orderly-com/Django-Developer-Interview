from django.db import models

STATUS = (
    (0, 'Crawling'),
    (1, 'New'),
    (2, 'Expired')
)


class Category(models.Model):
    category_id = models.IntegerField()
    name = models.CharField(max_length=20)
    url = models.URLField(max_length=200)
    status = models.IntegerField(choices=STATUS, default=0)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Commodity(models.Model):
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 limit_choices_to={'status': '1'},
                                 related_name='commoditys')

    title = models.CharField(max_length=200)
    price = models.CharField(max_length=10)
    discount_type = models.CharField(max_length=10)
    url = models.URLField(max_length=200)
    status = models.IntegerField(choices=STATUS, default=0)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
