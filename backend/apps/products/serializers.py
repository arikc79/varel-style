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
        # Беремо перше фото з довільного товару категорії (уже prefetch'd)
        for product in obj.products.all():
            if not product.in_stock:
                continue
            imgs = list(product.images.all())
            if imgs:
                url = imgs[0].image.url
                return request.build_absolute_uri(url) if request else url
        return None


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

    in_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model  = Product
        fields = [
            'id', 'name', 'category', 'category_emoji',
            'price', 'old_price', 'description', 'emoji',
            'sizes', 'colors', 'details', 'badge', 'in_stock', 'stock', 'created_at', 'images',
        ]
