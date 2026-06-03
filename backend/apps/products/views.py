from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from django.db.models import Count, Q

class CategoryListView(APIView):
    """GET /api/categories/"""

    def get(self, request):
        cats = Category.objects.annotate(
            product_count=Count('products', filter=Q(products__in_stock=True))
        )
        return Response(CategorySerializer(cats, many=True).data)

class ProductListView(APIView):
    """GET /api/products/"""

    def get(self, request):
        category = request.query_params.get('category')
        qs = Product.objects.filter(in_stock=True).select_related('category').prefetch_related('images')
        if category:
            qs = qs.filter(category__name=category)
        return Response(ProductSerializer(qs, many=True, context={'request': request}).data)

class ProductDetailView(APIView):
    """GET /api/products/<id>/"""

    def get(self, request, pk):
        try:
            product = Product.objects.select_related('category').prefetch_related('images').get(pk=pk, in_stock=True)
        except Product.DoesNotExist:
            return Response({'error': 'Товар не знайдено'}, status=404)
        return Response(ProductSerializer(product, context={'request': request}).data)
