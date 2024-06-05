from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .tasks import order_created
from .forms import *
from .models import *
from basket.basket import Basket


class OrderCreateView(CreateView):
    form_class = OrderForm
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'
    success_url = reverse_lazy('products')

    def form_valid(self, form):
        basket = Basket(self.request)
        new_order = Order.objects.create(name=form.cleaned_data.get('name'),
                                         surname=form.cleaned_data.get('surname'),
                                         phone=form.cleaned_data.get('phone'),
                                         email=form.cleaned_data.get('email'),
                                         address=form.cleaned_data.get('address'))
        order = Order.objects.get(pk=new_order.pk)
        for i in basket:
            ItemInOrder.objects.create(order=order,
                                       product=i['product'],
                                       price=i['price'],
                                       quantity=i['quantity'])
        basket.clear()
        order_created.delay(order.pk)
        return render(self.request, 'orders/thanks.html', {'order': order})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['basket'] = Basket(self.request)
        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
