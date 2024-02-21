from django.contrib import admin

from .models import Productmaster,Categorymaster,Customermaster,Subcategorymaster,Inventorymaster,Blg

# Register your models here.
admin.site.register(Productmaster)
admin.site.register(Categorymaster)
admin.site.register(Customermaster)
admin.site.register(Subcategorymaster)
admin.site.register(Inventorymaster)
admin.site.register(Blg)
