# Generated by Django 3.2.7 on 2021-09-12 16:46

from django.db import migrations
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('offert', '0007_auto_20210912_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=mptt.fields.TreeForeignKey(on_delete=django.db.models.deletion.PROTECT, to='offert.category'),
        ),
    ]