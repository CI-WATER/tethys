# Generated by Django 3.2.10 on 2021-12-21 23:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tethys_config", "0003_auto_20211220_2307"),
    ]

    operations = [
        migrations.AlterField(
            model_name="setting",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="settingscategory",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
