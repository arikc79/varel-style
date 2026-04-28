from rest_framework import serializers
from .models import Category, Product, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()

    class Meta:
        model  = Category
        fields = ['id', 'name', 'emoji', 'order', 'product_count']

    def get_product_count(self, obj):
        return obj.products.filter(in_stock=True).count()


class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model  = ProductImage
        fields = ['id', 'image_url', 'order']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None


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
