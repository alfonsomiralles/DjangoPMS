# Generated by Django 4.1.4 on 2023-01-22 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accommodation', '0003_alter_accommodation_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(max_length=30),
        ),
    ]
