# Generated by Django 5.0.3 on 2024-05-24 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0029_alter_order_appt_date_alter_order_ship_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_proof',
            field=models.ImageField(null=True, upload_to='payment_proofs/'),
        ),
    ]