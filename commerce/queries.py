from main.models import *

#  with create()

electronics = Category.objects.create(title='Электроника', slug='electronics')

laptops = Category.objects.create(title='Ноутбуки', parent=electronics, slug='laptops')

lenove_tag = Tag.objects.create(title='Lenovo')

Product.objects.create(
    category=laptops,
    title='15.6 Ноутбук Lenovo IdeaPad L340-15API (81LW0056RK), мерый металик',
    slug='laptops-lenovo',
    price=39590,
    quantity=3
).tags.add(lenove_tag)

Product.objects.create(
    category=laptops,
    title='14" Ноутбук Lenovo ThinkBook 14 G2 ARE (20VF0035RU)',
    short_desc='14" Ноутбук Lenovo ThinkBook 14 G2 ARE (20VF0035RU), AMD Ryzen 3 4300U (2.7 ГГц), RAM 8 ГБ, SSD 256 ГБ, AMD Radeon Graphics, Без системы, (20VF0035RU), серый',
    slug='14-laptops-lenovo',
    price=39590,
    quantity=3
).tags.add(lenove_tag)

Product.objects.create(
    category=laptops,
    title='17.3" Ноутбук Lenovo IdeaPad 3 17ADA05',
    short_desc='17.3" Ноутбук Lenovo IdeaPad 3 17ADA05, AMD Ryzen 3 3250U (2.6 ГГц), RAM 8 ГБ, SSD, AMD Radeon Graphics, Без системы, (81W2003XRK), голубой',
    slug='17-laptops-lenovo',
    price=52340,
    quantity=3
).tags.add(lenove_tag)

acer_tag = Tag.objects.create(title='Acer')

Product.objects.create(
    category=laptops,
    title='15.6" Ноутбук Acer Aspire 3 A315-42-R951 (NX.HF9ER.04F), черный',
    slug='laptops-acer',
    price=58890,
    quantity=5
).tags.add(acer_tag)

television = Category.objects.create(title='Телевизоры', parent=electronics, slug='television')

thomson_tag = Tag.objects.create(title='Thomson')

Product.objects.create(
    category=television,
    title='Full HD Телевизор Thomson T40FSL5130 40"',
    slug='television-thomson',
    price=15990,
    quantity=12
).tags.add(thomson_tag)

samsung_tag = Tag.objects.create(title='Samsung')

Product.objects.create(
    category=television,
    title='4K UHD Телевизор Samsung UE55TU7100UX 55"',
    slug='television-samsung',
    price=46990,
    quantity=2
).tags.add(samsung_tag)


#  with save()

appliances = Category(title='Бытовая техника', slug='appliances')
appliances.save()

refrigerators = Category.objects.create(title='Холодильники', parent=appliances, slug='refrigerators')
refrigerators.save()

indesit_tag = Tag(title='Indesit')
indesit_tag.save()

indesit = Product(
    category=refrigerators,
    title='Холодильник Indesit DS 4180 W, белый',
    slug='refrigerators-indesit',
    price=19430,
    quantity=4
)
indesit.save()

indesit.tags.add(indesit_tag)

# filter()

cat_laptops = Category.objects.filter(title='Ноутбуки').first()
cat_laptops.products.all()

cat_refrigerators = Category.objects.filter(title='Холодильники').first()
cat_refrigerators.products.all()
