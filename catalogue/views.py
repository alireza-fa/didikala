from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from catalogue.models import Product, ProductFavorite, View
from comment.forms import QuestionForm
from comment.models import ProductQuestion
from django.http import JsonResponse
from django.core.paginator import Paginator

from partner.models import Partner


class Main(ListView):
    model = Product
    paginate_by = 25
    template_name = 'catalogue/search.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(product_type__slug=self.kwargs['slug'], is_active=True)

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(*args, object_list=None, **kwargs)
        context['no_filter'] = True
        if context['object_list'].exists():
            product_type = context['object_list'].first().product_type
            context['filters'] = Product.filters(product_type)
            partners = Partner.objects.filter(stocks__product__product_type=product_type).distinct()
            if partners.exists():
                context['filters']['partners'] = partners
        return context


class ProductList(ListView):
    model = Product
    paginate_by = 25
    template_name = 'catalogue/search.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(
            Q(brand__slug=self.kwargs['slug']) | Q(category__slug=self.kwargs['slug'], is_active=True)).distinct()

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(*args, object_list=None, **kwargs)
        context['slug'] = self.kwargs['slug']
        if context['object_list'].exists():
            product_type = context['object_list'].first().product_type
            context['filters'] = Product.filters(product_type)
            partners = Partner.objects.filter(stocks__product__product_type=product_type).distinct()
            if partners.exists():
                context['filters']['partners'] = partners
        return context


class ProductDetail(FormMixin, DetailView):
    model = Product
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    template_name = 'catalogue/product_detail.html'
    form_class = QuestionForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            View.save_vote(user=self.request.user, slug=self.kwargs['slug'])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

    def get_success_url(self):
        return reverse('catalogue:product_detail', kwargs={"slug": self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(product_type=self.object.product_type.id)[:6]
        if self.request.user.is_authenticated:
            favorite = self.object.favorites.filter(user=self.request.user)
            if favorite.exists():
                context['favorite'] = True
            else:
                context['favorite'] = False
        return context

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            self.object = self.get_object()
            form = self.get_form()
            if form.is_valid():
                cd = form.cleaned_data
                question = ProductQuestion(user=request.user, product=self.object, name=cd['name'], question=cd['body'])
                if cd['notify']:
                    question.notify = cd['notify']
                question.save()
            return super().form_valid(form)


@login_required
def favorite(request):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=request.POST.get('product_id'))
        user_favorite = ProductFavorite.objects.filter(product=product, user=request.user)
        if user_favorite.exists():
            return JsonResponse({"status": 'bad'})
        pf = ProductFavorite(product=product, user=request.user)
        pf.save()
        return JsonResponse({"status": 'ok'})


@login_required
def no_favorite(request):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=request.POST.get('product_id'))
        user_favorite = ProductFavorite.objects.filter(product=product, user=request.user)
        if user_favorite.exists():
            user_favorite.delete()
            return JsonResponse({"status": 'ok'})
        return JsonResponse({"status": 'bad'})


class ProductDiscount(ListView):
    model = Product
    paginate_by = 25
    template_name = 'catalogue/search.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(discount__gte=1)


class ProductSearch(ListView):
    model = Product
    paginate_by = 25
    template_name = 'catalogue/search.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(Q(title__icontains=self.request.GET.get('q')) | Q(description__icontains=self.request.GET.get('q')))


@require_GET
def product_search(request):
    print(request.GET.get('q'))


class ProductMostOrder(ListView):
    model = Product
    paginate_by = 25
    template_name = 'catalogue/search.html'

    def get_queryset(self):
        return Product.get_most_orders()


@require_http_methods(request_method_list=['GET', 'POST'])
def filter_tab(request):

    def paginator(query):
        pagination = Paginator(query, 50)
        page_number = request.GET.get('page')
        return pagination.get_page(page_number)

    if request.POST.get('filter_tab') == 'relation':
        slug = request.POST['page_obj']
        qs = Product.objects.filter(Q(brand__slug=slug) | Q(category__slug=slug)).distinct()
        page_obj = paginator(qs)
        t = render_to_string('catalogue/ajax/product.html', {"page_obj": page_obj})
        return JsonResponse({"data": t}, safe=False)

    elif request.POST.get('filter_tab') == 'view':
        qs = Product.regular_by_view(slug=request.POST['page_obj'])
        page_obj = paginator(qs)
        t = render_to_string('catalogue/ajax/product.html', {"page_obj": page_obj})
        return JsonResponse({"data": t}, safe=False)

    elif request.POST.get('filter_tab') == 'new':
        slug = request.POST['page_obj']
        qs = Product.objects.filter(Q(brand__slug=slug) | Q(category__slug=slug)).distinct()
        page_obj = paginator(qs)
        t = render_to_string('catalogue/ajax/product.html', {"page_obj": page_obj})
        return JsonResponse({"data": t}, safe=False)

    elif request.POST.get('filter_tab') == 'sale':
        qs = Product.get_most_orders(request.POST['page_obj'])
        page_obj = paginator(qs)
        t = render_to_string('catalogue/ajax/product.html', {"page_obj": page_obj})
        return JsonResponse({"data": t}, safe=False)

    elif request.POST.get('filter_tab') == 'cheap':
        qs = Product.get_cheap(request.POST['page_obj'])
        page_obj = paginator(qs)
        t = render_to_string('catalogue/ajax/product.html', {"page_obj": page_obj})
        return JsonResponse({"data": t}, safe=False)

    elif request.POST.get('filter_tab') == 'expensive':
        qs = Product.get_expensive(request.POST['page_obj'])
        page_obj = paginator(qs)
        t = render_to_string('catalogue/ajax/product.html', {"page_obj": page_obj})
        return JsonResponse({"data": t}, safe=False)


@require_http_methods(request_method_list=['POST', 'GET'])
def filters(request):
    categories = request.POST.getlist('category[]')
    brands = request.POST.getlist('brand[]')
    partners = request.POST.getlist('partner[]')
    colors = request.POST.getlist('color[]')
    product_type = request.POST.get('product_type_id')
    products = Product.objects.prefetch_related('category', 'brand', 'product_type').filter(product_type=product_type)

    if request.POST.get('is_active') and request.POST.get('is_active') == 'true':
        products = products.filter(is_active=True).distinct()
    if categories:
        if 'all' not in categories:
            products = products.filter(category__id__in=categories).distinct()
    if brands:
        if 'all' not in brands:
            products = products.filter(brand__id__in=brands).distinct()
    if partners:
        if 'all' not in partners:
            products = products.filter(stocks__partner__id__in=partners).distinct()
    if colors:
        if 'all' not in colors:
            products = products.filter(colors__id__in=colors).distinct()

    def paginator(query):
        pagination = Paginator(query, 50)
        page_number = request.GET.get('page')
        return pagination.get_page(page_number)

    page_obj = paginator(products)
    t = render_to_string('catalogue/ajax/product.html', {"page_obj": page_obj})
    return JsonResponse({"data": t}, safe=False)
