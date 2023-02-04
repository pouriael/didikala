
from distutils.command.upload import upload
from itertools import product
from operator import truediv
from tkinter.tix import Tree
from turtle import tracer
from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField 
from taggit.managers import TaggableManager
from accounts.models import * 
from django.forms import BooleanField, ModelForm
from django.db.models import Avg
from django_jalali.db import models as jmodels
from django.db.models.signals import post_save
from django.contrib.auth.models import User

class Category(models.Model):
    sub_category = models.ForeignKey("self", on_delete=models.CASCADE,related_name='sub',null=True,blank=True,verbose_name = 'زیر شاخه')
    sub_cat = models.BooleanField(default=False,verbose_name = 'آیا زیر شاخه است؟')
    name = models.CharField(max_length=50,verbose_name = 'اسم')
    create = jmodels.jDateTimeField(auto_now_add=True,verbose_name = 'زمان ایجاد')
    update = jmodels.jDateTimeField(auto_now=True,verbose_name = 'آخرین آپدیت')
    slug = models.SlugField(null=True,blank=True,unique=True,allow_unicode=True,verbose_name = 'شناسه')
    image = models.ImageField(upload_to="category",null=True,blank=True,verbose_name = 'تصویر')

    class Meta:
        verbose_name = 'دسته بندی '
        verbose_name_plural = 'دسته بندی ها '

    def __str__(self) :
        return self.name

    def get_absolute_url(self):
        return reverse("home:category",args=[self.slug,self.id])

class Product(models.Model):
    VARIANT =(
        ("None","none"),
        ("Size","size"),
        ("Color","color"),
        ("Both","Both"),
    )
    category = models.ManyToManyField(Category,blank=True,verbose_name = 'دسته بندی')
    name = models.CharField(max_length=50,verbose_name = 'اسم')
    amount = models.PositiveIntegerField(verbose_name = 'مقدار')
    create = jmodels.jDateTimeField(auto_now_add=True,verbose_name = 'زمان ایجاد')
    update = jmodels.jDateTimeField(auto_now=True,verbose_name = 'آخرین آپدیت')
    image = models.ImageField(upload_to ="product",verbose_name = 'تصویر')
    available = models.BooleanField(default=True,verbose_name = 'موجود است؟')
    unit_price = models.PositiveIntegerField(verbose_name = 'قیمت اصلی')
    change = models.BooleanField(default=True)
    discount = models.PositiveIntegerField(null=True,blank=True,verbose_name = 'درصد تخفیف')
    total_price = models.PositiveIntegerField(verbose_name = 'قیمت نهایی')
    information = RichTextUploadingField(blank=True,null=True,verbose_name = 'اطلاعات')
    status = models.CharField(max_length=50,choices=VARIANT,blank=True,null=True,verbose_name = 'ویژگی')
    tags =  TaggableManager(blank=True,verbose_name = 'نسبت تشابه')
    like = models.ManyToManyField(User,related_name="product_like",blank=True)
    total_like = models.IntegerField(default=0,verbose_name = 'مجموع لایک ها')
    unlike = models.ManyToManyField(User,related_name="product_unlike",blank=True)
    total_unlike = models.IntegerField(default=0,verbose_name = 'مجموع آن لایک ها')
    favourite = models.ManyToManyField(User,blank=True,related_name="fa_user",verbose_name = 'علاقه مندی')
    brand = models.ForeignKey("Brand",on_delete=models.CASCADE,blank=True,null=True,verbose_name="برند")
    size = models.ManyToManyField('ProductSize',blank=True,verbose_name='اندازه')
    color = models.ManyToManyField('ProductColor',blank=True,verbose_name='رنگ')
    total_favourite = models.PositiveIntegerField(default= 0)
    sell = models.PositiveIntegerField(default= 0)
    view = models.ManyToManyField(User,blank=True,related_name='product_view')
    num_view = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    def average(self):
        data = Comment.objects.filter(is_reply = False,product=self).aggregate(avg =Avg('rate'))
        star = 0
        if data['avg'] is not None:
            star = round(data['avg'],1)
        return star

    def total_like(self):
        return self.like.count()

    def total_unlike(self):
        return self.unlike.count()

    def __str__(self):
        return self.name

    @property
    def total_price(self):
        if not self.discount:
            return self.unit_price
        elif self.discount:
            total = (self.unit_price* self.discount)/100
            return int(self.unit_price - total)
        return self.total_price

class ProductColor(models.Model):
    name = models.CharField(max_length=20,verbose_name = 'اسم')

    class Meta:
        verbose_name = 'رنگ محصول'
        verbose_name_plural = 'رنگ محصولات'


    def __str__(self):
           return self.name

class ProductSize(models.Model):
    name = models.CharField(max_length=20,verbose_name = 'اسم') 

    class Meta:
        verbose_name = 'سایز محصول'
        verbose_name_plural = 'سایز محصولات'

    def __str__(self):
           return self.name

class Variantproduct(models.Model):
    name = models.CharField(max_length=200,verbose_name = 'اسم')
    color_variant = models.ForeignKey(ProductColor,on_delete=models.CASCADE,null=True,blank=True,verbose_name = 'رنگ')
    size_variant = models.ForeignKey(ProductSize,on_delete=models.CASCADE,null=True,blank=True,verbose_name = 'سایز')
    product_variant = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='pr',verbose_name = 'ویژگی محصول')
    unit_price = models.PositiveIntegerField(verbose_name = 'قیمت اصلی')
    discount = models.PositiveIntegerField(null=True,blank=True,verbose_name = 'درصد تخفیف')
    total_price = models.PositiveIntegerField(verbose_name = 'قیمت نهایی')
    amount = models.PositiveIntegerField(verbose_name = 'مقدار')
    change = models.BooleanField(default=True)
    update = jmodels.jDateTimeField(auto_now=True)
    class Meta:
        verbose_name = 'ویژگی محصول'
        verbose_name_plural = 'ویژگی محصولات'

    def __str__(self):
        return self.name

    @property
    def total_price(self):
        if not self.discount:
            return self.unit_price
        elif self.discount:
            total = (self.unit_price* self.discount)/100
            return int(self.unit_price - total)
        return self.total_price


class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comment_u',verbose_name = 'کاربر')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name = 'محصول')
    comment = models.TextField(verbose_name = 'نظر')
    rate = models.PositiveIntegerField(default=1,verbose_name = 'امتیاز')
    is_reply = models.BooleanField(default=False,verbose_name = 'آیا ریپلای است؟')
    reply = models.ForeignKey('self',null=True,blank=True,on_delete=models.CASCADE,related_name="comment_reply")
    create = jmodels.jDateTimeField(auto_now_add=True,verbose_name = 'زمان ایجاد')
    comment_like =models.ManyToManyField(User,blank=True,related_name='com_like',verbose_name = 'پسندیدن نظر')
    total_comment_like = models.PositiveIntegerField(default=0,verbose_name = 'مجموع لایک های نظر')

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'

    def __str__(self) :
        return self.comment

    def total_like_comment(self):
        return self.comment_like.count()

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["comment","rate"]

class ReplyForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["comment"]

class Images(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name = 'محصول')
    name = models.CharField(blank=True,max_length=25,verbose_name = 'اسم')
    image = models.ImageField(upload_to = 'image/',blank=True,verbose_name = 'تصویر')
        
    class Meta:
        verbose_name = 'تصویر'
        verbose_name_plural = 'تصاویر'

class Brand(models.Model):
    name = models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return self.name

class Chart(models.Model):
    name = models.CharField(max_length=50,blank=True,null=True)
    unit_price = models.IntegerField(default=0)
    update = jmodels.jDateTimeField(auto_now=True)
    color = models.CharField(max_length=50,blank=True,null=True)
    size = models.CharField(max_length=50,blank=True,null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True,related_name="pr_update")
    variant = models.ForeignKey(Variantproduct,on_delete=models.CASCADE,blank=True,null=True,related_name='v_update')

    def __str__(self):
        return self.name

def product_post_save(sender,instance,created,*args,**kwargs):
    data = instance
    if data.change == False:
        Chart.objects.create(product=data,unit_price = data.unit_price,update= data.update,name=data.name)

post_save.connect(product_post_save,sender=Product)

def variant_post_save(sender,instance,created,*args,**kwargs):
    data = instance
    if data.change == False:
        Chart.objects.create(variant=data,unit_price = data.unit_price,update= data.update,name=data.name,size = data.size_variant,color= data.color_variant)

post_save.connect(variant_post_save,sender=Variantproduct) 

class Views(models.Model):
    ip = models.CharField(max_length=200,null=True,blank=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,blank=True,null=True)
    create = jmodels.jDateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.product.name

class Gallery(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    image = models.ImageField(upload_to = 'gallery/',blank=True)
    text = models.CharField(max_length=500,null=True,blank=True)
    
    def __str__(self) :
        return self.name