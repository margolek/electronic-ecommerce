# Generated by Django 3.2.7 on 2021-09-12 13:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("offert", "0006_product_description"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="feature",
            name="category",
        ),
        migrations.AlterField(
            model_name="product",
            name="description",
            field=models.TextField(blank=True, verbose_name="Product Description"),
        ),
        migrations.CreateModel(
            name="FeatureCategory",
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
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="offert.category",
                    ),
                ),
                (
                    "feature",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="offert.feature"
                    ),
                ),
            ],
            options={
                "unique_together": {("feature", "category")},
            },
        ),
        migrations.AddField(
            model_name="feature",
            name="category",
            field=models.ManyToManyField(
                related_name="feature_categories",
                through="offert.FeatureCategory",
                to="offert.Category",
            ),
        ),
    ]