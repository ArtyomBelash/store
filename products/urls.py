from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='products'),
    path('popular', views.PopularProductsListView.as_view(), name='popular_products'),
    path('search', views.SearchProductsListView.as_view(), name='search_products'),
    path('product/<slug:slug>', views.ProductDetailView.as_view(), name='detail'),
    path('category/<slug:slug>', views.ProductsByCategoryListView.as_view(), name='category'),
]
