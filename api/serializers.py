from rest_framework import serializers
from products.models import Product, Category
from profiles.models import Profile


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'slug']


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
