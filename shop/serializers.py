from django.db.models import Q
from rest_framework import serializers
# рекурсивно забирает всех детей
from rest_framework_recursive.fields import RecursiveField

from photologue.models import Gallery, Photo

from .models import Product, Category


class PhotoSer(serializers.ModelSerializer):
    """Photos"""
    class Meta:
        model = Photo
        fields = ("image",)

# if you need you can serial Gallery
# class GallerySer(serializers.ModelSerializer):
#     """Gallery"""
#     #let op: many=True allows to serial manyToMany\ForeignKey rel obj
#     # here m2m with Photos
#     photos = PhotoSer(many=True)
#     class Meta:
#         model = Gallery
#         fields = ("photos",)


class CatSer(serializers.ModelSerializer):
    """Categories"""
    children = serializers.ListField(source='get_children', read_only=True,
                                     child=RecursiveField(), )

    class Meta:
        model = Category
        # see model as well
        fields = ("name", "children",)


class ProductSer(serializers.ModelSerializer):
    """Products seriolizing"""
    #gallery = GallerySer()  # if you need it
    photo = PhotoSer()

    class Meta:
        model = Product
        fields = (
            "title",
            "description",
            "price",
            "slug",
            "availability",
            "quantity",
            "photo",
            # if you need it: here gallery ser-ed
            #'gallery'
        )
