from django.contrib import admin
from .models import *
from django_jalali.admin.filters import JDateFieldListFilter

class ItemInline(admin.TabularInline):
    model = ItemOrder
    readonly_fields = ['user','product','variant','size','color','quantity',"price"]

class Order_Admin(admin.ModelAdmin):
    list_display = ['user','f_name','l_name','email','create','address','paid','get_price','code']
    inlines = [ItemInline]

class Coupon_Admin(admin.ModelAdmin):
    list_display = ['code','start','end','discount','active']
    list_filter = (
        ('code',JDateFieldListFilter),
    )
 
admin.site.register(ItemOrder)
admin.site.register(Order,Order_Admin)
admin.site.register(Coupon,Coupon_Admin)
