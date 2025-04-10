# Generated by Django 5.1.3 on 2024-11-28 16:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0002_alter_service_options"),
    ]

    operations = [
        migrations.CreateModel(
            name="PriceListCategory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255, verbose_name="Название")),
            ],
            options={
                "verbose_name": "Прайс-лист: категория",
                "verbose_name_plural": "Прайс-лист: категории",
            },
        ),
        migrations.CreateModel(
            name="PriceListItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255, verbose_name="Название")),
                ("price", models.CharField(max_length=255, verbose_name="Цена")),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="services.pricelistcategory",
                        verbose_name="категория",
                    ),
                ),
            ],
            options={
                "verbose_name": "Прайс-лист: элемент категории",
                "verbose_name_plural": "Прайс-лист: элементы категорий",
            },
        ),
    ]
