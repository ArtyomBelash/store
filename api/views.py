from rest_framework import viewsets
from products.models import Product, Category
from api.serializers import ProductSerializer, CategorySerializer
from .permissions import IsAdminOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response


class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'pk'

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
