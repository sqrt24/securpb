# Generated by Django 5.1.3 on 2024-12-23 15:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0012_alter_servicestepblock_options_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="ServiceStepBlock",
        ),
    ]
