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
    title = models.CharField(max_length=120, verbose_name='عنوان')
    english_title = models.CharField(max_length=120, verbose_name='عنوان به انگلیسی')
    slug = models.SlugField(max_length=120, allow_unicode=True, verbose_name='اسلاگ')

    class Meta:
        verbose_name = 'نوع محصول'
        verbose_name_plural = 'انواع محصولات'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("catalogue:main", args=[self.slug])


class Category(models.Model):
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, related_name='categories', verbose_name='نوع محصول')
    name = models.CharField(max_length=64, verbose_name='اسم')
    english_name = models.CharField(max_length=64, verbose_name='اسم به انگیسی')
    slug = models.SlugField(max_length=64, allow_unicode=True, verbose_name='اسلاگ')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True, verbose_name='دسته بندی والد')
    is_child = models.BooleanField(default=False, verbose_name='زیر مجموعه است/ نیست')

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalogue:product_list', args=[self.slug])


class Brand(models.Model):
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, related_name='brands', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='brands', verbose_name='دسته بندی')
    name = models.CharField(max_length=64, verbose_name='اسم')
    english_name = models.CharField(max_length=64, verbose_name='اسم به انگلیسی')
    slug = models.SlugField(max_length=64, allow_unicode=True, verbose_name='اسلاگ')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True, verbose_name='برند والد')
    is_child = models.BooleanField(default=False, verbose_name='زیر مجموعه است/ نیست')

    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برند ها'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalogue:product_list', args=[self.slug])


class Product(models.Model):
    title = models.CharField(max_length=120, verbose_name='عنوان')
    english_title = models.CharField(max_length=120, verbose_name='عنوان انگلیسی')
    slug = models.SlugField(max_length=120, allow_unicode=True, verbose_name='اسلاگ')
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, related_name='products', verbose_name='نوع محصول')
    upc = models.BigIntegerField(verbose_name='شماره اختصاصی')
    category = models.ManyToManyField(Category, related_name='products', verbose_name='دسته بندی')
    brand = models.ManyToManyField(Brand, related_name='products', blank=True, verbose_name='برند')
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات')
    discount = models.PositiveIntegerField(null=True, blank=True, verbose_name='تخفیف')
    special_sale = models.BooleanField(default=False, verbose_name='فروش ویژه')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ')
    modified = models.DateTimeField(auto_now=True, verbose_name='تاریخ اخرین تغییرات')
    is_active = models.BooleanField(default=True, verbose_name='فعال/غیر فعال')
    exist = models.BooleanField(default=True, verbose_name='وجود دارد/ندارد')

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
        ordering = ('-created', )

    default_manager = models.Manager()
    objects = ActiveManager()

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

    @staticmethod
    def filters(product_type):
        categories = product_type.categories.all()
        brands = product_type.brands.all()
        colors = ProductColor.objects.filter(product__product_type=product_type)
        data_filter = {"categories": None, "brands": None, "colors": None, "partners": None}
        if categories.exists():
            data_filter['categories'] = categories
        if brands.exists():
            data_filter['brands'] = brands
        if colors.exists():
            data_filter['colors'] = colors

        return data_filter


class Attribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attributes', verbose_name='محصول')
    title = models.CharField(max_length=120, verbose_name='عنوان')
    value = models.CharField(max_length=240, verbose_name='مقدار')

    class Meta:
        verbose_name = 'جزئیات'
        verbose_name_plural = 'جزیبات محصولات'

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='محصول')
    image = models.ImageField(upload_to='products/%Y/%m/%d/', verbose_name='تصویر')

    class Meta:
        verbose_name = 'تصویر محصول'
        verbose_name_plural = 'تصاویر محصولات'

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

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='colors', verbose_name='محصول')
    color = models.CharField(choices=COLOR_CHOICES, max_length=32, verbose_name='رنگ')

    class Meta:
        verbose_name = 'رنگ'
        verbose_name_plural = 'رنگ محصولات'

    def __str__(self):
        return f'{self.get_color_display()}'


class View(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='views', verbose_name='محصول')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='views', verbose_name='کاربر')

    class Meta:
        verbose_name = 'بازدید'
        verbose_name_plural = 'بازدید ها'

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
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sales', verbose_name='محصول')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET(get_user_sale), related_name='sales', verbose_name='کاربر')

    class Meta:
        verbose_name = 'فروش محصول'
        verbose_name_plural = 'فروش محصولات'


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
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sizes', verbose_name='محصول')
    value = models.PositiveSmallIntegerField(choices=PRODUCT_SIZE_CHOICES, default=L, verbose_name='مقدار')

    class Meta:
        verbose_name = 'سایز محصول'
        verbose_name_plural = 'سایز محصولات'

    def __str__(self):
        return f"{self.product} - {self.value}"


def get_user_view():
    user = User.objects.filter(username='view')
    if not user.exists():
        user = User.objects.create_user('view', 'sale@fake.com', 'where@view')
    return user[0]


class ProductFavorite(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorites', verbose_name='محصول')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites', verbose_name='کاربر')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ')

    class Meta:
        verbose_name = 'علاقه مندی'
        verbose_name_plural = 'علاقه مندی ها'
        ordering = ('-created', )

    def __str__(self):
        return f"{self.product} - {self.user}"
