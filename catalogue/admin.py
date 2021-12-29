from django.contrib import admin
from .models import Category, Brand, Product, Attribute, ProductImage, ProductColor, ProductType, \
    ProductSize, ProductFavorite, View


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('english_title', )}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('english_name',)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('english_name', )}


class AttributeInline(admin.StackedInline):
    model = Attribute
    extra = 3


class ProductImageInline(admin.StackedInline):
    model = ProductImage


class ProductColorInline(admin.StackedInline):
    model = ProductColor
    extra = 1


class ProductSizeInline(admin.StackedInline):
    model = ProductSize
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = (AttributeInline, ProductImageInline, ProductColorInline, ProductSizeInline)
    prepopulated_fields = {"slug": ('english_title', )}
    raw_id_fields = ('category', 'brand', 'product_type')


@admin.register(ProductFavorite)
class ProductFavorite(admin.ModelAdmin):
    pass


@admin.register(View)
class ProductViewAdmin(admin.ModelAdmin):
    pass
