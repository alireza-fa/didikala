from django.contrib import admin
from .models import Comment, ProductQuestion


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductQuestion)
class ProductQuestionAdmin(admin.ModelAdmin):
    pass
