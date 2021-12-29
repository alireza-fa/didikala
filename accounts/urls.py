from django.contrib.auth.views import LogoutView
from django.urls import path
from django.views.generic import TemplateView

from . import views


app_name = 'accounts'
urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.user_register, name='register'),
    path('welcome/', views.user_welcome, name='welcome'),
    path('profile/', views.user_profile, name='profile'),
    path('profile/change_password/', views.user_change_password, name='user_change_password'),
    path('profile/info/', views.personal_info, name='info'),
    path('profile/additional/', views.profile_additional, name='profile_additional'),
    path('privacy/', TemplateView.as_view(template_name='accounts/privacy.html'), name='privacy'),
    path('reset/', views.UserPassReset.as_view(), name='reset_pass'),
    path('reset/done/', views.PasswordResetDone.as_view(), name='password_reset_done'),
    path('confirm/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('confirm/done/', views.PasswordResetComplete.as_view(), name='password_reset_complete'),
    path('profile/history/', views.ProfileHistory.as_view(), name='profile_history'),
    path('profile/history/delete/<int:product_id>', views.history_delete, name='history_delete'),
    path('profile/favorite/', views.ProfileFavorite.as_view(), name='profile_favorite'),
    path('profile/favorite/delete/<int:product_id>/', views.favorite_delete, name='favorite_delete'),
    path('profile/comment/', views.ProfileComment.as_view(), name='profile_comment'),
    path('profile/comment/delete/<int:comment_id>/', views.comment_delete, name='comment_delete'),
    path('profile/address/', views.profile_address, name='profile_address'),
    path('profile/order/', views.profile_order, name='profile_order'),
    path('profile/order/return/', views.profile_order_return, name='profile_order_return'),
    path('profile/order/detail/<int:order_id>/', views.profile_order_detail, name='profile_order_detail'),
]
