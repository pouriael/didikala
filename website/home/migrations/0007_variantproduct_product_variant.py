# Generated by Django 4.0.4 on 2022-06-30 04:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_productcolor_productsize_product_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='variantproduct',
            name='product_variant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.product'),
        ),
    ]