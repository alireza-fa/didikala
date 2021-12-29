from django.db import models
from accounts.models import User


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    fullname = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=18)
    province = models.CharField(max_length=32)
    city = models.CharField(max_length=32)
    postal_address = models.TextField(max_length=500)
    postal_code = models.CharField(max_length=32)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('id', )

    def __str__(self):
        return self.fullname
