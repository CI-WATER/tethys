# Generated by Django 2.2.14 on 2020-12-09 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tethys_apps", "0002_auto_20200326_1657"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customsimplesetting",
            # model_name="customsetting",
            name="type",
            field=models.CharField(
                choices=[
                    ("STRING", "String"),
                    ("INTEGER", "Integer"),
                    ("FLOAT", "Float"),
                    ("BOOLEAN", "Boolean"),
                    ("UUID", "UUID"),
                ],
                default="STRING",
                max_length=200,
            ),
        ),
    ]
