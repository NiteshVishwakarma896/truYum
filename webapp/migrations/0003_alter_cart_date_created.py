# Generated by Django 4.0.4 on 2022-05-24 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
