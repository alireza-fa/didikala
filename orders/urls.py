from django.urls import path
from . import views


app_name = 'shopping'
urlpatterns = [
    path('', views.shopping, name='shopping'),
    path('create/', views.order_create, name='order_create'),
    path('detail/<int:order_id>', views.order_detail, name='order_detail'),
    path('payment/', views.payment, name='payment'),
    path('verify/', views.verify, name='verify'),
]
