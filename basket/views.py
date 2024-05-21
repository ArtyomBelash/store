from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, DetailView

from products.models import Product
from .basket import Basket
from .forms import BasketAddProductForm


class AddProductsBasketView(FormView):
    form_class = BasketAddProductForm
    success_url = reverse_lazy('basket_detail')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_object(self):
        return get_object_or_404(Product, slug=self.kwargs['slug'])

    def form_valid(self, form):
        product = self.get_object()
        basket = Basket(self.request)
        basket.add(product=product,
                   quantity=form.cleaned_data['quantity'],
                   update_quantity=form.cleaned_data['update'])
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class BasketRemoveView(View):

    def get(self, *args, **kwargs):
        basket = Basket(self.request)
        product = get_object_or_404(Product, slug=self.kwargs['slug'])
        basket.remove(product)
        return redirect('basket_detail')


class BasketDetailView(DetailView):
    model = Basket
    template_name = 'basket/detail.html'
    context_object_name = 'basket'

    def get_object(self, queryset=None):
        obj = Basket(self.request)
        return obj
