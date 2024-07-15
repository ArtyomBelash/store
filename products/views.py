from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, FormView

from .models import Product, Comment
from .forms import CommentForm
from basket.forms import BasketAddProductForm
from django.core.cache import cache


class ProductListView(ListView):
    model = Product
    template_name = 'products/index.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_queryset(self):
        products = cache.get('all_products')
        if not products:
            products = Product.objects.all().select_related('category').order_by('-updated')
            cache.set('all_products', products)
        return products


class ProductDetailView(DetailView, FormView):
    form_class = BasketAddProductForm
    model = Product
    slug_field = 'slug'
    context_object_name = 'product'
    template_name = 'products/detail.html'
    comment_form = CommentForm

    def get_object(self, queryset=None):
        product_detail = cache.get(f'product_detail_{self.kwargs["slug"]}')
        if not product_detail:
            product_detail = Product.objects.get(slug=self.kwargs['slug'])
            cache.set(f'product_detail_{self.kwargs["slug"]}', product_detail)
        return product_detail

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = self.comment_form()
        # context['comments'] = self.get_object().comments.order_by('-created_on').select_related()
        context['comments'] = Comment.objects.filter(product__slug=self.kwargs['slug']).order_by(
            '-created_on').select_related('author')
        return context

    @method_decorator(login_required(login_url='login'))
    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        comment_form = self.comment_form(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.product = obj
            comment.author = self.request.user
            comment.save()
            return self.form_valid(comment_form)
        else:
            return self.form_invalid(comment_form)

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER', 'detail')


class ProductsByCategoryListView(ListView):
    model = Product
    template_name = 'products/products_by_category.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_queryset(self):
        products = cache.get(f'{self.kwargs["slug"]}_products_by_category')
        if not products:
            products = Product.objects.select_related('category').filter(category__slug=self.kwargs['slug']).order_by(
                'name')
            cache.set(f'{self.kwargs["slug"]}_products_by_category', products)
        return products


class PopularProductsListView(ListView):
    model = Product
    template_name = 'products/popular_products.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_queryset(self):
        return Product.objects.annotate(total_quantity=Count('order_items__quantity')).order_by(
            '-total_quantity').select_related('category')
