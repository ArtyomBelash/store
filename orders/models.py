from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
from products.models import Product


class Order(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя')
    surname = models.CharField(max_length=200, verbose_name='Фамилия')
    phone = PhoneNumberField(region='BY', verbose_name='Телефон', blank=False)
    email = models.EmailField(default=None)
    address = models.CharField(max_length=600, verbose_name='Адрес')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обнавлено')
    paid = models.BooleanField(default=False, verbose_name='Заплачено')
    stripe_id = models.CharField(max_length=254, blank=True, verbose_name='StripeID')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ {self.pk}'

    def get_total_cost(self):
        return sum(i.get_cost() for i in self.items.all())

    def get_stripe_url(self):
        if not self.stripe_id:
            return ''
        if '_test_' in settings.STRIPE_SECRET_KEY:
            path = '/test/'
        else:
            path = '/'
        return f'https://dashboard.stripe.com{path}payments/{self.stripe_id}'


class ItemInOrder(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE, verbose_name='Товар')
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    def __str__(self):
        return f'Заказ №{self.pk}'

    def get_cost(self):
        return self.price * self.quantity

    class Meta:
        verbose_name_plural = 'Товары в заказе'
