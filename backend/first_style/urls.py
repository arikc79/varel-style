from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.products.urls import category_urlpatterns

urlpatterns = [
    path('admin/',            admin.site.urls),
    path('api/categories/',   include(category_urlpatterns)),
    path('api/products/',     include('apps.products.urls')),
    path('api/orders/',       include('apps.orders.urls')),
    path('',                  include('apps.core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

