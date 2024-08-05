from rest_framework import serializers

from orders.models import Order, ItemInOrder
from products.models import Product, Category
from profiles.models import Profile


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'description', 'short_description', 'slug', 'image', 'price', 'category', 'updated']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'username', 'email', 'password', 'picture', 'slug']
        read_only_fields = ['picture', 'slug']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile = super().create(validated_data)
        profile.set_password(profile.password)
        if not profile.slug:
            profile.slug = profile.username
        profile.save()
        return profile

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.slug = instance.username
        instance.save()
        return instance


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'name', 'surname', 'phone', 'email', 'address', 'created', 'stripe_id', 'get_total_cost']
        read_only_fields = ['created', 'stripe_id', ]

    @staticmethod
    def get_total_cost(obj):
        return obj.get_total_cost()


class ItemInOrderSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = ItemInOrder
        fields = ['id', 'order', 'product', 'quantity', 'get_cost']

    @staticmethod
    def get_cost(obj):
        return obj.get_cost()

    def create(self, validated_data):
        product = validated_data['product']
        validated_data['price'] = product.price
        return super().create(validated_data)

    def update(self, instance, validated_data):
        product = validated_data.get('product', instance.product)
        validated_data['price'] = product.price
        return super().update(instance, validated_data)
