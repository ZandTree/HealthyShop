from django.contrib import admin
from .models import Category,Product,Cart,CartItem,Order

from mptt.admin import MPTTModelAdmin


class CategoryMPTTModelAdmin(MPTTModelAdmin):
    # specify pixel amount for this ModelAdmin only:
    mptt_level_indent = 20

#example how to attach MPTTModelAdmin ==> admin.site.register(Node, CustomMPTTModelAdmin)
admin.site.register(Category,CategoryMPTTModelAdmin)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
