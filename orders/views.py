from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET
from suds import Client
from cart.cart import Cart
from orders.models import Order, OrderItem


@login_required
@require_GET
def shopping(request):
    if not request.session['cart']:
        return redirect('cart:cart_detail')
    cart = Cart(request)
    count = len(cart.cart)
    active_address = request.user.addresses.filter(is_active=True, user=request.user)
    disable_addresses = request.user.addresses.filter(is_active=False, user=request.user)
    if active_address.exists():
        active_address = active_address[0]
    return render(
        request, 'orders/shopping.html', {"cart": cart, "address": active_address,
                                          "addresses": disable_addresses, "count": count})


@login_required
def order_detail(request, order_id):
    global order_global
    order = get_object_or_404(Order, id=order_id)
    order_global = order
    return render(request, 'orders/detail.html', {"order": order})


@login_required
@require_GET
def order_create(request):
    cart = Cart(request)
    order = Order.objects.create(user=request.user)
    for item in cart:
        OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
        cart.clear()
        cart = Cart(request)
    return redirect('shopping:order_detail', order.id)


MERCHANT = '70d96859-b496-4e56-a71d-0c4b10ea3d05'
client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
description = "پرداخت دیدی کالا"
mobile = '09123456789'
CallbackURL = 'http://localhost:8787/shopping/verify/'


@login_required
@require_GET
def payment(request):
    if request.user.phone_number:
        result = client.service.PaymentRequest(MERCHANT, order_global.get_total_price(), description, request.user.email,
                                               request.user.phone_number, CallbackURL)
    else:
        result = client.service.PaymentRequest(MERCHANT, order_global.get_total_price(), description, request.user.email,
                                               mobile, CallbackURL)
    if result.Status == 100:
        return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
    else:
        return render(request, 'orders/failed_pay.html')


@login_required
@require_GET
def verify(request):
    if not order_global.user == request.user:
        return render(request, 'orders/failed_pay.html')
    if request.GET.get('Status') == 'OK':
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], order_global.get_total_price())
        if result.Status == 100:
            order_global.paid = True
            order_global.save()
            return redirect('shop:home')
        elif result.Status == 101:
            return render(request, 'orders/success_pay.html', {"order": order_global})
        else:
            return render(request, 'orders/failed_pay.html', {"order": order_global})
    else:
        return render(request, 'orders/failed_pay.html', {"order": order_global})
