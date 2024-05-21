from django.urls import path
from .views import *


urlpatterns = [
    path('', BasketDetailView.as_view(), name='basket_detail'),
    path('remove/<slug:slug>/', BasketRemoveView.as_view(), name='basket_remove'),
    path('add/<slug:slug>/', AddProductsBasketView.as_view(), name='basket_add'),
]