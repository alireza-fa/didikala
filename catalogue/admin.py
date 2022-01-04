from django.contrib import admin
from .models import Category, Brand, Product, Attribute, ProductImage, ProductColor, ProductType, \
    ProductSize, ProductFavorite, View


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('title', )
    search_fields = ('title', )
    prepopulated_fields = {"slug": ('english_title', )}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('product_type', 'name', 'is_child')
    list_filter = ('is_child', 'product_type')
    search_fields = ('product_type__title', 'name', 'english_name')
    prepopulated_fields = {"slug": ('english_name',)}
    raw_id_fields = ('product_type', 'parent')


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'parent', 'is_child')
    search_fields = ('name', 'category__name', 'parent__name')
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
    list_display = ('title', 'product_type', 'is_active', 'exist', 'created', 'modified')
    list_filter = ('product_type', 'is_active', 'exist', 'created')
    search_fields = ('title', 'product_type__title')
    prepopulated_fields = {"slug": ('english_title', )}
    raw_id_fields = ('category', 'brand', 'product_type')


@admin.register(ProductFavorite)
class ProductFavorite(admin.ModelAdmin):
    pass


@admin.register(View)
class ProductViewAdmin(admin.ModelAdmin):
    pass
