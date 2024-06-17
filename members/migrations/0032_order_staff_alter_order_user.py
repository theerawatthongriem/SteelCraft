# Generated by Django 5.0.3 on 2024-05-24 12:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0031_alter_order_payment_proof'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='staff',
            field=models.ForeignKey(blank=True, limit_choices_to={'is_active': False, 'is_staff': True, 'is_superuser': False}, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='customer', to=settings.AUTH_USER_MODEL),
        ),
    ]