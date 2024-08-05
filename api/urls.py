from django.urls import path, include
from . import views
from rest_framework import routers
from rest_framework.authtoken import views as rest_views

router = routers.SimpleRouter()
router.register(r'products', views.ProductsViewSet)
router.register(r'category', views.CategoriesViewSet)
router.register(r'profile', views.ProfileViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'item_in_order', views.ItemViewSet)
urlpatterns = [
    path('', views.ApiRoot.as_view()),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/', rest_views.obtain_auth_token)
]
