# Generated by Django 4.0.4 on 2022-06-30 19:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_remove_variantproduct_color_variant_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductColor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='ProductSize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Variantproduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('unit_price', models.PositiveIntegerField()),
                ('discount', models.PositiveIntegerField(blank=True, null=True)),
                ('amount', models.PositiveIntegerField()),
                ('color_variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.productcolor')),
                ('product_variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.product')),
                ('size_variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.productsize')),
            ],
        ),
    ]
