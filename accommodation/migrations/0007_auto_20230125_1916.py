# Generated by Django 3.2.16 on 2023-01-25 18:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accommodation', '0006_review'),
    ]

    operations = [
        migrations.RenameField(
            model_name='accommodation',
            old_name='image',
            new_name='default_image',
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/')),
                ('accommodation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accommodation.accommodation')),
            ],
        ),
    ]
