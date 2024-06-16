import stripe
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from decimal import Decimal
from .tasks import order_created
from .forms import *
from .models import *
from basket.basket import Basket
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET


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
        self.request.session['order_id'] = order.id
        success_url = self.request.build_absolute_uri(reverse('completed'))
        cancel_url = self.request.build_absolute_uri(reverse('canceled'))
        session_data = {
            'mode': 'payment',
            'client_reference_id': order.id,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': []
        }
        for item in order.items.all():
            session_data['line_items'].append({
                'price_data': {
                    'unit_amount': int(item.price * Decimal('100')),
                    'currency': 'byn',
                    'product_data': {
                        'name': item.product.name,
                    },
                },
                'quantity': item.quantity,
            })
        session = stripe.checkout.Session.create(**session_data)
        # order.paid = True
        # order.save()
        return redirect(session.url, code=303)
        # return render(self.request, 'orders/thanks.html', {'order': order})

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


# @csrf_exempt
# def get_stripe_webhook(request):
#     wb = stripe.WebhookEndpoint.create(
#         enabled_events=["charge.succeeded", "charge.failed"],
#         url="http://127.0.0.1:8000/order/webhook/",
#     )
#     return wb

@csrf_exempt
def stripe_webhook(request):
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    print(sig_header)
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload=request.body,
            sig_header=sig_header,
            secret=endpoint_secret
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
    if event.type == 'checkout.session.completed':
        session = event.data.object
        if session.mode == 'payment' and session.payment_status == 'paid':
            try:
                order = Order.objects.get(id=session.client_reference_id)
            except Order.DoesNotExist:
                return HttpResponse(status=404)
            order.paid = True
            order.stripe_id = session.payment_intent
            order.save()
    return HttpResponse(status=200)


def payment_completed(request):
    return render(request, 'orders/thanks.html')


def payment_canceled(request):
    return render(request, 'orders/canceled.html')
