from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from products.models import Product, Category
from api.serializers import ProductSerializer, CategorySerializer, ProfileSerializer
from profiles.models import Profile
from .permissions import IsAdminOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response


class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    pagination_class = LimitOffsetPagination

    @action(methods=['get'], detail=False)
    def categories(self, request):
        cats = Category.objects.all()
        serializer = CategorySerializer(cats, many=True)
        return Response(serializer.data)


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'pk'

    @action(methods=['get'], detail=True)
    def products(self, request):
        category = self.get_object()
        products = Product.objects.filter(category=category)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
