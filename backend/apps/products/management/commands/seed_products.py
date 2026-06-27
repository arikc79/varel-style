from django.core.management.base import BaseCommand
from apps.products.models import Product, ProductImage, ProductSizeStock, Category

PRODUCTS_DATA = [
    {
        "name": "Класична біла сорочка",
        "price": 890, "old_price": 1200,
        "description": "Елегантна сорочка з натуральної бавовни. Підходить для офісу та повсякденного носіння. Легко поєднується з будь-яким одягом.",
        "emoji": "👔", "sizes": ["XS", "S", "M", "L", "XL"], "colors": ["білий", "блакитний"],
        "details": {"матеріал": "100% бавовна", "країна": "Туреччина"}, "badge": "sale",
        "category": "Чоловічий одяг",
        "photo_url": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=600",
    },
    {
        "name": "Чорні джинси Slim Fit",
        "price": 1450, "old_price": None,
        "description": "Стильні джинси зі зручним кроєм slim fit. Виготовлені з якісного денімового матеріалу з додаванням еластану.",
        "emoji": "👖", "sizes": ["S", "M", "L", "XL"], "colors": ["чорний", "темно-синій"],
        "details": {"матеріал": "98% бавовна, 2% еластан", "країна": "Бангладеш"}, "badge": "new",
        "category": "Чоловічий одяг",
        "photo_url": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=600",
    },
    {
        "name": "Літня сукня в квіти",
        "price": 1200, "old_price": 1600,
        "description": "Легка літня сукня з квітковим принтом. Ідеальний вибір для прогулянок та відпочинку. Приємна тканина не викликає дискомфорту.",
        "emoji": "👗", "sizes": ["XS", "S", "M", "L"], "colors": ["рожевий", "жовтий"],
        "details": {"матеріал": "100% віскоза", "країна": "Туреччина"}, "badge": "sale",
        "category": "Жіночий одяг",
        "photo_url": "https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=600",
    },
    {
        "name": "Жіноче пальто оверсайз",
        "price": 2800, "old_price": None,
        "description": "Стильне пальто вільного крою для прохолодної погоди. Класичний дизайн поєднується з сучасним силуетом.",
        "emoji": "🧥", "sizes": ["S", "M", "L", "XL"], "colors": ["бежевий", "сірий", "чорний"],
        "details": {"матеріал": "70% вовна, 30% поліестер", "країна": "Польща"}, "badge": "new",
        "category": "Жіночий одяг",
        "photo_url": "https://images.unsplash.com/photo-1548624313-0396c75e4b1a?w=600",
    },
    {
        "name": "Шкіряний ремінь чоловічий",
        "price": 450, "old_price": None,
        "description": "Класичний ремінь з натуральної шкіри. Металева пряжка з антикорозійним покриттям. Підходить до будь-якого стилю.",
        "emoji": "👜", "sizes": ["S", "M", "L"], "colors": ["коричневий", "чорний"],
        "details": {"матеріал": "натуральна шкіра", "країна": "Україна"}, "badge": "",
        "category": "Аксесуари",
        "photo_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=600",
    },
    {
        "name": "Спортивний костюм",
        "price": 1890, "old_price": 2200,
        "description": "Зручний спортивний костюм для тренувань та активного відпочинку. Дихаючий матеріал забезпечує комфорт.",
        "emoji": "🩱", "sizes": ["S", "M", "L", "XL", "XXL"], "colors": ["сірий", "чорний", "синій"],
        "details": {"матеріал": "80% бавовна, 20% поліестер", "країна": "Китай"}, "badge": "sale",
        "category": "Чоловічий одяг",
        "photo_url": "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=600",
    },
    {
        "name": "Жіноча блуза шовкова",
        "price": 980, "old_price": None,
        "description": "Елегантна блуза з шовкоподібної тканини. Вільний крій підкреслює жіночність. Підходить для офісу та вечірніх виходів.",
        "emoji": "👚", "sizes": ["XS", "S", "M", "L"], "colors": ["білий", "чорний", "бордовий"],
        "details": {"матеріал": "100% поліестер (шовковий)", "країна": "Туреччина"}, "badge": "",
        "category": "Жіночий одяг",
        "photo_url": "https://images.unsplash.com/photo-1564257631407-4deb1f99d992?w=600",
    },
    {
        "name": "Кросівки білі унісекс",
        "price": 2200, "old_price": 2800,
        "description": "Легкі та зручні кросівки для повсякденного носіння. Підошва з піни забезпечує амортизацію. Підходять до будь-якого образу.",
        "emoji": "👟", "sizes": ["38", "39", "40", "41", "42", "43", "44"], "colors": ["білий"],
        "details": {"матеріал": "текстиль + гума", "країна": "В'єтнам"}, "badge": "sale",
        "category": "Аксесуари",
        "photo_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600",
    },
    {
        "name": "Худі оверсайз унісекс",
        "price": 1100, "old_price": None,
        "description": "Теплий худі з м'якого флісу. Великий капюшон і кенгуру-кишеня. Ідеально для осені та весни.",
        "emoji": "🧥", "sizes": ["S", "M", "L", "XL", "XXL"], "colors": ["сірий", "чорний", "зелений"],
        "details": {"матеріал": "70% бавовна, 30% поліестер", "країна": "Бангладеш"}, "badge": "new",
        "category": "Чоловічий одяг",
        "photo_url": "https://images.unsplash.com/photo-1556821840-3a63f15732ce?w=600",
    },
    {
        "name": "Сумка шопер жіноча",
        "price": 750, "old_price": 950,
        "description": "Практична сумка-шопер з екошкіри. Великий основний відділ і внутрішня кишеня на блискавці. Зручні ручки.",
        "emoji": "👜", "sizes": ["one size"], "colors": ["чорний", "бежевий", "червоний"],
        "details": {"матеріал": "екошкіра", "країна": "Польща"}, "badge": "",
        "category": "Аксесуари",
        "photo_url": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=600",
    },
    {
        "name": "Чоловіча футболка базова",
        "price": 380, "old_price": None,
        "description": "Базова футболка з щільної бавовни. Рівний крій, стійкий до деформації після прання. Є в багатьох кольорах.",
        "emoji": "👕", "sizes": ["XS", "S", "M", "L", "XL", "XXL"], "colors": ["білий", "чорний", "сірий", "синій"],
        "details": {"матеріал": "100% бавовна", "країна": "Туреччина"}, "badge": "",
        "category": "Чоловічий одяг",
        "photo_url": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=600",
    },
    {
        "name": "Жіночі легінси спортивні",
        "price": 650, "old_price": 850,
        "description": "Легінси з компресійного матеріалу для занять спортом. Широкий пояс не сповзає під час тренування.",
        "emoji": "🩲", "sizes": ["XS", "S", "M", "L"], "colors": ["чорний", "сірий", "рожевий"],
        "details": {"матеріал": "80% поліамід, 20% еластан", "країна": "Китай"}, "badge": "new",
        "category": "Жіночий одяг",
        "photo_url": "https://images.unsplash.com/photo-1506629082955-511b1aa562c8?w=600",
    },
    {
        "name": "Краватка шовкова чоловіча",
        "price": 420, "old_price": None,
        "description": "Елегантна краватка з натурального шовку. Класичний візерунок у смужку. Підходить для ділових зустрічей.",
        "emoji": "👔", "sizes": ["one size"], "colors": ["синій", "бордовий", "сірий"],
        "details": {"матеріал": "100% шовк", "країна": "Італія"}, "badge": "",
        "category": "Аксесуари",
        "photo_url": "https://images.unsplash.com/photo-1589756823695-278bc923f962?w=600",
    },
    {
        "name": "Зимова куртка пухова",
        "price": 3200, "old_price": 4000,
        "description": "Тепла пухова куртка для холодної зими. Водовідштовхувальне покриття. Капюшон знімається.",
        "emoji": "🧥", "sizes": ["S", "M", "L", "XL", "XXL"], "colors": ["чорний", "темно-синій", "хакі"],
        "details": {"матеріал": "нейлон + пух 80%", "країна": "Китай"}, "badge": "sale",
        "category": "Чоловічий одяг",
        "photo_url": "https://images.unsplash.com/photo-1544923246-77307dd654cb?w=600",
    },
    {
        "name": "Жіноче плаття міді",
        "price": 1350, "old_price": None,
        "description": "Елегантне плаття міді довжини з поясом. Підходить для офісу та вечірніх виходів. Є підкладка.",
        "emoji": "👗", "sizes": ["XS", "S", "M", "L"], "colors": ["чорний", "бежевий", "смарагдовий"],
        "details": {"матеріал": "поліестер з підкладкою", "країна": "Туреччина"}, "badge": "new",
        "category": "Жіночий одяг",
        "photo_url": "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=600",
    },
]


class Command(BaseCommand):
    help = 'Seed products with demo data and photos from Unsplash'

    def handle(self, *args, **kwargs):
        created_count = 0

        for data in PRODUCTS_DATA:
            category, _ = Category.objects.get_or_create(name=data["category"])

            product = Product.objects.create(
                category=category,
                name=data["name"],
                price=data["price"],
                old_price=data["old_price"],
                description=data["description"],
                emoji=data["emoji"],
                sizes=data["sizes"],
                colors=data["colors"],
                details=data["details"],
                badge=data["badge"],
                stock=50,
            )

            for size in data["sizes"]:
                ProductSizeStock.objects.create(product=product, size=size, quantity=10)

            ProductImage.objects.create(
                product=product, order=0, external_url=data["photo_url"]
            )
            self.stdout.write(f"+ {product.name}")

            created_count += 1

        self.stdout.write(
            self.style.SUCCESS(f'\nГотово! Створено {created_count} товарів.')
        )
