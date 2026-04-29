import json
import sys
import os
import django

# Setup Django
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'first_style.settings')
django.setup()

from apps.products.models import Category, Product, ProductImage

# Load backup
with open('database/db_backup.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Import categories
categories_map = {}
for item in data:
    if item['model'] == 'products.category':
        cat, created = Category.objects.get_or_create(
            pk=item['pk'],
            defaults=item['fields']
        )
        categories_map[item['pk']] = cat
        print(f"✓ Категорія: {cat}")

# Import products
products_map = {}
valid_product_fields = ['category', 'name', 'price', 'old_price', 'description', 
                        'emoji', 'sizes', 'details', 'badge', 'in_stock', 'created_at']

for item in data:
    if item['model'] == 'products.product':
        fields = {}
        for key, value in item['fields'].items():
            if key in valid_product_fields:
                fields[key] = value
        
        if fields.get('category'):
            fields['category_id'] = fields.pop('category')
        else:
            fields.pop('category', None)
        
        prod, created = Product.objects.get_or_create(
            pk=item['pk'],
            defaults=fields
        )
        products_map[item['pk']] = prod
        print(f"✓ Товар: {prod.name}")

# Import product images
for item in data:
    if item['model'] == 'products.productimage':
        fields = item['fields'].copy()
        fields['product_id'] = fields.pop('product')
        
        try:
            img, created = ProductImage.objects.get_or_create(
                pk=item['pk'],
                defaults=fields
            )
            print(f"✓ Фото: {img}")
        except Exception as e:
            print(f"✗ Помилка фото: {e}")

print(f"\n🎉 Імпорт завершено!")
print(f"📦 Категорій: {Category.objects.count()}")
print(f"🛍️ Товарів: {Product.objects.count()}")
print(f"📸 Фото: {ProductImage.objects.count()}")

