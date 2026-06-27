from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from django.db.models import Count, Q


class CategoryListView(APIView):
    """GET /api/categories/"""

    def get(self, request):
        cats = Category.objects.annotate(
            product_count=Count(
                'products',
                filter=Q(products__size_stocks__quantity__gt=0),
                distinct=True,
            )
        ).prefetch_related('products__images', 'products__size_stocks')
        return Response(CategorySerializer(cats, many=True, context={'request': request}).data)


class ProductListView(APIView):
    """GET /api/products/"""

    def get(self, request):
        category = request.query_params.get('category')
        sale     = request.query_params.get('sale')

        # Показуємо товари які або мають залишки, або ще не налаштовані (немає записів size_stocks)
        qs = Product.objects.filter(
            Q(size_stocks__quantity__gt=0) | Q(size_stocks__isnull=True)
        ).distinct().select_related('category').prefetch_related('images', 'size_stocks')

        if category:
            qs = qs.filter(category__name=category)
        if sale == 'true':
            qs = qs.filter(old_price__isnull=False)

        return Response(ProductSerializer(qs, many=True, context={'request': request}).data)


class ProductDetailView(APIView):
    """GET /api/products/<id>/"""

    def get(self, request, pk):
        try:
            product = Product.objects.select_related('category').prefetch_related('images', 'size_stocks').get(pk=pk)
        except Product.DoesNotExist:
            return Response({'error': 'Товар не знайдено'}, status=404)
        return Response(ProductSerializer(product, context={'request': request}).data)
