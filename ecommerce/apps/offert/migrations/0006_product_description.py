# Generated by Django 3.2.7 on 2021-09-12 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("offert", "0005_product_features"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="description",
            field=models.TextField(blank=True),
        ),
    ]
