from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from accounts.managers import UserManager
from django.db.models import Sum
import os


def get_filename(filename):
    base = os.path.basename(filename)
    name, ext = os.path.splitext(base)
    return name, ext


def upload_image_to(instance, filename):
    name, ext = get_filename(filename)
    return f'/{instance.id}{ext}'


class User(AbstractBaseUser):
    username = models.CharField(max_length=32, unique=True, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True, unique=True)
    first_name = models.CharField(max_length=32, null=True, blank=True)
    last_name = models.CharField(max_length=32, null=True, blank=True)
    fullname = models.CharField(max_length=64, null=True, blank=True)
    code_melli = models.CharField(max_length=20, null=True, blank=True)
    card_number = models.CharField(max_length=20, null=True, blank=True)
    received_news = models.BooleanField(default=False)
    phone_number = models.BigIntegerField(null=True, blank=True, unique=True)
    image = models.ImageField(upload_to='profiles/%Y/%m/%d/', null=True, blank=True)
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    city = models.CharField(max_length=32, null=True, blank=True)
    foreign_person = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    REQUIRED_FIELDS = ('email', )
    objects = UserManager()

    def __str__(self):
        return str(self.id)

    def has_perm(self, perms, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def get_total_score(self):
        scores = self.scores.all().aggregate(
            count=Sum('score')
        )
        return scores['count']


class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scores')
    score = models.IntegerField()

    def __str__(self):
        return f"{self.user} - {self.score}"

    class Meta:
        ordering = ('-user', )


class UserMassage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='massages')
    subject = models.CharField(max_length=120)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created', )
