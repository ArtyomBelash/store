from django.contrib import admin
from django.contrib.admin import TabularInline

from .models import *

from django.utils.safestring import mark_safe


def order_stripe_payment(obj):
    url = obj.get_stripe_url()
    if obj.stripe_id:
        html = f'<a href="{url}" target="_blank">{obj.stripe_id}</a>'
        return mark_safe(html)
    return ''


order_stripe_payment.short_description = 'Инфо Stripe'


class ItemInOrderInlines(TabularInline):
    model = ItemInOrder
    raw_id_fields = ['product', ]
    verbose_name_plural = 'Товары в заказе'


admin.site.register(ItemInOrder)


class OrdersAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'surname', 'phone', 'address', 'created', 'paid', order_stripe_payment]
    list_editable = ['paid']
    inlines = (ItemInOrderInlines,)


admin.site.register(Order, OrdersAdmin)
