# Generated by Django 4.0.4 on 2022-07-13 07:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0028_brand_alter_category_options_alter_comment_options_and_more'),
        ('order', '0004_coupon_order_discount'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coupon',
            options={'verbose_name': 'تخفیف', 'verbose_name_plural': '  تخفیف ها'},
        ),
        migrations.AlterModelOptions(
            name='itemorder',
            options={'verbose_name': 'جزئیات سفارش', 'verbose_name_plural': 'جزئیات سفارشات'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'فرم سفارش', 'verbose_name_plural': 'فرم های سفارش'},
        ),
        migrations.AlterField(
            model_name='coupon',
            name='active',
            field=models.BooleanField(default=False, verbose_name='آیا فعال است؟'),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='code',
            field=models.CharField(max_length=100, unique=True, verbose_name='کد تخفیف'),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='discount',
            field=models.IntegerField(verbose_name='درصد تخفیف'),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='end',
            field=django_jalali.db.models.jDateTimeField(verbose_name='پایان'),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='start',
            field=django_jalali.db.models.jDateTimeField(verbose_name='شروع'),
        ),
        migrations.AlterField(
            model_name='itemorder',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_item', to='order.order', verbose_name='سفارش'),
        ),
        migrations.AlterField(
            model_name='itemorder',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.product', verbose_name='محصول'),
        ),
        migrations.AlterField(
            model_name='itemorder',
            name='quantity',
            field=models.IntegerField(verbose_name='مقدار'),
        ),
        migrations.AlterField(
            model_name='itemorder',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
        migrations.AlterField(
            model_name='itemorder',
            name='variant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.variantproduct', verbose_name='ویژگی'),
        ),
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.CharField(max_length=500, verbose_name='آدرس'),
        ),
        migrations.AlterField(
            model_name='order',
            name='create',
            field=django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='زمان ایجاد'),
        ),
        migrations.AlterField(
            model_name='order',
            name='discount',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='درصد تخفیف'),
        ),
        migrations.AlterField(
            model_name='order',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='ایمیل'),
        ),
        migrations.AlterField(
            model_name='order',
            name='f_name',
            field=models.CharField(max_length=50, verbose_name='نام'),
        ),
        migrations.AlterField(
            model_name='order',
            name='l_name',
            field=models.CharField(max_length=50, verbose_name='نام خانوادگی'),
        ),
        migrations.AlterField(
            model_name='order',
            name='paid',
            field=models.BooleanField(default=False, verbose_name='آیا پرداخت شده است؟'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
    ]
