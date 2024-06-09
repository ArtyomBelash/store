from django.urls import path
from .views import *

urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='get_order'),
    path('completed/', payment_completed, name='completed'),
    path('canceled/', payment_canceled, name='canceled'),
]