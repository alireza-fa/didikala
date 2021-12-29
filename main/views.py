import random
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.http import require_GET
from cart.cart import Cart
from catalogue.models import Product


@require_GET
def home_page(request):
    special_products = Product.objects.filter(special_sale=True)[:6]
    we_suggest = Product.objects.filter(special_sale=True)
    discounts = Product.objects.filter(discount__gte=20)[:6]
    order_products = Product.get_most_orders()[:6]
    products = Product.objects.all()
    if products.exists():
        random_product = set(random.choices(products, k=4))
    else:
        random_product = None
    return render(request, 'main/home.html', {
        "special_products": special_products, "discounts": discounts, "we_suggest": we_suggest,
        "order_products": order_products, "random_product": random_product})


def navbar_partial(request):
    cart = Cart(request)
    count = len(cart.cart)
    return render(request, 'shared/navbar.html', {"cart": cart, "count": count})


def search_up(request):
    print(request.POST)
    keyup = request.POST['keyup']
    if len(keyup) > 2:
        products = Product.objects.filter(Q(title__icontains=keyup) | Q(description__icontains=keyup))
    else:
        products = None
    t = render_to_string('main/ajax/search.html', {"search_result": products})
    return JsonResponse({'data': t}, safe=False)
