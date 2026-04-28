from django.urls import path
from .views import CategoryListView, ProductListView, ProductDetailView

urlpatterns = [
    path('',         ProductListView.as_view()),
    path('<int:pk>/', ProductDetailView.as_view()),
]

# Окремо — категорії
category_urlpatterns = [
    path('', CategoryListView.as_view(), name='categories'),
]

