
from random import choices
from tkinter import Widget
import django_filters
from django import forms
from .models import *

class ProductFilter(django_filters.FilterSet):
    choice_1 ={
        ('گران ترین','گران ترین'),
        ('ارزان ترین','ارزان ترین')
    }

    choice_2 ={
        ('قدیمی ترین','قدیمی ترین'),
        ('جدید ترین','جدید ترین'),
        
    }

    choice_3 ={
        ('بیشترین تخفیف','بیشترین تخفیف'),
        ('کم تخفیف','کم تخفیف')
    }

    choice_4 ={
        ('کم محبوب','کم محبوب'),
        ('محبوب ترین','محبوب ترین')
    }

    choice_5 ={
        ('پر فروش ترین','پر فروش ترین'),
        ("کم فروش ترین",'کم فروش ترین')
    }
    price_1 = django_filters.NumberFilter(field_name='unit_price',lookup_expr="gte") 
    price_2 = django_filters.NumberFilter(field_name='unit_price',lookup_expr="lte") 
    brand = django_filters.ModelMultipleChoiceFilter(queryset=Brand.objects.all(),widget=forms.CheckboxSelectMultiple)
    size = django_filters.ModelMultipleChoiceFilter(queryset = ProductSize.objects.all(),widget = forms.CheckboxSelectMultiple)
    color = django_filters.ModelMultipleChoiceFilter(queryset = ProductColor.objects.all(),widget = forms.CheckboxSelectMultiple)
    price = django_filters.ChoiceFilter(choices = choice_1,method = 'price_filter')
    create = django_filters.ChoiceFilter(choices = choice_2,method = 'create_filter')
    discount = django_filters.ChoiceFilter(choices = choice_3,method = 'discount_filter')
    sell = django_filters.ChoiceFilter(choices=choice_5,method = 'sell_filter')
    favourite = django_filters.ChoiceFilter(choices=choice_4,method = 'favourite_filter')

    def price_filter(self,queryset,name,value):
        data = 'unit_price' if value == 'ارزان ترین' else '-unit_price'
        return queryset.order_by(data)

    def create_filter(self,queryset,name,value):
        data = "create" if value == 'قدیمی ترین' else '-create'
        return queryset.order_by(data)

    def discount_filter(self,queryset,name,value):
        data = "discount" if value == 'بیشترین تخفیف' else '-discount'
        return queryset.order_by(data)

    def sell_filter(self,queryset,name,value):
        data = "sell" if value == 'پر فروش ترین' else '-sell'
        return queryset.order_by(data)

    def favourite_filter(self,queryset,name,value):
        data = "favourite" if value == 'محبوب ترین' else '-favourite'
        return queryset.order_by(data)

