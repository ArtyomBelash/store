from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .services import create_order, create_stripe_session
from .forms import OrderForm
from .models import Order
from basket.basket import Basket

class OrderCreateView(CreateView):
    form_class = OrderForm
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'
    success_url = reverse_lazy('products')

    def form_valid(self, form):
        order = create_order(self.request, form)
        stripe_session_url = create_stripe_session(self.request, order)
        return redirect(stripe_session_url, code=303)

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


class PaymentCompeted(TemplateView):
    template_name = 'orders/thanks.html'


class PaymentCanceled(TemplateView):
    template_name = 'orders/canceled.html'
