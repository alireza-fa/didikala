from django.db import models
from catalogue.models import Product


class Partner(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class PartnerStock(models.Model):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='stocks')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stocks')
    price = models.BigIntegerField()

    class Meta:
        ordering = ('price', )

    def __str__(self):
        return f"{self.partner} >> {self.price}"
