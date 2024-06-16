from celery import shared_task
from django.core.mail import send_mail
from .models import Order
from django.conf import settings


@shared_task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    subject = f'Заказ №. {order.id}'
    message = f'Здравствуйте! \n\n' \
              f'Ваш заказ успешно обработан.' \
              f'Номер ващего заказа {order.id}.'
    mail_sent = send_mail(subject=subject, message=message, from_email=settings.EMAIL_HOST_USER,
                          recipient_list=[order.email])
    return mail_sent
