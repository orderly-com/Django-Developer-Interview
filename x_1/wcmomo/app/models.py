from django.db import models


class Bank_card(models.Model):
    bank_name = models.CharField(verbose_name='銀行名稱', max_length=100)
    date = models.CharField(verbose_name='活動期間', max_length=100)
    suffice = models.CharField(verbose_name='活動條件', max_length=100)
    discount = models.CharField(verbose_name='折扣方式', max_length=100)
    par_time = models.DateTimeField(
        verbose_name='爬取時間', auto_now_add=True)
    # alive = models.BooleanField(verbose_name='活動', default=True)

    class Meta:
        ordering = ['bank_name']

    # def __str__(self):
    #     return "???"


class Limited_time_sale(models.Model):
    href = models.URLField(verbose_name='網址')
    imgsrc = models.URLField(verbose_name='圖片網址')
    prdname = models.CharField(verbose_name='商品名稱', max_length=100)
    discount = models.CharField(verbose_name='折數', max_length=100)
    g_discount = models.IntegerField(verbose_name='% off')
    prdprice = models.CharField(verbose_name='$售價', max_length=100)
    g_prdprice = models.IntegerField(verbose_name='售價')
    par_time = models.DateTimeField(
        verbose_name='爬取時間', auto_now_add=True)

    class Meta:
        ordering = ['g_prdprice']
