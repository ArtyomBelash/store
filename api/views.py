from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets, permissions
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView

from api.utils import get_permissions_for_orders_and_item_in_order
from orders.models import Order, ItemInOrder
from products.models import Product, Category
from api.serializers import ProductSerializer, CategorySerializer, ProfileSerializer, OrderSerializer, \
    ItemInOrderSerializer
from profiles.models import Profile
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.reverse import reverse


class ApiRoot(APIView):
    http_method_names = ['get']

    @staticmethod
    def get(request):
        return Response({
            'products': reverse('product-list', request=request),
            'category': reverse('category-list', request=request),
            'profile': reverse('profile-list', request=request),
            'orders': reverse('order-list', request=request),
            'item_in_order': reverse('iteminorder-list', request=request),
        })


class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().select_related('category')
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    pagination_class = LimitOffsetPagination

    @method_decorator(cache_page(60 * 60), name='products_list_cache')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(methods=['get'], detail=False)
    def categories(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'pk'

    @action(methods=['get'], detail=False)
    def products(self, request):
        category = self.get_object()
        products = Product.objects.filter(category=category)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProfileViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    @method_decorator(cache_page(60 * 60), name='profile_list_cache')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_permissions(self):
        return get_permissions_for_orders_and_item_in_order(self.action)


class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemInOrderSerializer
    queryset = ItemInOrder.objects.all()

    def get_permissions(self):
        return get_permissions_for_orders_and_item_in_order(self.action)
