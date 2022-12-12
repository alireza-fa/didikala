from django.urls import path, re_path
from . import views


app_name = 'catalogue'
urlpatterns = [
    path('filter_tab/', views.filter_tab, name='filter_tab'),
    path('filters/', views.filters, name='filters'),
    path('main/<str:slug>/', views.Main.as_view(), name='main'),
    path('search/<str:slug>/', views.ProductList.as_view(), name='product_list'),
    path('product/discount/', views.ProductDiscount.as_view(), name='product_discount'),
    path('product/most_orders/', views.ProductMostOrder.as_view(), name='product_order'),
    path('product/search/', views.ProductSearch.as_view(), name='product_search'),
    path('product/<str:slug>/', views.ProductDetail.as_view(), name='product_detail'),
    path('favorite/', views.favorite, name='favorite'),
    path('no_favorite/', views.no_favorite, name='no_favorite'),
]
