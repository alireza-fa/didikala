from django.db import models
from catalogue.models import Product


class Partner(models.Model):
    name = models.CharField(max_length=120, verbose_name='اسم')
    description = models.TextField(verbose_name='توضیحات')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ')
    modified = models.DateTimeField(auto_now=True, verbose_name='تاریخ تغییرات')

    class Meta:
        verbose_name = 'فروشنده'
        verbose_name_plural = 'فروشندگان'

    def __str__(self):
        return self.name


class PartnerStock(models.Model):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='stocks', verbose_name='فروشنده')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stocks', verbose_name='محصول')
    price = models.BigIntegerField(verbose_name='قیمت')

    class Meta:
        verbose_name = 'قیمت فروشنده'
        verbose_name_plural = 'قیمت فروشندگان'
        ordering = ('price', )

    def __str__(self):
        return f"{self.partner} >> {self.price}"
