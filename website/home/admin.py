from django.contrib import admin
from .models import *
import admin_thumbnails

class ProductVariantInlines(admin.TabularInline):
    model = Variantproduct

@admin_thumbnails.thumbnail('image')
class ImagesInlines(admin.TabularInline):
    model = Images

class Category_Admin(admin.ModelAdmin):
    list_display = ("name","create","update",'sub_category')
    list_filter = ('create',)
    prepopulated_fields = {
        'slug':("name",)
    }
admin.site.register(Category,Category_Admin)


class Product_Admin(admin.ModelAdmin):
    list_display = ['name','create', 'update','amount','available','unit_price','discount','total_price']
    list_filter = ('available',)
    list_editable = ('amount',)
    raw_id_fields = ('category',)
    change_list_template = 'home/change.html'
    inlines = [ProductVariantInlines,ImagesInlines]
admin.site.register(Product,Product_Admin)



class ProductColorAdmin(admin.ModelAdmin):
    list_display = ["name","id"]
admin.site.register(ProductColor,ProductColorAdmin)

class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ["name","id"]
admin.site.register(ProductSize,ProductSizeAdmin)

class ProductVariantAdmin(admin.ModelAdmin):
    list_display =["name","id"]
admin.site.register(Variantproduct,ProductVariantAdmin)

class Comment_Admin(admin.ModelAdmin):
    list_display = ["user","create",'rate']
admin.site.register(Comment,Comment_Admin)

admin.site.register(Images)
admin.site.register(Brand)
admin.site.register(Chart)
admin.site.register(Views)
admin.site.register(Gallery)