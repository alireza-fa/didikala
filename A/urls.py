"""A URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static as static_local
from django.conf import settings
from django.views.static import serve
import django.views.static
from django.conf.urls import url

urlpatterns = [
    path('wheredad123/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('catalogue/', include('catalogue.urls')),
    path('comment/', include('comment.urls')),
    path('shipping/', include('shipping.urls')),
    path('cart/', include('cart.urls')),
    path('shopping/', include('orders.urls')),
    path('', include('main.urls', namespace='main')),
]
if settings.DEBUG:
    urlpatterns += static_local(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static_local(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if not settings.DEBUG:
    urlpatterns += url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})
    urlpatterns += url(r'^static/(?P<path>.*)$', django.views.static.serve, {'document_root': settings.STATIC_ROOT,
                                                                             'show_indexes': settings.DEBUG})
