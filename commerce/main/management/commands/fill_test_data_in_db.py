from django.core.management.base import BaseCommand, CommandError

from main.models import Category, Tag, Product


class Command(BaseCommand):
    help = 'Fill test data in db'

    def handle(self, *args, **options):

        for product in TEST_DATA_PRODUCT["products"]:
            new_product = Product.objects.filter(title=product["title"]).first()
            if new_product is None:
                new_product = Product()
                new_product.title = product["title"]
                new_product.slug = product["slug"]
                new_product.short_desc = product["short_desc"]
                new_product.description = product["description"]
                new_product.price = product["price"]
                new_product.category = Category.objects.get_or_create(
                    title=product["category"]["title"], slug=product["category"]["slug"]
                )[0]
                new_product.save()

                new_product.tags.add(Tag.objects.get_or_create(title=product["tags"])[0])

        self.stdout.write(self.style.SUCCESS("Successfully closed command fill test data in db."))


TEST_DATA_PRODUCT = {
    "products": [
        {
            "title": "15.6 Ноутбук Lenovo IdeaPad L340-15API (81LW0056RK)",
            "slug": "laptops-lenovo-ideapad-l340-15api",
            "short_desc": "Краткое описние",
            "description": "Описание для модели 15.6 Ноутбук Lenovo IdeaPad L340-15API (81LW0056RK)",
            "price": 25400,
            "quantity": 4,
            "tags": "Lenovo",
            "category": {
                "title": "Ноутбуки", "slug": "noutbuki"
            }
        },
        {
            "title": "14 Ноутбук Lenovo ThinkBook 14 G2 ARE (20VF0035RU)",
            "slug": "laptops-lenovo-thinkbook-14-g2-are",
            "short_desc": "Краткое описние",
            "description": "Описание для модели 14 Ноутбук Lenovo ThinkBook 14 G2 ARE (20VF0035RU)",
            "price": 32000,
            "quantity": 5,
            "tags": "Lenovo",
            "category": {
                "title": "Ноутбуки", "slug": "noutbuki"
            }
        },
        {
            "title": "Apple iPhone 12 Pro Max, 512 ГБ, серебристый",
            "slug": "apple-iphone-12-pro-max-512-silver-color",
            "short_desc": "Краткое описние",
            "description": "Дисплей представляет собой прямоугольник с закруглёнными углами. Диагональ этого прямоугольника без учёта закруглений составляет 5,42 дюйма (для iPhone 12 mini), 5,85 дюйма (для iPhone 11 Pro, iPhone XS, iPhone X), 6,06 дюйма (для iPhone 12 Pro, iPhone 12, iPhone 11, iPhone XR), 6,46 дюйма (для iPhone 11 Pro Max, iPhone XS Max) или 6,68 дюйма (для iPhone 12 Pro Max). Фактическая область просмотра меньше.",
            "price": 139990,
            "quantity": 3,
            "tags": "Apple",
            "category": {
                "title": "Смартфоны", "slug": "smartphones"
            }
        },
        {
            "title": "Apple Watch Series 6, 44 мм, корпус из алюминия синего цвета",
            "slug": "apple-watch-series-6-44-blue-aluminum-housing",
            "short_desc": "Краткое описние",
            "description": "Отличный помощник для айфона и прекрасный мотиватор тренировок. Apple Watch 6 как и остальные яблочные модели прекрасен во всём (про заряд - ставлю ежедневно на зарядку будто завожу и не напрягаюсь вообще), от цвета до дизайна. Функционал на высоте. Очень рекомендую!",
            "price": 39490,
            "quantity": 7,
            "tags": "Apple",
            "category": {
                "title": "Смарт-часы", "slug": "smart-watch"
            }
        },
    ],
}
