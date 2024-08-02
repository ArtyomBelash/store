from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'products', views.ProductsViewSet)
router.register(r'category', views.CategoriesViewSet)
router.register(r'profile', views.ProfileViewSet)

urlpatterns = [
    path('', include(router.urls), ),
]
