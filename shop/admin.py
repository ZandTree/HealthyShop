from django.contrib import admin
from django import forms

from photologue.admin import GalleryAdmin as GalleryAdminDefault
from photologue.models import Gallery

from .models import Category,Product,Cart,CartItem,Order,Comment

from mptt.admin import MPTTModelAdmin


class CategoryMPTTModelAdmin(MPTTModelAdmin):
    mptt_level_indent = 20

admin.site.register(Category,CategoryMPTTModelAdmin)

class CartItemAdmin(admin.ModelAdmin):
    """Products in cart"""
    list_display =('cart','product','qty')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('slug','title','category','rating','price','sale','availability','gallery')
    prepopulated_fields={'slug':('title',)}

class GalleryAdminForm(forms.ModelForm):
    """Users never need to enter a description on a gallery."""

    class Meta:
        model = Gallery
        exclude = ['description']


class GalleryAdmin(GalleryAdminDefault):
    form = GalleryAdminForm

admin.site.unregister(Gallery)
admin.site.register(Gallery, GalleryAdmin)

admin.site.register(Product,ProductAdmin)
admin.site.register(Cart)
admin.site.register(CartItem,CartItemAdmin)
admin.site.register(Order)
admin.site.register(Comment)
