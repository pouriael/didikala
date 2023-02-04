from django.contrib import admin

from .models import *

class CartAdmin(admin.ModelAdmin):
    list_display = ['user','product','variants','quantity']

class CompareAdmin(admin.ModelAdmin):
    list_display = ['user','product','session_key']
 
admin.site.register(Cart,CartAdmin)
admin.site.register(Compare,CompareAdmin)