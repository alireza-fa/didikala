from django.urls import path
from . import views


app_name = 'shipping'
urlpatterns = [
    path('address/add/', views.add_address, name='add_address'),
    path('address/edit/<int:address_id>/', views.edit_address, name='edit_address'),
    path('address/edit/save/', views.edit_address_save, name='edit_address_save'),
    path('address/delete/<int:address_id>/', views.delete_address, name='delete_address'),
    path('address/active_address/<int:address_id>/', views.active_address, name='active_address'),
    path('address/change_active_address/<int:address_id>/', views.change_active_address, name='change_active_address'),
]
