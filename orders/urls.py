from django.urls import path
from .webhooks import stripe_webhook
from . import views

urlpatterns = [
    path('create/', views.OrderCreateView.as_view(), name='get_order'),
    path('completed/', views.payment_completed, name='completed'),
    path('canceled/', views.payment_canceled, name='canceled'),
    path('webhook/', stripe_webhook, name='webhook'),
]