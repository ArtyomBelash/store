from django.urls import path
from .webhooks import stripe_webhook
from . import views

urlpatterns = [
    path('create/', views.OrderCreateView.as_view(), name='get_order'),
    path('completed/', views.PaymentCompeted.as_view(), name='completed'),
    path('canceled/', views.PaymentCanceled.as_view(), name='canceled'),
    path('webhook/', stripe_webhook, name='webhook'),
]
