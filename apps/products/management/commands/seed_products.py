from django.core.management.base import BaseCommand
from apps.products.models import Category, Product


CATEGORIES_DATA = [
    {'name': 'Джинси',   'emoji': '👖', 'order': 0},
    {'name': 'Сорочки',  'emoji': '👔', 'order': 1},
    {'name': 'Костюми',  'emoji': '🤵', 'order': 2},
    {'name': 'Спорт',    'emoji': '🏃', 'order': 3},
    {'name': 'Куртки',   'emoji': '🧥', 'order': 4},
    {'name': 'Кросівки', 'emoji': '👟', 'order': 5},
]

PRODUCTS = [
    {
        'category_name': 'Джинси', 'name': 'Slim-Fit Jeans', 'emoji': '👖',
        'price': 2890, 'old_price': 3500, 'badge': 'Хіт',
        'description': 'Класичні чорні джинси зі стрейч-тканини. Ідеальна посадка на кожен день.',
        'sizes': ['28','30','32','34','36','38'],
        'details': {'Склад':'98% Бавовна, 2% Еластан','Країна':'Туреччина','Посадка':'Slim Fit','Колір':'Чорний'},
    },
    {
        'category_name': 'Джинси', 'name': 'Regular Denim', 'emoji': '👖',
        'price': 2590, 'badge': '',
        'description': 'Класичний синій деним. Прямий крій, міцна тканина.',
        'sizes': ['30','32','34','36','38'],
        'details': {'Склад':'100% Бавовна','Країна':'Туреччина','Посадка':'Regular Fit','Колір':'Синій'},
    },
    {
        'category_name': 'Сорочки', 'name': 'Oxford Shirt White', 'emoji': '👔',
        'price': 1990, 'old_price': 2400, 'badge': 'New',
        'description': 'Класична оксфордська сорочка. Ідеальна для офісу та вечора.',
        'sizes': ['S','M','L','XL','XXL'],
        'details': {'Склад':'100% Бавовна','Країна':'Італія','Крій':'Slim','Колір':'Білий'},
    },
    {
        'category_name': 'Сорочки', 'name': 'Linen Shirt Black', 'emoji': '👔',
        'price': 2290, 'badge': '',
        'description': 'Льняна сорочка. Легка, дихаюча, ідеальна для теплого сезону.',
        'sizes': ['S','M','L','XL'],
        'details': {'Склад':'100% Льон','Країна':'Португалія','Крій':'Regular','Колір':'Чорний'},
    },
    {
        'category_name': 'Костюми', 'name': 'Classic Suit Charcoal', 'emoji': '🤵',
        'price': 12900, 'old_price': 15000, 'badge': 'Premium',
        'description': 'Класичний двійка. Вовняна тканина, ідеальний крій.',
        'sizes': ['46','48','50','52','54'],
        'details': {'Склад':'70% Вовна, 30% Поліестер','Країна':'Польща','Тип':'Двійка','Колір':'Антрацит'},
    },
    {
        'category_name': 'Костюми', 'name': 'Navy Blue Suit', 'emoji': '🤵',
        'price': 11500, 'badge': '',
        'description': 'Темно-синій костюм — класика преміум-класу.',
        'sizes': ['46','48','50','52'],
        'details': {'Склад':'65% Вовна, 35% Поліестер','Країна':'Польща','Тип':'Двійка','Колір':'Темно-синій'},
    },
    {
        'category_name': 'Спорт', 'name': 'Sport Suit Track', 'emoji': '🏃',
        'price': 4900, 'old_price': 5800, 'badge': 'Sale',
        'description': 'Стильний спортивний костюм. Дихаюча тканина.',
        'sizes': ['S','M','L','XL','XXL'],
        'details': {'Склад':'80% Поліестер, 20% Бавовна','Країна':'Туреччина','Тип':'Брюки + Худі','Колір':'Чорний'},
    },
    {
        'category_name': 'Спорт', 'name': 'Jogger Set Grey', 'emoji': '🏃',
        'price': 3900, 'badge': '',
        'description': 'Джоггер-сет у сірому кольорі. Мінімалістичний дизайн.',
        'sizes': ['S','M','L','XL'],
        'details': {'Склад':'75% Бавовна, 25% Поліестер','Країна':'Туреччина','Тип':'Брюки + Толстовка','Колір':'Сірий'},
    },
    {
        'category_name': 'Куртки', 'name': 'Leather Jacket Black', 'emoji': '🧥',
        'price': 8900, 'old_price': 11000, 'badge': 'Premium',
        'description': 'Шкіряна куртка — вічна класика. Натуральна шкіра.',
        'sizes': ['S','M','L','XL'],
        'details': {'Склад':'100% Натуральна шкіра','Країна':'Іспанія','Тип':'Косуха','Колір':'Чорний'},
    },
    {
        'category_name': 'Куртки', 'name': 'Bomber Olive', 'emoji': '🧥',
        'price': 5900, 'badge': '',
        'description': 'Бомбер в кольорі олива. Сучасний фасон, тепла підкладка.',
        'sizes': ['S','M','L','XL','XXL'],
        'details': {'Склад':'Поліестер, Нейлон','Країна':'Туреччина','Тип':'Бомбер','Колір':'Олива'},
    },
    {
        'category_name': 'Кросівки', 'name': 'Air Max Pro', 'emoji': '👟',
        'price': 6500, 'old_price': 7900, 'badge': 'New',
        'description': 'Преміальні кросівки Air Max. Легкі, дихаючі.',
        'sizes': ['39','40','41','42','43','44','45'],
        'details': {'Матеріал':'Сітка + шкіра','Підошва':'Гума Air','Країна':"В'єтнам",'Колір':'Білий/Чорний'},
    },
    {
        'category_name': 'Кросівки', 'name': 'Suede Sneaker White', 'emoji': '👟',
        'price': 5200, 'badge': '',
        'description': 'Замшеві кросівки. Простота та елегантність.',
        'sizes': ['40','41','42','43','44'],
        'details': {'Матеріал':'Натуральна замша','Підошва':'Гума','Країна':'Португалія','Колір':'Білий'},
    },
]


class Command(BaseCommand):
    help = 'Заповнити базу тестовими категоріями та товарами'

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help='Очистити перед заповненням')

    def handle(self, *args, **options):
        if options['clear']:
            Product.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write(self.style.WARNING('БД очищено'))

        # 1. Категорії
        for c in CATEGORIES_DATA:
            Category.objects.update_or_create(name=c['name'], defaults=c)
        self.stdout.write(f'  Категорії: {Category.objects.count()}')

        # 2. Товари
        created = 0
        for data in PRODUCTS:
            cat_name = data.pop('category_name')
            cat = Category.objects.get(name=cat_name)
            _, is_new = Product.objects.update_or_create(
                name=data['name'],
                defaults={'category': cat, **data},
            )
            if is_new:
                created += 1

        self.stdout.write(self.style.SUCCESS(
            f'✅ Готово! Нових товарів: {created}, всього: {Product.objects.count()}'
        ))
