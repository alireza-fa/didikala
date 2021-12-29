from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from django.views.decorators.http import require_GET
from catalogue.models import Product


def cart_detail(request):
    cart = Cart(request)
    if cart.cart:
        return render(request, 'cart/cart_detail.html', {"cart": cart, "count": (len(cart.cart.keys()))})
    else:
        return render(request, 'cart/cart_empty.html')


@require_GET
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product)
    return redirect('catalogue:product_detail', product.slug)


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')
