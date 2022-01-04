from django.db import models
from accounts.models import User


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name='کاربر')
    fullname = models.CharField(max_length=64, verbose_name='نام و نام خانوادگی')
    phone_number = models.CharField(max_length=18, verbose_name='شماره موبایل')
    province = models.CharField(max_length=32, verbose_name='استان')
    city = models.CharField(max_length=32, verbose_name='شهر')
    postal_address = models.TextField(max_length=500, verbose_name='آدرس دقیق')
    postal_code = models.CharField(max_length=32, verbose_name='کد پستی')
    is_active = models.BooleanField(default=True, verbose_name='فعال/غیر فعال')

    class Meta:
        verbose_name = 'آدرس'
        verbose_name_plural = 'آدرس ها'
        ordering = ('id', )

    def __str__(self):
        return self.fullname
