# Generated by Django 2.2.6 on 2020-03-26 16:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("tethys_apps", "0001_initial_30"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="tethysapp",
            options={
                "verbose_name": "Tethys App",
                "verbose_name_plural": "Installed Apps",
            },
        ),
    ]
