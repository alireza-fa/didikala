from django.db import models
from django.conf import settings
from django.shortcuts import get_object_or_404
from accounts.models import User
from django.urls import reverse
from django.db.models import Avg, Count, Q


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True).prefetch_related('category', 'brand', 'product_type')


class ProductType(models.Model):
    title = models.CharField(max_length=120)
    english_title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120, allow_unicode=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("catalogue:main", args=[self.slug])


class Category(models.Model):
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=64)
    english_name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64, allow_unicode=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True)
    is_child = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalogue:product_list', args=[self.slug])


class Brand(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='brands')
    name = models.CharField(max_length=64)
    english_name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64, allow_unicode=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True)
    is_child = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalogue:product_list', args=[self.slug])


class Product(models.Model):
    title = models.CharField(max_length=120)
    english_title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120, allow_unicode=True)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, related_name='products')
    upc = models.BigIntegerField()
    category = models.ManyToManyField(Category, related_name='products')
    brand = models.ManyToManyField(Brand, related_name='products', blank=True)
    description = models.TextField(null=True, blank=True)
    discount = models.PositiveIntegerField(null=True, blank=True)
    special_sale = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    exist = models.BooleanField(default=True)

    default_manager = models.Manager()
    objects = ActiveManager()

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return self.title

    @classmethod
    def get_most_orders(cls, slug=None):
        if slug:
            return cls.objects.filter(Q(brand__slug=slug) | Q(category__slug=slug)).annotate(
                order_count=Count('order_items')
            ).order_by('-order_count').distinct()
        return cls.objects.all().annotate(
            order_count=Count('order_items')
        ).order_by('-order_count')

    def get_category(self):
        return self.category.last()

    def get_image(self):
        return self.images.all()[0]

    def get_images(self):
        return self.images.all()

    def get_image_slide(self):
        return self.images.all()[1:]

    def get_stock(self):
        try:
            price = self.stocks.all()[0]
            return price
        except:
            return None

    @classmethod
    def get_cheap(cls, slug=None):
        if slug:
            return cls.objects.filter(Q(brand__slug=slug) | Q(category__slug=slug)).annotate(
                price=Avg('stocks__price')
            ).order_by('price').distinct()
        return cls.objects.all().annotate(
            price=Avg('stocks__price')
        ).order_by('price')

    @classmethod
    def get_expensive(cls, slug=None):
        if slug:
            return cls.objects.filter(Q(brand__slug=slug) | Q(category__slug=slug)).annotate(
                price=Avg('stocks__price')
            ).order_by('-price').distinct()
        return cls.objects.all().annotate(
            price=Avg('stocks__price')
        ).order_by('-price')

    def get_absolute_url(self):
        return reverse('catalogue:product_detail', args=[self.slug])

    def get_attributes(self):
        return self.attributes.all()[:5]

    def get_rate(self):
        if not self.comments.filter(is_active=True):
            return None
        rate = self.comments.filter(is_active=True).aggregate(
            quality_avg=Avg('quality'),
            cost_avg=Avg('cost'),
            innovation_avg=Avg('innovation'),
            features_avg=Avg('features'),
            easiness_avg=Avg('easiness'),
            designing_avg=Avg('designing'),
        )
        for key, value in rate.items():
            rate[key] = round(value)
        return rate

    def get_total_rate(self):
        if not self.get_rate():
            return None
        rate = self.get_rate()
        rate['total_rate'] = sum((rate['quality_avg'], rate['cost_avg'], rate['innovation_avg'], rate['features_avg'],
                                  rate['easiness_avg'], rate['designing_avg'])) / 6
        rate['total_rate'] = round(rate['total_rate'])
        return rate['total_rate']

    def get_quality(self):
        if not self.comments.filter(is_active=True):
            return None
        rate = self.comments.filter(is_active=True).aggregate(quality_avg=Avg('quality'))
        return self.get_info_rate(round(rate['quality_avg']))

    def get_cost(self):
        if not self.comments.filter(is_active=True):
            return None
        rate = self.comments.filter(is_active=True).aggregate(cost_avg=Avg('cost'))
        return self.get_info_rate(round(rate['cost_avg']))

    def get_innovation(self):
        if not self.comments.filter(is_active=True):
            return None
        rate = self.comments.filter(is_active=True).aggregate(innovation_avg=Avg('innovation'))
        return self.get_info_rate(round(rate['innovation_avg']))

    def get_features(self):
        if not self.comments.filter(is_active=True):
            return None
        rate = self.comments.filter(is_active=True).aggregate(features_avg=Avg('features'))
        return self.get_info_rate(round(rate['features_avg']))

    def get_easiness(self):
        if not self.comments.filter(is_active=True):
            return None
        rate = self.comments.filter(is_active=True).aggregate(easiness_avg=Avg('easiness'))
        return self.get_info_rate(round(rate['easiness_avg']))

    def get_designing(self):
        if not self.comments.filter(is_active=True):
            return None
        rate = self.comments.filter(is_active=True).aggregate(designing_avg=Avg('designing'))
        return self.get_info_rate(round(rate['designing_avg']))

    def get_info_rate(self, rate):
        info = dict()
        if rate == 1:
            info['info'] = 'خیلی بد'
            info['percent'] = 16
        elif rate == 2:
            info['info'] = 'بد'
            info['percent'] = 32
        elif rate == 3:
            info['info'] = 'معمولی'
            info['percent'] = 50
        elif rate == 4:
            info['info'] = 'خوب'
            info['percent'] = 75
        elif rate == 5:
            info['info'] = 'عالی'
            info['percent'] = 100
        return info

    def get_questions(self):
        return self.questions.filter(is_active=True)

    def product_comments(self):
        return self.comments.filter(is_active=True)

    def product_view(self):
        return self.views.aggregate(
            views=Count('id')
        )

    @classmethod
    def regular_by_view(cls, slug=None):
        if slug:
            return cls.objects.filter(Q(brand__slug=slug) | Q(category__slug=slug)).annotate(
                view=Count('views__id')
            ).order_by('-view').distinct()

        return cls.objects.all().annotate(
            view=Count('views__id')
        ).order_by('-view')


class Attribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attributes')
    title = models.CharField(max_length=120)
    value = models.CharField(max_length=240)

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/%Y/%m/%d/')

    def __str__(self):
        return f"{self.product} - {self.id}"


class ProductColor(models.Model):
    BLUE = '#2196f3'
    WHITE = '#f6f6f6'
    BLACK = '#212121'
    RED = '#FF0000'
    PINK = '#FFC0CB'
    ORANGE = '#FFA500'
    YELLOW = '#FFFF00'

    COLOR_CHOICES = (
        (BLUE, 'آبی'),
        (WHITE, 'سفید'),
        (BLACK, 'مشکلی'),
        (RED, 'قرمز'),
        (PINK, 'صورتی'),
        (ORANGE, 'نارنجی'),
        (YELLOW, 'زرد')
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='colors')
    color = models.CharField(choices=COLOR_CHOICES, max_length=32)

    def __str__(self):
        return f'{self.get_color_display()}'


class View(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='views')

    def __str__(self):
        return f"{self.product} - {self.user}"

    @staticmethod
    def save_vote(user, slug):
        product = get_object_or_404(Product, slug=slug)
        like = product.views.filter(user=user)
        if like.exists():
            return like
        like = View(product=product, user=user)
        like.save()
        return like


def get_user_sale():
    user = User.objects.filter(username='sale')
    if not user.exists():
        user = User.objects.create_user('sale', 'sale@fake.com', 'where@sale')
    return user[0]


class ProductSale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sales')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET(get_user_sale), related_name='sales')


class ProductSize(models.Model):
    S = 1
    M = 2
    L = 3
    XL = 4
    XXL = 5
    L_XL = 6
    PRODUCT_SIZE_CHOICES = (
        (S, "S"),
        (M, "M"),
        (L, "L"),
        (XL, "XL"),
        (XXL, "XXL"),
        (L_XL, "L-XL")
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sizes')
    value = models.PositiveSmallIntegerField(choices=PRODUCT_SIZE_CHOICES, default=L)

    def __str__(self):
        return f"{self.product} - {self.value}"


def get_user_view():
    user = User.objects.filter(username='view')
    if not user.exists():
        user = User.objects.create_user('view', 'sale@fake.com', 'where@view')
    return user[0]


class ProductFavorite(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorites')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return f"{self.product} - {self.user}"
