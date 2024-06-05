from celery import shared_task
from django.core.mail import send_mail
from .models import Order


@shared_task
def order_created(order_pk):
    order = Order.objects.get(pk=order_pk)
    subject = f'Заказ №. {order.pk}'
    message = f'Hello! \n\n' \
              f'You have successfully placed an order.' \
              f'Your order ID is {order.id}.'
    mail_sent = send_mail(subject, message,
                          'arteniy999@gmail.com',
                          [order.email])
    return mail_sent
