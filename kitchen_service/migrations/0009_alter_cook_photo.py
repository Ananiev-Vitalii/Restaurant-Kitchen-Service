# Generated by Django 5.1 on 2024-10-26 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kitchen_service', '0008_alter_cook_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cook',
            name='photo',
            field=models.ImageField(default='cooks/default.jpg', upload_to='cooks/'),
        ),
    ]
