from tabnanny import verbose
from home.models import *
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django_jalali.db import models as jmodels
from cart.models import *
class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name = 'کاربر')
    email = models.EmailField(verbose_name = 'ایمیل')
    create = jmodels.jDateTimeField(auto_now_add=True,verbose_name = 'زمان ایجاد')
    discount = models.PositiveIntegerField(blank=True,null=True,verbose_name = 'درصد تخفیف')
    paid = models.BooleanField(default=False,verbose_name = 'آیا پرداخت شده است؟')
    f_name = models.CharField(max_length=50,verbose_name = 'نام')
    l_name = models.CharField(max_length=50,verbose_name = 'نام خانوادگی')
    address = models.CharField(max_length=500,verbose_name = 'آدرس')
    code = models.CharField(max_length=200,null=True)
    total_to = models.IntegerField(null=True,blank=True)
    class Meta:
        verbose_name = 'فرم سفارش'
        verbose_name_plural = 'فرم های سفارش'

    def __str__(self):
        return self.user.username 
    @property
    def get_price(self):
        total = sum(i.price() for i in self.order_item.all())
        if self.discount:
            discount_price =(self.discount/100) * total
            self.total_to = int(total - discount_price)
        else:
            self.total_to  = total
        return self.total_to

class ItemOrder(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name="order_item",verbose_name = 'سفارش')
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name = 'کاربر')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name = 'محصول')
    variant = models.ForeignKey(Variantproduct,on_delete=models.CASCADE,null=True,blank=True,verbose_name = 'ویژگی')
    quantity = models.IntegerField(verbose_name = 'مقدار')
    to_int = models.IntegerField

    class Meta:
        verbose_name = 'جزئیات سفارش'
        verbose_name_plural = 'جزئیات سفارشات'

    def __str__(self) :
        return self.user.username

    def size(self):
        return self.variant.size_variant.name

    def color(self):
        return self.variant.color_variant.name
    
    def price(self):
        if self.product.status != "None":
            return self.variant.total_price * self.quantity
        else:
            return self.product.total_price * self.quantity
    

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['email','f_name','l_name',"address"]
        

class Coupon(models.Model):
    code = models.CharField(max_length=100,unique=True,verbose_name = 'کد تخفیف')
    active = models.BooleanField(default= False,verbose_name = 'آیا فعال است؟')
    start = jmodels.jDateTimeField(verbose_name = 'شروع')
    end = jmodels.jDateTimeField(verbose_name = 'پایان')
    discount = models.IntegerField(verbose_name = 'درصد تخفیف')

    class Meta:
        verbose_name = 'تخفیف'
        verbose_name_plural = '  تخفیف ها'
