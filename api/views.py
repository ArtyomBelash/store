from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView

from products.models import Product, Category
from api.serializers import ProductSerializer, CategorySerializer, ProfileSerializer
from profiles.models import Profile
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.reverse import reverse


class ApiRoot(APIView):
    http_method_names = ['get']

    def get(self, request):
        return Response({
            'products': reverse('product-list', request=request),
            'category': reverse('category-list', request=request),
            'profile': reverse('profile-list', request=request)
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
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    @method_decorator(cache_page(60 * 60), name='profile_list_cache')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


