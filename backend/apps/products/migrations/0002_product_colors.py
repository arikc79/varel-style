# Generated migration to add colors field to Product model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='colors',
            field=models.JSONField(default=list, help_text='["Чорний", "Білий", "Синій"]', verbose_name='Кольори'),
        ),
    ]

