# Generated by Django 5.1.3 on 2024-11-28 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project_settings", "0002_projectsettings_address_projectsettings_email_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="projectsettings",
            name="ymaps_widget_url",
            field=models.URLField(blank=True, default="", verbose_name="URL Яндекс.Карт"),
        ),
    ]
