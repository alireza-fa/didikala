from django.contrib import admin
from .models import Comment, ProductQuestion


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'subject', 'created', 'is_active')
    # list_filter = ('created', 'is_active')
    search_fields = ('user', 'created')


@admin.register(ProductQuestion)
class ProductQuestionAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'is_child', 'is_active', 'created')
    list_filter = ('created', 'is_active')
    search_fields = ('name', 'product__title', 'created')
