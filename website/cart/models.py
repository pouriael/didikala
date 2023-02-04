from dataclasses import field
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from home.models import Product, Variantproduct

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name = 'کاربر')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name = 'محصول')
    variants = models.ForeignKey(Variantproduct,on_delete=models.CASCADE,blank=True,null=True,verbose_name = 'ویژگی')
    quantity = models.PositiveIntegerField(verbose_name = 'مقدار')

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبد های خرید'

    def __str__(self) :
        return self.user.username

class CartForm(ModelForm):
    class Meta:
        model = Cart
        fields = ['quantity']

class Compare(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
    session_key = models.CharField(max_length=300,null=True,blank=True)

    def __str__(self) :
        return self.product.name

class CompareForm(ModelForm):
    class Meta:
        model = Compare
        fields = ['product']