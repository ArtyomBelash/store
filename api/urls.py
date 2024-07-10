from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'products', ProductsViewSet)
router.register(r'category', CategoriesViewSet)

urlpatterns = [
    path('', include(router.urls),),
    # path('products/', ProductListAPIView.as_view(), name='products_api_list'),
    # path('products/<pk>/', ProductDetailView.as_view(), name='product_api_detail'),
]
