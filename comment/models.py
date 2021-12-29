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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    subject = models.CharField(max_length=120)
    positive_point = models.CharField(max_length=500, null=True, blank=True)
    negative_point = models.CharField(max_length=500, null=True, blank=True)
    body = models.TextField()
    suggest = models.PositiveSmallIntegerField(choices=SUGGEST_CHOICES, default=NO_IDEA)
    quality = models.PositiveSmallIntegerField(choices=COMMENT_CHOICES, default=NORMAL)
    cost = models.PositiveSmallIntegerField(choices=COMMENT_CHOICES, default=NORMAL)
    innovation = models.PositiveSmallIntegerField(choices=COMMENT_CHOICES, default=NORMAL)
    features = models.PositiveSmallIntegerField(choices=COMMENT_CHOICES, default=NORMAL)
    easiness = models.PositiveSmallIntegerField(choices=COMMENT_CHOICES, default=NORMAL)
    designing = models.PositiveSmallIntegerField(choices=COMMENT_CHOICES, default=NORMAL)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        ordering = ('modified', )

    def __str__(self):
        return self.subject

    def get_total_rate(self):
        total_rate = sum(
            (self.quality, self.cost, self.innovation, self.features, self.easiness, self.designing)
        )
        return round(total_rate / 6)


class ProductQuestion(models.Model):
    name = models.CharField(max_length=64, default='ناشناس')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='questions')
    question = models.TextField()
    notify = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_child = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
