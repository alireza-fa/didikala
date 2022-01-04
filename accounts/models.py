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
    username = models.CharField(max_length=32, unique=True, null=True, blank=True, verbose_name='نام کاربری')
    email = models.EmailField(max_length=100, null=True, blank=True, unique=True, verbose_name='ایمیل')
    first_name = models.CharField(max_length=32, null=True, blank=True, verbose_name='نام')
    last_name = models.CharField(max_length=32, null=True, blank=True, verbose_name='نام خانوادگی')
    fullname = models.CharField(max_length=64, null=True, blank=True, verbose_name='نام و نام خانوادگی')
    code_melli = models.CharField(max_length=20, null=True, blank=True, verbose_name='کد ملی')
    card_number = models.CharField(max_length=20, null=True, blank=True, verbose_name='شماره حساب')
    received_news = models.BooleanField(default=False, verbose_name='عضویت در خبرنامه')
    phone_number = models.BigIntegerField(null=True, blank=True, unique=True, verbose_name='شماره موبایل')
    image = models.ImageField(upload_to='profiles/%Y/%m/%d/', null=True, blank=True, verbose_name='تصویر')
    age = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='سن')
    city = models.CharField(max_length=32, null=True, blank=True, verbose_name='شهر')
    foreign_person = models.BooleanField(default=False, verbose_name='تبعه خارجی')

    USERNAME_FIELD = 'username'
    is_active = models.BooleanField(default=True, verbose_name='کاربر فعال/غیر فعال')
    is_admin = models.BooleanField(default=False, verbose_name='مدیر')
    REQUIRED_FIELDS = ('email', )
    objects = UserManager()

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scores', verbose_name='کاربر')
    score = models.IntegerField(verbose_name='امتیاز')

    def __str__(self):
        return f"{self.user} - {self.score}"

    class Meta:
        ordering = ('-user', )


class UserMassage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='massages', verbose_name='کاربر')
    subject = models.CharField(max_length=120, verbose_name='موضوع')
    body = models.TextField(verbose_name='متن')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ پیام')

    class Meta:
        ordering = ('-created', )
