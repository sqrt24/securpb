# Generated by Django 5.1.3 on 2025-01-04 11:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0014_servicestepblock"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="servicereasonblock",
            name="title",
        ),
        migrations.RemoveField(
            model_name="servicestepblock",
            name="title",
        ),
    ]
