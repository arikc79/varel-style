from rest_framework import serializers
from .models import Category, Product, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only=True)

    class Meta:
        model  = Category
        fields = ['id', 'name', 'emoji', 'order', 'product_count']

    def get_product_count(self, obj):
        return obj.products.filter(in_stock=True).count()


class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.ImageField(source='image', read_only=True)

    class Meta:
        model  = ProductImage
        fields = ['id', 'image_url', 'order']


class ProductSerializer(serializers.ModelSerializer):
    images         = ProductImageSerializer(many=True, read_only=True)
    # category повертає рядок (назву) — сумісно з JS
    category       = serializers.CharField(source='category.name',  read_only=True, default='')
    category_emoji = serializers.CharField(source='category.emoji', read_only=True, default='👔')

    class Meta:
        model  = Product
        fields = [
            'id', 'name', 'category', 'category_emoji',
            'price', 'old_price', 'description', 'emoji',
            'sizes', 'details', 'badge', 'in_stock', 'created_at', 'images',
        ]
