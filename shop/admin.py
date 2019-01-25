from django.contrib import admin
from .models import Category,Product,Cart,CartItem,Order
#from .models import ImageGroup

from mptt.admin import MPTTModelAdmin


class CategoryMPTTModelAdmin(MPTTModelAdmin):
    # specify pixel amount for this ModelAdmin only:
    mptt_level_indent = 20

#example how to attach MPTTModelAdmin ==> admin.site.register(Node, CustomMPTTModelAdmin)
admin.site.register(Category,CategoryMPTTModelAdmin)

class CartItemAdmin(admin.ModelAdmin):
    """Products in cart"""
    list_display =('cart','product','qty')

#admin.site.register(ImageGroup)


admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem,CartItemAdmin)
admin.site.register(Order)
