import stripe
from django.conf import settings
from django.urls import reverse
from decimal import Decimal
from .models import Order, ItemInOrder
from basket.basket import Basket

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


def create_order(request, form) -> Order:
    basket = Basket(request)
    new_order = Order.objects.create(
        name=form.cleaned_data.get('name'),
        surname=form.cleaned_data.get('surname'),
        phone=form.cleaned_data.get('phone'),
        email=form.cleaned_data.get('email'),
        address=form.cleaned_data.get('address')
    )
    order = Order.objects.get(pk=new_order.pk)
    for product in basket:
        ItemInOrder.objects.create(
            order=order,
            product=product['product'],
            price=product['price'],
            quantity=product['quantity']
        )
    basket.clear()
    request.session['order_id'] = order.id
    return order


def create_stripe_session(request, order):
    success_url = request.build_absolute_uri(reverse('completed'))
    cancel_url = request.build_absolute_uri(reverse('canceled'))
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
    return session.url
