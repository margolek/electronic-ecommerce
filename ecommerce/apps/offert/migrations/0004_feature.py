# Generated by Django 3.2.7 on 2021-09-11 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("offert", "0003_delete_feature"),
    ]

    operations = [
        migrations.CreateModel(
            name="Feature",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=255, unique=True, verbose_name="Feature Name"
                    ),
                ),
                (
                    "value",
                    models.DecimalField(
                        decimal_places=2, max_digits=6, verbose_name="Feature value"
                    ),
                ),
                ("unit", models.CharField(max_length=10, verbose_name="Unit")),
            ],
        ),
    ]
