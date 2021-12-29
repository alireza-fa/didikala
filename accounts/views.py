from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth import views as auth_views
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_GET
from catalogue.models import Product, ProductFavorite, View
from orders.models import Order
from shipping.models import Address
from .forms import UserLoginForm, UserRegistrationForm, UserChangePasswordForm, ProfileAdditionalForm, \
    UserPasswordResetForm, UserPasswordResetConfirmForm
from django.contrib import messages
from comment.models import Comment


@user_passes_test(lambda u: not u.is_authenticated, login_url='accounts:logout')
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            done = form.login(request)
            if done:
                return redirect('main:home')
            else:
                messages.warning(request, 'اطلاعات وارد شده صحیح نمیباشد. لطفا با دفت بیشتری وارد کنید', 'warning')
                return redirect('accounts:login')

    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {"form": form})


@user_passes_test(lambda u: not u.is_authenticated, login_url='accounts:logout')
def user_register(request):

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(request)
            return redirect('accounts:welcome')

    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {"form": form})


@require_GET
@login_required
def user_welcome(request):
    return render(request, 'accounts/welcome.html')


@require_GET
@login_required
def user_profile(request):
    favorites = request.user.favorites.all()[:3]
    orders = request.user.orders.all()[:3]
    return render(request, 'accounts/profile.html', {'favorites': favorites, "orders": orders})


@login_required
def user_change_password(request):
    if request.method == 'POST':
        form = UserChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            form.clean_password()
            check = form.check_pass()
            if not check:
                messages.warning(request, 'پسورد جدید و تکرار پسورد با هم تطابق ندارند😵', 'warning')
                return redirect('accounts:user_change_password')
            user = form.save(request, cd['password1'])
            if user:
                messages.success(request, 'پسورد شما با موفقیت تغییر کرد')
                return redirect('accounts:login')

    else:
        form = UserChangePasswordForm()
    return render(request, 'accounts/user_change_password.html', {"form": form})


@require_GET
@login_required
def personal_info(request):
    return render(request, 'accounts/personal_info.html')


@login_required
def profile_additional(request):
    if request.method == 'POST':
        form = ProfileAdditionalForm(user=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            user = form.save(request.user)
            try:
                user.image = request.FILES['image']
            except:
                pass
            user.save()
            return redirect('accounts:profile')

    else:
        form = ProfileAdditionalForm(initial={
            "first_name": request.user.first_name, "fullname": request.user.fullname,
            "code_melli": request.user.code_melli, "phone_number": request.user.phone_number,
            "email": request.user.email, "card_number": request.user.card_number,
            "foreign_person": request.user.foreign_person, "shared_news": request.user.received_news
        })
    return render(request, 'accounts/profile_additional_info.html', {"form": form})


class UserPassReset(auth_views.PasswordResetView):
    form_class = UserPasswordResetForm
    template_name = 'accounts/password_reset_form.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    email_template_name = 'accounts/password_reset_email.html'


class PasswordResetDone(auth_views.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class PasswordResetConfirm(auth_views.PasswordResetConfirmView):
    form_class = UserPasswordResetConfirmForm
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class PasswordResetComplete(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'


class ProfileHistory(ListView):
    model = Product
    template_name = 'accounts/profile_history.html'

    @method_decorator(login_required, )
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset().filter(views__user=self.request.user)
        return qs[::-1][:8]


def history_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    history = get_object_or_404(View, product=product, user=request.user)
    history.delete()
    return redirect('accounts:profile_history')


class ProfileFavorite(ListView):
    model = Product
    template_name = 'accounts/profile_favorite.html'

    @method_decorator(login_required, )
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset().filter(favorites__user=self.request.user)
        return qs[::-1][:8]


@login_required
@require_GET
def favorite_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    favorite = get_object_or_404(ProductFavorite, product=product, user=request.user)
    favorite.delete()
    return redirect('accounts:profile_favorite')


class ProfileComment(ListView):
    model = Comment
    template_name = 'accounts/profile_comment.html'

    @method_decorator(login_required, )
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset().filter(user=self.request.user)
        return qs


@login_required
@require_GET
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    comment.delete()
    return redirect('accounts:profile_comment')


@login_required
@require_GET
def profile_address(request):
    addresses = Address.objects.filter(user=request.user)
    return render(request, 'accounts/profile_address.html', {"addresses": addresses})


@login_required
def profile_order(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'accounts/orders.html', {"orders": orders})


@login_required
def profile_order_detail(request, order_id):
    return render(request, 'accounts/order_detail.html')


@login_required
def profile_order_return(request):
    return render(request, 'accounts/profile_orders_return.html')
