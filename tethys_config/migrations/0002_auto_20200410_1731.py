# Generated by Django 2.2.8 on 2020-04-10 17:31

from django.db import migrations
from tethys_config.init import custom_settings, reverse_custom


class Migration(migrations.Migration):

    dependencies = [
        ("tethys_config", "0001_initial_30"),
    ]

    operations = [
        migrations.RunPython(custom_settings, reverse_custom),
        migrations.AlterModelOptions(
            name="settingscategory",
            options={
                "ordering": ["pk"],
                "verbose_name": "Settings Category",
                "verbose_name_plural": "Site Settings",
            },
        ),
    ]
