# Generated by Django 4.0.4 on 2022-06-30 14:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_alter_variantproduct_color_variant_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variantproduct',
            name='color_variant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.productcolor'),
        ),
        migrations.AlterField(
            model_name='variantproduct',
            name='product_variant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.product'),
        ),
        migrations.AlterField(
            model_name='variantproduct',
            name='size_variant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.productsize'),
        ),
    ]
