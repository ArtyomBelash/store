from django.urls import path, include
from .views import *

urlpatterns = [
    path('', ProductListView.as_view(), name='products'),
    path('product/<slug:slug>', ProductDetailView.as_view(), name='detail'),
    path('category/<slug:slug>', ProductsByCategoryListView.as_view(), name='category'),
]
