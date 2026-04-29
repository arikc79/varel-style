from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('catalog/', views.catalog, name='catalog'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
    path('find-us/', views.find_us, name='find_us'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
]

