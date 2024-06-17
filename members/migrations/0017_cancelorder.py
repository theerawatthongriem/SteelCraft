# Generated by Django 5.0.3 on 2024-05-08 13:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0016_order_deposit_payment'),
    ]

    operations = [
        migrations.CreateModel(
            name='CancelOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cancellation_reason', models.CharField(blank=True, max_length=100, null=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.order')),
            ],
        ),
    ]