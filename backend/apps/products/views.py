from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from django.db.models import Count, Q

class CategoryListView(APIView):
    """GET /api/categories/"""

    def get(self, request):
        cats = Category.objects.annotate(
            product_count=Count('products', filter=Q(products__stock__gt=0))
        ).prefetch_related('products__images')
        return Response(CategorySerializer(cats, many=True, context={'request': request}).data)

class ProductListView(APIView):
    """GET /api/products/"""

    def get(self, request):
        category = request.query_params.get('category')
        sale     = request.query_params.get('sale')
        qs = Product.objects.filter(size_stocks__quantity__gt=0).distinct().select_related('category').prefetch_related('images', 'size_stocks')
        if category:
            qs = qs.filter(category__name=category)
        if sale == 'true':
            qs = qs.filter(old_price__isnull=False)
        return Response(ProductSerializer(qs, many=True, context={'request': request}).data)

class ProductDetailView(APIView):
    """GET /api/products/<id>/"""

    def get(self, request, pk):
        try:
            product = Product.objects.select_related('category').prefetch_related('images').get(pk=pk, stock__gt=0)
        except Product.DoesNotExist:
            return Response({'error': 'Товар не знайдено'}, status=404)
        return Response(ProductSerializer(product, context={'request': request}).data)
