from .models import *

import django_filters

# this class for filter on blog.
class BlogFilter(django_filters.FilterSet):
    choice_2 ={
        ('قدیمی ترین','قدیمی ترین'),
        ('جدید ترین','جدید ترین'),
        
    }

    create = django_filters.ChoiceFilter(choices = choice_2,method = 'create_filter')


    def create_filter(self,queryset,name,value):
        data = "create" if value == 'قدیمی ترین' else '-create'
        return queryset.order_by(data)


  

