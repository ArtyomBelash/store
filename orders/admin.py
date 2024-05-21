from django.contrib import admin
from django.contrib.admin import TabularInline

from .models import *


class OrderAdmin(TabularInline):
    model = ItemInOrder
    raw_id_fields = ['products', ]


admin.site.register(ItemInOrder)


class OrdersAdmin(admin.ModelAdmin):
    list_display = ['name', 'surname', 'phone', 'address', 'created', 'paid']
    list_editable = ['paid']


admin.site.register(Order, OrdersAdmin)
