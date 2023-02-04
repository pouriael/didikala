from django.contrib import admin

from .models import formprofile

# this class for profile in admin panel.
class profile_admin(admin.ModelAdmin):
    list_display = ['user','phone','address']

admin.site.register(formprofile,profile_admin)

