from django.urls import path, include
from .views import *

urlpatterns = [
    path('', ProductListView.as_view(), name='products'),
    path('<slug:slug>', ProductDetailView.as_view(), name='detail'),
]
