from django.urls import path
from . import views


app_name = 'comment'
urlpatterns = [
    path('product/add_comment/<int:product_id>/', views.comment_add, name='comment_add'),
    # path('product/add_question/<int:product_id>/', views.question_add, name='question_add'),
]
