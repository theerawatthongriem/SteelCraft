# Generated by Django 5.0.3 on 2024-05-20 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0010_remove_product_material'),
        ('members', '0026_measuresizematerial'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='measuresizematerial',
            constraint=models.UniqueConstraint(fields=('measure_size', 'material'), name='unique_measure_size_material'),
        ),
    ]
