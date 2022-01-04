from django.db import models
from accounts.models import User
from catalogue.models import Product


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name='کاربر')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ')
    modified = models.DateTimeField(auto_now=True, verbose_name='تاریخ تغییرات')
    paid = models.BooleanField(default=False, verbose_name='پرداخت شده/نشده')

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'
        ordering = ('-created', )

    def __str__(self):
        return f'{self.user} - {self.pk}'

    def get_total_price(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='سفارش')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items', verbose_name='محصول')
    price = models.PositiveIntegerField(verbose_name='قیمت')
    quantity = models.PositiveSmallIntegerField(default=1, verbose_name='تعداد')

    class Meta:
        verbose_name = 'آیتم سفارش'
        verbose_name_plural = 'آیتم سفارشات'

    def __str__(self):
        return f"{self.order} - {self.product}"

    def get_cost(self):
        return self.price * self.quantity
