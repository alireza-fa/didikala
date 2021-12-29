from django.urls import path
from django.views.generic.base import TemplateView
from . import views


app_name = 'main'
urlpatterns = [
    path('', views.home_page, name='home'),
    path('navbar_partial/', views.navbar_partial, name='navbar_partial'),
    path('search_up/', views.search_up, name='search_up'),
]
