# Generated by Django 5.1.3 on 2024-12-08 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0003_pricelistcategory_pricelistitem"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="service",
            options={"ordering": ["order"], "verbose_name": "Услуга", "verbose_name_plural": "Услуги"},
        ),
        migrations.AddField(
            model_name="service",
            name="noindex",
            field=models.BooleanField(default=False, verbose_name="Закрыть от индексации"),
        ),
        migrations.AddField(
            model_name="service",
            name="order",
            field=models.IntegerField(blank=True, default=0, verbose_name="Порядковый номер"),
        ),
        migrations.AddField(
            model_name="service",
            name="seo_description",
            field=models.TextField(blank=True, default="", verbose_name="SEO Description"),
        ),
        migrations.AddField(
            model_name="service",
            name="seo_h1",
            field=models.TextField(blank=True, default="", verbose_name="SEO H1"),
        ),
        migrations.AddField(
            model_name="service",
            name="seo_title",
            field=models.TextField(blank=True, default="", verbose_name="SEO Title"),
        ),
        migrations.AddField(
            model_name="service",
            name="show_in_footer",
            field=models.BooleanField(default=False, verbose_name="Показывать в подвале"),
        ),
        migrations.AddField(
            model_name="service",
            name="slug",
            field=models.SlugField(default=1, max_length=255, unique=True, verbose_name="Слаг"),
            preserve_default=False,
        ),
    ]
