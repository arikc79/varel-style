from rest_framework import serializers
from .models import Category, Product, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only=True)
    cover_image   = serializers.SerializerMethodField()

    class Meta:
        model  = Category
        fields = ['id', 'name', 'emoji', 'order', 'product_count', 'cover_image']

    def get_product_count(self, obj):
        return obj.products.filter(stock__gt=0).count()

    def get_cover_image(self, obj):
        request = self.context.get('request')
        for product in obj.products.all():
            imgs = list(product.images.all())
            if imgs:
                if imgs[0].external_url:
                    return imgs[0].external_url
                if imgs[0].image:
                    url = imgs[0].image.url
                    return request.build_absolute_uri(url) if request else url
        return None


class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model  = ProductImage
        fields = ['id', 'image_url', 'order']

    def get_image_url(self, obj):
        if obj.external_url:
            return obj.external_url
        if obj.image:
            request = self.context.get('request')
            url = obj.image.url
            return request.build_absolute_uri(url) if request else url
        return None


class ProductSerializer(serializers.ModelSerializer):
    images         = ProductImageSerializer(many=True, read_only=True)
    # category повертає рядок (назву) — сумісно з JS
    category       = serializers.CharField(source='category.name',  read_only=True, default='')
    category_emoji = serializers.CharField(source='category.emoji', read_only=True, default='👔')

    in_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model  = Product
        fields = [
            'id', 'name', 'category', 'category_emoji',
            'price', 'old_price', 'description', 'emoji',
            'sizes', 'colors', 'details', 'badge', 'in_stock', 'stock', 'created_at', 'images',
        ]
