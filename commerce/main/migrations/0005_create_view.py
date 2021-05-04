
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20210501_2016'),
    ]

    sql = """
        CREATE VIEW main_views_product AS
        SELECT id, views FROM main_product;
    """

    operations = [
        migrations.RunSQL(sql)
    ]

