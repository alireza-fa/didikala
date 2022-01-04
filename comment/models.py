from django.db import models
from accounts.models import User
from catalogue.models import Product


class Comment(models.Model):
    VERY_BAD = 1
    BAD = 2
    NORMAL = 3
    GOOD = 4
    VERY_GOOD = 5

    SUGGEST = 1
    NO_SUGGEST = 2
    NO_IDEA = 3

    SUGGEST_CHOICES = (
        (SUGGEST, 'توصیه میکنم'),
        (NO_SUGGEST, 'توصیه نمیکنم'),
        (NO_IDEA, 'نظری ندارم'),
    )

    COMMENT_CHOICES = (
        (VERY_BAD, 'خیلی بد'),
        (BAD, 'بد'),
        (NORMAL, 'نرمال'),
        (GOOD, 'خوب'),
        (VERY_GOOD, 'خیلی خوب')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='کاربر')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', verbose_name='محصول')
    subject = models.CharField(max_length=120, verbose_name='موضوع')
    positive_point = models.CharField(max_length=500, null=True, blank=True, verbose_name='نقاط قوت')
    negative_point = models.CharField(max_length=500, null=True, blank=True, verbose_name='نقاط ضعف')
    body = models.TextField(verbose_name='متن')
    suggest = models.PositiveSmallIntegerField(choices=SUGGEST_CHOICES, default=NO_IDEA, verbose_name='موضوع')
    quality = models.PositiveSmallIntegerField(choices=COMMENT_CHOICES, default=NORMAL, verbose_name='کیفیت')
    cost = models.PositiveSmallIntegerField(choices=COMMENT_CHOICES, default=NORMAL, verbose_name='قسمت')
    innovation = models.PositiveSmallIntegerField(choices=COMMENT_CHOICES, default=NORMAL, verbose_name='نو آوری')
    features = models.PositiveSmallIntegerField(choices=COMMENT_CHOICES, default=NORMAL, verbose_name='امکانات')
    easiness = models.PositiveSmallIntegerField(choices=COMMENT_CHOICES, default=NORMAL, verbose_name='سهولت در استفاده')
    designing = models.PositiveSmallIntegerField(choices=COMMENT_CHOICES, default=NORMAL, verbose_name='طراحی')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت نظر')
    modified = models.DateTimeField(auto_now=True, verbose_name='تاریخ تغییر نظر')
    is_active = models.BooleanField(default=False, verbose_name='فغال/غیر فعال')

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'
        ordering = ('modified', )

    def __str__(self):
        return self.subject

    def get_total_rate(self):
        total_rate = sum(
            (self.quality, self.cost, self.innovation, self.features, self.easiness, self.designing)
        )
        return round(total_rate / 6)


class ProductQuestion(models.Model):
    name = models.CharField(max_length=64, default='ناشناس', verbose_name='اسم')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions', verbose_name='کاربر')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='questions', verbose_name='محصول')
    question = models.TextField(verbose_name='سوال')
    notify = models.BooleanField(default=False, verbose_name='اعلن بازخورد/اعلان ندارد')
    is_active = models.BooleanField(default=False, verbose_name='فعال/ غیر فعال')
    is_child = models.BooleanField(default=False, verbose_name='بازخور')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ')

    class Meta:
        verbose_name = 'سوال'
        verbose_name_plural = 'سوالات'
        ordering = ('-created', )

    def __str__(self):
        return self.name
