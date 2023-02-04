from django.contrib import admin

from .models import *


# this class for blog in admin panel.
class Blog_Admin(admin.ModelAdmin):
    list_display = ("name","create","update",)
    list_filter = ('create',)
    
admin.site.register(Blog,Blog_Admin)